"""Analysis layer for technical indicators and sentiment."""

from stockagent.analysis.indicators import (
    calculate_all_indicators,
    calculate_bollinger_bands,
    calculate_ema,
    calculate_macd,
    calculate_rsi,
    calculate_sma,
    interpret_macd,
    interpret_rsi,
)
from stockagent.analysis.news_sentiment import (
    analyze_news_sentiment,
    analyze_sentiment,
    fetch_news,
)
from stockagent.analysis.scoring import (
    calculate_composite_score,
    generate_recommendation,
    get_explanation_factors,
    score_bollinger,
    score_macd,
    score_moving_averages,
    score_rsi,
    score_sentiment,
)

__all__ = [
    # Indicators
    "calculate_all_indicators",
    "calculate_sma",
    "calculate_rsi",
    "calculate_ema",
    "calculate_macd",
    "calculate_bollinger_bands",
    "interpret_rsi",
    "interpret_macd",
    # News sentiment
    "analyze_news_sentiment",
    "analyze_sentiment",
    "fetch_news",
    # Scoring
    "calculate_composite_score",
    "generate_recommendation",
    "get_explanation_factors",
    "score_rsi",
    "score_macd",
    "score_moving_averages",
    "score_bollinger",
    "score_sentiment",
]
