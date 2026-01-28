"""Tests for Feature 001: Project Bootstrap."""

import pytest


class TestProjectStructure:
    """Test that project structure exists."""

    @pytest.mark.feature001
    def test_src_stockagent_package_exists(self):
        """Test that stockagent package can be imported."""
        import stockagent

        assert hasattr(stockagent, "__version__")
        assert stockagent.__version__ == "0.1.0"

    @pytest.mark.feature001
    def test_subpackages_exist(self):
        """Test that all subpackages can be imported."""
        from stockagent import data
        from stockagent import analysis
        from stockagent import graph
        from stockagent import ui
        from stockagent import utils

        # Just verify they import without error
        assert data is not None
        assert analysis is not None
        assert graph is not None
        assert ui is not None
        assert utils is not None


class TestConfigModule:
    """Test configuration module."""

    @pytest.mark.feature001
    def test_load_config_with_api_key(self, mock_env_with_api_key):
        """Test that config loads successfully with API key set."""
        from stockagent.config import load_config

        config = load_config()
        assert "POLYGON_API_KEY" in config
        assert config["POLYGON_API_KEY"] == "test_api_key_12345"

    @pytest.mark.feature001
    def test_load_config_without_api_key_raises(self, mock_env_without_api_key):
        """Test that config raises ValueError when API key missing."""
        from stockagent.config import load_config

        with pytest.raises(ValueError) as exc_info:
            load_config()

        error_msg = str(exc_info.value)
        assert "POLYGON_API_KEY" in error_msg
        assert "required" in error_msg.lower()

    @pytest.mark.feature001
    def test_get_polygon_api_key(self, mock_env_with_api_key):
        """Test get_polygon_api_key helper function."""
        from stockagent.config import get_polygon_api_key

        key = get_polygon_api_key()
        assert key == "test_api_key_12345"

    @pytest.mark.feature001
    def test_error_message_is_helpful(self, mock_env_without_api_key):
        """Test that error message guides user to solution."""
        from stockagent.config import load_config

        with pytest.raises(ValueError) as exc_info:
            load_config()

        error_msg = str(exc_info.value)
        # Should mention .env file or environment
        assert ".env" in error_msg or "environment" in error_msg.lower()


class TestModelsModule:
    """Test models module."""

    @pytest.mark.feature001
    def test_stock_analysis_state_import(self):
        """Test that StockAnalysisState can be imported."""
        from stockagent.models import StockAnalysisState

        assert StockAnalysisState is not None

    @pytest.mark.feature001
    def test_stock_analysis_state_is_typed_dict(self):
        """Test that StockAnalysisState is a TypedDict."""
        from stockagent.models import StockAnalysisState
        from typing import get_type_hints

        hints = get_type_hints(StockAnalysisState)
        # Check for expected fields
        assert "ticker" in hints
        assert "price_data" in hints
        assert "technical_signals" in hints
        assert "news_sentiment" in hints
        assert "recommendation" in hints
        assert "confidence" in hints
        assert "errors" in hints

    @pytest.mark.feature001
    def test_ohlcv_type_exists(self):
        """Test that OHLCV type can be imported."""
        from stockagent.models import OHLCV
        from typing import get_type_hints

        hints = get_type_hints(OHLCV)
        assert "open" in hints
        assert "high" in hints
        assert "low" in hints
        assert "close" in hints
        assert "volume" in hints

    @pytest.mark.feature001
    def test_technical_signals_type_exists(self):
        """Test that TechnicalSignals type can be imported."""
        from stockagent.models import TechnicalSignals
        from typing import get_type_hints

        hints = get_type_hints(TechnicalSignals)
        assert "rsi" in hints
        assert "macd" in hints

    @pytest.mark.feature001
    def test_sentiment_result_type_exists(self):
        """Test that SentimentResult type can be imported."""
        from stockagent.models import SentimentResult
        from typing import get_type_hints

        hints = get_type_hints(SentimentResult)
        assert "overall_score" in hints
        assert "overall_label" in hints
        assert "headlines" in hints


class TestDependencies:
    """Test that required dependencies are installed."""

    @pytest.mark.feature001
    def test_langgraph_importable(self):
        """Test that langgraph can be imported."""
        import langgraph

        assert langgraph is not None

    @pytest.mark.feature001
    def test_streamlit_importable(self):
        """Test that streamlit can be imported."""
        import streamlit

        assert streamlit is not None

    @pytest.mark.feature001
    def test_polygon_importable(self):
        """Test that polygon can be imported."""
        import polygon

        assert polygon is not None

    @pytest.mark.feature001
    def test_duckduckgo_search_importable(self):
        """Test that duckduckgo_search can be imported."""
        from duckduckgo_search import DDGS

        assert DDGS is not None

    @pytest.mark.feature001
    def test_pandas_importable(self):
        """Test that pandas can be imported."""
        import pandas

        assert pandas is not None

    @pytest.mark.feature001
    def test_numpy_importable(self):
        """Test that numpy can be imported."""
        import numpy

        assert numpy is not None

    @pytest.mark.feature001
    def test_dotenv_importable(self):
        """Test that python-dotenv can be imported."""
        from dotenv import load_dotenv

        assert load_dotenv is not None
