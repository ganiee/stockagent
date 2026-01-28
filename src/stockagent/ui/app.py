"""Streamlit UI for StockAgent."""

import json

import streamlit as st

from stockagent.graph import run_analysis


# Page configuration
st.set_page_config(
    page_title="StockAgent - Stock Analysis Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def init_session_state():
    """Initialize session state variables."""
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "current_ticker" not in st.session_state:
        st.session_state.current_ticker = ""
    if "last_analyzed_ticker" not in st.session_state:
        st.session_state.last_analyzed_ticker = ""


def set_ticker(ticker: str):
    """Set the ticker in session state."""
    st.session_state.current_ticker = ticker


def render_header():
    """Render the page header."""
    st.title("📈 StockAgent")
    st.markdown("*AI-powered stock analysis using technical indicators and news sentiment*")
    st.divider()


def render_ticker_input():
    """Render ticker input section."""
    col1, col2 = st.columns([2, 3])

    with col1:
        ticker = st.text_input(
            "Enter Ticker Symbol",
            value=st.session_state.current_ticker,
            placeholder="e.g., AAPL",
            key="ticker_input",
            help="Enter a stock ticker symbol (e.g., AAPL for Apple Inc.)",
        )
        if ticker != st.session_state.current_ticker:
            st.session_state.current_ticker = ticker.upper().strip()

    with col2:
        st.markdown("**Quick Select:**")
        quick_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
        cols = st.columns(len(quick_tickers))
        for i, t in enumerate(quick_tickers):
            with cols[i]:
                if st.button(t, key=f"quick_{t}", use_container_width=True):
                    st.session_state.current_ticker = t
                    st.rerun()

    return st.session_state.current_ticker


def render_metrics(result: dict):
    """Render metrics row with analysis results."""
    col1, col2, col3, col4 = st.columns(4)

    # Price metric
    with col1:
        current_price = result.get("current_price", 0.0)
        previous_close = result.get("previous_close", 0.0)
        if current_price and previous_close:
            price_change = current_price - previous_close
            price_delta = f"{price_change:+.2f}"
        else:
            price_delta = None
        st.metric(
            label="Current Price",
            value=f"${current_price:.2f}" if current_price else "N/A",
            delta=price_delta,
        )

    # RSI metric
    with col2:
        technical = result.get("technical_signals", {})
        rsi = technical.get("rsi")
        rsi_interp = technical.get("rsi_interpretation", "N/A")
        st.metric(
            label="RSI (14)",
            value=f"{rsi:.1f}" if rsi is not None else "N/A",
            delta=rsi_interp.capitalize() if rsi is not None else None,
            delta_color="off",
        )

    # Sentiment metric
    with col3:
        sentiment = result.get("news_sentiment", {})
        sentiment_score = sentiment.get("overall_score", 0.0)
        sentiment_label = sentiment.get("overall_label", "neutral")
        delta_color = "normal" if sentiment_score >= 0 else "inverse"
        st.metric(
            label="News Sentiment",
            value=f"{sentiment_score:+.2f}",
            delta=sentiment_label.capitalize(),
            delta_color="off",
        )

    # Recommendation metric
    with col4:
        recommendation = result.get("recommendation", "N/A")
        confidence = result.get("confidence", 0.0)
        st.metric(
            label="Recommendation",
            value=recommendation,
            delta=f"{confidence:.0f}% confidence",
            delta_color="off",
        )


def render_tabs(result: dict):
    """Render tabbed interface with analysis details."""
    tab1, tab2, tab3 = st.tabs(["📄 Full Report", "📊 Technical Data", "📰 News Headlines"])

    with tab1:
        synthesis = result.get("synthesis", "")
        if synthesis:
            st.markdown(synthesis)
        else:
            st.info("No report generated.")

    with tab2:
        technical = result.get("technical_signals", {})
        if technical:
            st.json(technical)
        else:
            st.info("No technical data available.")

    with tab3:
        sentiment = result.get("news_sentiment", {})
        headlines = sentiment.get("headlines", [])
        if headlines:
            for headline in headlines:
                title = headline.get("title", "")
                label = headline.get("label", "neutral")
                score = headline.get("score", 0.0)
                url = headline.get("url", "")

                # Color code based on sentiment
                if label == "positive":
                    emoji = "🟢"
                elif label == "negative":
                    emoji = "🔴"
                else:
                    emoji = "⚪"

                col1, col2 = st.columns([4, 1])
                with col1:
                    if url:
                        st.markdown(f"{emoji} [{title}]({url})")
                    else:
                        st.markdown(f"{emoji} {title}")
                with col2:
                    st.caption(f"{label} ({score:+.2f})")
        else:
            st.info("No news headlines found.")


def render_errors(result: dict):
    """Render any errors from the analysis."""
    errors = result.get("errors", [])
    if errors:
        with st.expander("⚠️ Analysis Warnings", expanded=False):
            for error in errors:
                st.warning(error)


def render_disclaimer():
    """Render disclaimer footer."""
    st.divider()
    st.caption(
        "**Disclaimer:** This tool is for educational and informational purposes only. "
        "It does not constitute financial advice. Always conduct your own research and "
        "consult a qualified financial advisor before making investment decisions. "
        "Data provided by Polygon.io. News sourced via DuckDuckGo."
    )


def main():
    """Main application entry point."""
    init_session_state()
    render_header()

    # Ticker input section
    ticker = render_ticker_input()

    # Run analysis button
    st.markdown("")  # Spacer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_button = st.button(
            "🔍 Run Analysis",
            disabled=not ticker,
            use_container_width=True,
            type="primary",
        )

    # Handle analysis
    if run_button and ticker:
        # Clear previous results if ticker changed
        if ticker != st.session_state.last_analyzed_ticker:
            st.session_state.analysis_result = None

        with st.spinner(f"Analyzing {ticker}..."):
            try:
                result = run_analysis(ticker)
                st.session_state.analysis_result = result
                st.session_state.last_analyzed_ticker = ticker
            except Exception as e:
                st.error(f"Error analyzing {ticker}: {str(e)}")
                st.session_state.analysis_result = None

    # Display results
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result

        st.markdown("")  # Spacer
        st.subheader(f"Analysis Results: {result.get('company_name', ticker)}")

        # Render components
        render_errors(result)
        render_metrics(result)
        st.markdown("")  # Spacer
        render_tabs(result)

    # Always show disclaimer
    render_disclaimer()


if __name__ == "__main__":
    main()
