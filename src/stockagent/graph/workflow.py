"""LangGraph workflow for stock analysis."""

import logging
from typing import Annotated, Any

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from stockagent.analysis import (
    analyze_news_sentiment,
    calculate_all_indicators,
    calculate_composite_score,
    generate_recommendation,
    generate_report,
    get_explanation_factors,
)
from stockagent.data import PolygonClient, PolygonAPIError
from stockagent.models import StockAnalysisState

logger = logging.getLogger(__name__)


def merge_lists(left: list, right: list) -> list:
    """Merge two lists, used for error accumulation."""
    return left + right


# Define state with reducer for errors
class WorkflowState(StockAnalysisState):
    """Workflow state with error accumulation."""
    errors: Annotated[list[str], merge_lists]


def fetch_data(state: WorkflowState) -> dict[str, Any]:
    """Fetch stock data from Polygon.io.

    Args:
        state: Current workflow state with ticker

    Returns:
        Updated state fields: price_data, company_name, current_price, previous_close
    """
    ticker = state.get("ticker", "").upper().strip()
    errors = []

    if not ticker:
        return {"errors": ["No ticker provided"]}

    try:
        client = PolygonClient()

        # Fetch all data
        price_data = []
        company_name = ticker
        current_price = 0.0
        previous_close = 0.0

        try:
            aggregates = client.get_stock_aggregates(ticker, days=90)
            price_data = aggregates
        except PolygonAPIError as e:
            errors.append(f"Error fetching price data: {e}")

        try:
            details = client.get_ticker_details(ticker)
            company_name = details.get("company_name", ticker)
        except PolygonAPIError as e:
            errors.append(f"Error fetching company details: {e}")

        try:
            close_data = client.get_previous_close(ticker)
            current_price = close_data.get("current_price", 0.0)
            previous_close = close_data.get("previous_close", 0.0)
        except PolygonAPIError as e:
            errors.append(f"Error fetching price: {e}")

        return {
            "price_data": price_data,
            "company_name": company_name,
            "current_price": current_price,
            "previous_close": previous_close,
            "errors": errors,
        }

    except Exception as e:
        logger.error(f"Unexpected error in fetch_data: {e}")
        return {"errors": [f"Unexpected error fetching data: {e}"]}


def technical_analysis(state: WorkflowState) -> dict[str, Any]:
    """Calculate technical indicators from price data.

    Args:
        state: Current workflow state with price_data

    Returns:
        Updated state field: technical_signals
    """
    price_data = state.get("price_data", [])

    if not price_data:
        return {
            "technical_signals": {
                "rsi": None,
                "rsi_interpretation": "neutral",
                "macd": None,
                "macd_interpretation": "neutral",
                "bollinger": None,
                "sma_20": None,
                "sma_50": None,
                "sma_200": None,
                "current_price": state.get("current_price", 0.0),
            }
        }

    try:
        signals = calculate_all_indicators(price_data)
        # Update current_price from state if available
        if state.get("current_price"):
            signals["current_price"] = state["current_price"]
        return {"technical_signals": signals}
    except Exception as e:
        logger.error(f"Error in technical_analysis: {e}")
        return {
            "technical_signals": {
                "rsi": None,
                "rsi_interpretation": "neutral",
                "macd": None,
                "macd_interpretation": "neutral",
                "bollinger": None,
                "sma_20": None,
                "sma_50": None,
                "sma_200": None,
                "current_price": state.get("current_price", 0.0),
            },
            "errors": [f"Error calculating indicators: {e}"],
        }


def news_sentiment_node(state: WorkflowState) -> dict[str, Any]:
    """Analyze news sentiment for the stock.

    Args:
        state: Current workflow state with ticker and company_name

    Returns:
        Updated state field: news_sentiment
    """
    ticker = state.get("ticker", "")
    company_name = state.get("company_name", "")

    try:
        sentiment = analyze_news_sentiment(ticker, company_name)
        return {"news_sentiment": sentiment}
    except Exception as e:
        logger.error(f"Error in news_sentiment: {e}")
        return {
            "news_sentiment": {
                "overall_score": 0.0,
                "overall_label": "neutral",
                "headlines": [],
                "headline_count": 0,
            },
            "errors": [f"Error analyzing news sentiment: {e}"],
        }


