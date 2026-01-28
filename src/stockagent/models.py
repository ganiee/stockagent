"""Data models for StockAgent."""

from typing import TypedDict


class OHLCV(TypedDict):
    """Open, High, Low, Close, Volume price bar."""

    open: float
    high: float
    low: float
    close: float
    volume: int
    timestamp: str


class MACDResult(TypedDict):
    """MACD indicator result."""

    macd_line: float
    signal_line: float
    histogram: float


class BollingerBands(TypedDict):
    """Bollinger Bands result."""

    upper: float
    middle: float
    lower: float


class TechnicalSignals(TypedDict, total=False):
    """Technical analysis signals."""

    rsi: float | None
    rsi_interpretation: str
    macd: MACDResult | None
    macd_interpretation: str
    bollinger: BollingerBands | None
    sma_20: float | None
    sma_50: float | None
    sma_200: float | None
    current_price: float


class HeadlineSentiment(TypedDict):
    """Individual headline with sentiment."""

    title: str
    url: str
    date: str
    score: float
    label: str


class SentimentResult(TypedDict):
    """News sentiment analysis result."""

    overall_score: float
    overall_label: str
    headlines: list[HeadlineSentiment]
    headline_count: int


class StockAnalysisState(TypedDict, total=False):
    """Complete state for stock analysis workflow."""

    # Input
    ticker: str

    # Fetched data
    price_data: list[OHLCV]
    company_name: str
    current_price: float
    previous_close: float

    # Computed data
    technical_signals: TechnicalSignals
    news_sentiment: SentimentResult

    # Output
    synthesis: str
    recommendation: str
    confidence: float
    explanation_factors: list[str]

    # Errors
    errors: list[str]
