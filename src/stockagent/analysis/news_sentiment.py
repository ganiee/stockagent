"""News sentiment analysis using DuckDuckGo search."""

import logging
from typing import Any

from duckduckgo_search import DDGS

from stockagent.models import SentimentResult

logger = logging.getLogger(__name__)

# Sentiment keyword lists (lowercase)
POSITIVE_KEYWORDS = [
    "surge",
    "surges",
    "growth",
    "profit",
    "profits",
    "bullish",
    "upgrade",
    "upgraded",
    "beat",
    "beats",
    "record",
    "strong",
    "gain",
    "gains",
    "rally",
    "rallies",
    "soar",
    "soars",
    "jump",
    "jumps",
    "rise",
    "rises",
    "positive",
    "boost",
    "outperform",
    "buy",
    "winner",
    "success",
    "breakthrough",
    "innovation",
]

NEGATIVE_KEYWORDS = [
    "crash",
    "crashes",
    "loss",
    "losses",
    "decline",
    "declines",
    "bearish",
    "downgrade",
    "downgraded",
    "miss",
    "misses",
    "weak",
    "fall",
    "falls",
    "drop",
    "drops",
    "plunge",
    "plunges",
    "sink",
    "sinks",
    "tumble",
    "tumbles",
    "negative",
    "warning",
    "layoff",
    "layoffs",
    "cut",
    "cuts",
    "sell",
    "underperform",
    "loser",
    "failure",
    "concern",
    "risk",
    "lawsuit",
    "investigation",
]


def analyze_sentiment(headline: str) -> dict:
    """Analyze sentiment of a single headline using keyword matching.

    Args:
        headline: News headline text

    Returns:
        dict with:
            - score: float (-1.0 to +1.0)
            - label: "positive", "negative", or "neutral"
            - positive_count: int
            - negative_count: int
    """
    if not headline:
        return {
            "score": 0.0,
            "label": "neutral",
            "positive_count": 0,
            "negative_count": 0,
        }

    headline_lower = headline.lower()

    # Count keyword matches
    positive_count = sum(1 for kw in POSITIVE_KEYWORDS if kw in headline_lower)
    negative_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw in headline_lower)

    # Calculate score: (positive - negative) / (positive + negative + 1)
    # Adding 1 to denominator avoids division by zero and normalizes
    score = (positive_count - negative_count) / (positive_count + negative_count + 1)

    # Clamp to range [-1.0, +1.0]
    score = max(-1.0, min(1.0, score))

    # Determine label based on thresholds
    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return {
        "score": score,
        "label": label,
        "positive_count": positive_count,
        "negative_count": negative_count,
    }


def fetch_news(
    ticker: str, company_name: str = "", max_results: int = 8
) -> list[dict[str, Any]]:
    """Fetch recent news headlines for a stock.

    Args:
        ticker: Stock ticker symbol
        company_name: Company name for better search results
        max_results: Maximum number of results to fetch

    Returns:
        List of news article dicts with title, url, date, source
    """
    # Build search query
    if company_name:
        query = f"{company_name} stock"
    else:
        query = f"{ticker} stock"

    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))

        # Transform results to our format
        articles = []
        for result in results:
            article = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "date": result.get("date", ""),
                "source": result.get("source", ""),
            }
            articles.append(article)

        return articles

    except Exception as e:
        logger.warning(f"Error fetching news for {ticker}: {e}")
        return []


def analyze_news_sentiment(ticker: str, company_name: str = "") -> SentimentResult:
    """Analyze news sentiment for a stock.

    Fetches recent news and computes aggregate sentiment score.

    Args:
        ticker: Stock ticker symbol
        company_name: Company name for better search results

    Returns:
        SentimentResult dict with overall score, label, and headlines
    """
    # Fetch news
    articles = fetch_news(ticker, company_name, max_results=8)

    if not articles:
        # No news found - return neutral
        return {
            "overall_score": 0.0,
            "overall_label": "neutral",
            "headlines": [],
            "headline_count": 0,
        }

    # Analyze each headline
    analyzed_headlines = []
    scores = []

    for article in articles:
        title = article.get("title", "")
        if not title:
            continue

        sentiment = analyze_sentiment(title)
        scores.append(sentiment["score"])

        analyzed_headlines.append({
            "title": title,
            "url": article.get("url", ""),
            "date": article.get("date", ""),
            "score": sentiment["score"],
            "label": sentiment["label"],
        })

    if not scores:
        return {
            "overall_score": 0.0,
            "overall_label": "neutral",
            "headlines": [],
            "headline_count": 0,
        }

    # Calculate aggregate score (average)
    overall_score = sum(scores) / len(scores)

    # Determine overall label
    if overall_score > 0.2:
        overall_label = "positive"
    elif overall_score < -0.2:
        overall_label = "negative"
    else:
        overall_label = "neutral"

    # Sort by absolute sentiment and keep top 5
    analyzed_headlines.sort(key=lambda x: abs(x["score"]), reverse=True)
    top_headlines = analyzed_headlines[:5]

    return {
        "overall_score": overall_score,
        "overall_label": overall_label,
        "headlines": top_headlines,
        "headline_count": len(scores),
    }