def synthesize(state: WorkflowState) -> dict[str, Any]:
    """Synthesize analysis into a markdown report.

    Generates a comprehensive report from all analysis data.

    Args:
        state: Current workflow state

    Returns:
        Updated state field: synthesis
    """
    try:
        report = generate_report(state)
        return {"synthesis": report}
    except Exception as e:
        logger.error(f"Error in synthesize: {e}")
        return {
            "synthesis": f"Error generating report: {e}",
            "errors": [f"Report generation error: {e}"],
        }


def recommend(state: WorkflowState) -> dict[str, Any]:
    """Generate recommendation based on analysis.

    Uses scoring engine to combine technical signals and sentiment
    into a final recommendation with confidence and explanation.

    Args:
        state: Current workflow state

    Returns:
        Updated state fields: recommendation, confidence, explanation_factors
    """
    technical_signals = state.get("technical_signals", {})
    sentiment = state.get("news_sentiment", {})

    try:
        # Calculate composite score
        score = calculate_composite_score(technical_signals, sentiment)

        # Generate recommendation and confidence
        recommendation, confidence = generate_recommendation(score)

        # Get explanation factors
        factors = get_explanation_factors(technical_signals, sentiment)

        # Add score to factors for transparency
        if not factors:
            factors = ["Insufficient data for detailed analysis"]

        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "explanation_factors": factors,
        }
    except Exception as e:
        logger.error(f"Error in recommend: {e}")
        return {
            "recommendation": "HOLD",
            "confidence": 0.0,
            "explanation_factors": [f"Error generating recommendation: {e}"],
            "errors": [f"Recommendation error: {e}"],
        }


def create_workflow() -> CompiledStateGraph:
    """Create and compile the stock analysis workflow graph.

    The workflow follows this structure:
    START -> fetch_data -> [technical_analysis, news_sentiment] (parallel)
          -> synthesize -> recommend -> END

    Returns:
        Compiled LangGraph StateGraph
    """
    # Create the graph
    graph = StateGraph(WorkflowState)

    # Add nodes
    graph.add_node("fetch_data", fetch_data)
    graph.add_node("technical_analysis", technical_analysis)
    graph.add_node("news_sentiment", news_sentiment_node)
    graph.add_node("synthesize", synthesize)
    graph.add_node("recommend", recommend)

    # Wire edges
    # START -> fetch_data
    graph.add_edge(START, "fetch_data")

    # fetch_data -> parallel analysis nodes
    graph.add_edge("fetch_data", "technical_analysis")
    graph.add_edge("fetch_data", "news_sentiment")

    # Both analysis nodes -> synthesize
    graph.add_edge("technical_analysis", "synthesize")
    graph.add_edge("news_sentiment", "synthesize")

    # synthesize -> recommend -> END
    graph.add_edge("synthesize", "recommend")
    graph.add_edge("recommend", END)

    # Compile and return
    return graph.compile()


def run_analysis(ticker: str) -> dict[str, Any]:
    """Run complete stock analysis for a ticker.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')

    Returns:
        Complete StockAnalysisState with all analysis results
    """
    # Initialize state
    initial_state: WorkflowState = {
        "ticker": ticker.upper().strip(),
        "price_data": [],
        "company_name": "",
        "current_price": 0.0,
        "previous_close": 0.0,
        "technical_signals": {},
        "news_sentiment": {},
        "synthesis": "",
        "recommendation": "",
        "confidence": 0.0,
        "explanation_factors": [],
        "errors": [],
    }

    # Create and run workflow
    workflow = create_workflow()
    result = workflow.invoke(initial_state)

    return result
