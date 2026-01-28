"""Shared pytest fixtures for StockAgent tests."""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_env_with_api_key(monkeypatch):
    """Set up environment with valid API key."""
    monkeypatch.setenv("POLYGON_API_KEY", "test_api_key_12345")


@pytest.fixture
def mock_env_without_api_key(monkeypatch):
    """Set up environment without API key."""
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)


@pytest.fixture
def sample_ohlcv_data():
    """Sample OHLCV price data for testing."""
    return [
        {"open": 100.0, "high": 105.0, "low": 99.0, "close": 103.0, "volume": 1000000, "timestamp": "2024-01-01"},
        {"open": 103.0, "high": 107.0, "low": 102.0, "close": 106.0, "volume": 1100000, "timestamp": "2024-01-02"},
        {"open": 106.0, "high": 108.0, "low": 104.0, "close": 105.0, "volume": 900000, "timestamp": "2024-01-03"},
        {"open": 105.0, "high": 106.0, "low": 101.0, "close": 102.0, "volume": 1200000, "timestamp": "2024-01-04"},
        {"open": 102.0, "high": 104.0, "low": 100.0, "close": 103.0, "volume": 1000000, "timestamp": "2024-01-05"},
    ]


@pytest.fixture
def sample_price_series():
    """Sample close prices for indicator calculations."""
    return [
        100.0, 102.0, 101.0, 103.0, 105.0, 104.0, 106.0, 108.0, 107.0, 109.0,
        110.0, 108.0, 106.0, 107.0, 109.0, 111.0, 110.0, 112.0, 114.0, 113.0,
        115.0, 114.0, 116.0, 118.0, 117.0, 119.0, 120.0, 118.0, 116.0, 117.0,
    ]


@pytest.fixture
def sample_technical_signals():
    """Sample technical signals for testing."""
    return {
        "rsi": 55.0,
        "rsi_interpretation": "neutral",
        "macd": {"macd_line": 1.5, "signal_line": 1.0, "histogram": 0.5},
        "macd_interpretation": "bullish",
        "bollinger": {"upper": 120.0, "middle": 110.0, "lower": 100.0},
        "sma_20": 108.0,
        "sma_50": 105.0,
        "sma_200": 95.0,
        "current_price": 115.0,
    }


@pytest.fixture
def sample_sentiment_result():
    """Sample sentiment result for testing."""
    return {
        "overall_score": 0.35,
        "overall_label": "positive",
        "headlines": [
            {"title": "Stock surges on earnings beat", "url": "http://example.com/1", "date": "2024-01-01", "score": 0.8, "label": "positive"},
            {"title": "Analyst upgrades rating", "url": "http://example.com/2", "date": "2024-01-02", "score": 0.5, "label": "positive"},
        ],
        "headline_count": 2,
    }


@pytest.fixture
def sample_stock_state(sample_ohlcv_data, sample_technical_signals, sample_sentiment_result):
    """Sample complete stock analysis state."""
    return {
        "ticker": "TEST",
        "price_data": sample_ohlcv_data,
        "company_name": "Test Company Inc.",
        "current_price": 115.0,
        "previous_close": 110.0,
        "technical_signals": sample_technical_signals,
        "news_sentiment": sample_sentiment_result,
        "synthesis": "",
        "recommendation": "BUY",
        "confidence": 65.0,
        "explanation_factors": ["RSI neutral", "MACD bullish"],
        "errors": [],
    }
