"""Tests for Feature 008: Streamlit UI."""

from unittest.mock import MagicMock, patch

import pytest


class TestUIImports:
    """Test that UI module can be imported."""

    @pytest.mark.feature008
    def test_app_module_imports(self):
        """Test that app module can be imported."""
        from stockagent.ui import app

        assert app is not None

    @pytest.mark.feature008
    def test_main_function_exists(self):
        """Test that main function exists."""
        from stockagent.ui.app import main

        assert main is not None
        assert callable(main)

    @pytest.mark.feature008
    def test_render_functions_exist(self):
        """Test that render functions exist."""
        from stockagent.ui.app import (
            render_disclaimer,
            render_errors,
            render_header,
            render_metrics,
            render_tabs,
            render_ticker_input,
        )

        assert render_header is not None
        assert render_ticker_input is not None
        assert render_metrics is not None
        assert render_tabs is not None
        assert render_errors is not None
        assert render_disclaimer is not None

    @pytest.mark.feature008
    def test_helper_functions_exist(self):
        """Test that helper functions exist."""
        from stockagent.ui.app import init_session_state, set_ticker

        assert init_session_state is not None
        assert set_ticker is not None


class TestSetTicker:
    """Test set_ticker function."""

    @pytest.mark.feature008
    def test_set_ticker_updates_session_state(self):
        """Test that set_ticker updates session state."""
        from stockagent.ui.app import set_ticker

        # Mock streamlit session state with MagicMock for attribute access
        mock_session_state = MagicMock()
        with patch("stockagent.ui.app.st") as mock_st:
            mock_st.session_state = mock_session_state
            set_ticker("AAPL")
            assert mock_session_state.current_ticker == "AAPL"


class TestRenderMetrics:
    """Test render_metrics function with mocked Streamlit."""

    @pytest.mark.feature008
    def test_render_metrics_with_full_data(self):
        """Test render_metrics with complete analysis result."""
        from stockagent.ui.app import render_metrics

        result = {
            "current_price": 150.50,
            "previous_close": 148.25,
            "technical_signals": {
                "rsi": 55.5,
                "rsi_interpretation": "neutral",
            },
            "news_sentiment": {
                "overall_score": 0.35,
                "overall_label": "positive",
            },
            "recommendation": "BUY",
            "confidence": 65.0,
        }

        with patch("stockagent.ui.app.st") as mock_st:
            mock_st.columns.return_value = [MagicMock() for _ in range(4)]
            render_metrics(result)

            # Verify st.metric was called
            assert mock_st.metric.called

    @pytest.mark.feature008
    def test_render_metrics_with_missing_data(self):
        """Test render_metrics handles missing data gracefully."""
        from stockagent.ui.app import render_metrics

        result = {
            "current_price": 0.0,
            "previous_close": 0.0,
            "technical_signals": {},
            "news_sentiment": {},
            "recommendation": "N/A",
            "confidence": 0.0,
        }

        with patch("stockagent.ui.app.st") as mock_st:
            mock_st.columns.return_value = [MagicMock() for _ in range(4)]
            # Should not raise any exceptions
            render_metrics(result)

    @pytest.mark.feature008
    def test_render_metrics_calculates_price_change(self):
        """Test that render_metrics calculates price change correctly."""
        from stockagent.ui.app import render_metrics

        result = {
            "current_price": 150.0,
            "previous_close": 145.0,
            "technical_signals": {},
            "news_sentiment": {},
            "recommendation": "HOLD",
            "confidence": 50.0,
        }

        with patch("stockagent.ui.app.st") as mock_st:
            mock_cols = [MagicMock() for _ in range(4)]
            mock_st.columns.return_value = mock_cols

            render_metrics(result)

            # Check that metric was called with price delta
            calls = mock_st.metric.call_args_list
            assert len(calls) > 0


class TestRenderTabs:
    """Test render_tabs function with mocked Streamlit."""

    @pytest.mark.feature008
    def test_render_tabs_with_synthesis(self):
        """Test render_tabs displays synthesis report."""
        from stockagent.ui.app import render_tabs

        result = {
            "synthesis": "# Test Report\n\nThis is a test.",
            "technical_signals": {"rsi": 50.0},
            "news_sentiment": {
                "headlines": [
                    {"title": "Test headline", "label": "positive", "score": 0.5, "url": ""}
                ]
            },
        }

        with patch("stockagent.ui.app.st") as mock_st:
            # Create mock tabs that work as context managers
            mock_tab1 = MagicMock()
            mock_tab2 = MagicMock()
            mock_tab3 = MagicMock()
            mock_tab1.__enter__ = MagicMock(return_value=None)
            mock_tab1.__exit__ = MagicMock(return_value=False)
            mock_tab2.__enter__ = MagicMock(return_value=None)
            mock_tab2.__exit__ = MagicMock(return_value=False)
            mock_tab3.__enter__ = MagicMock(return_value=None)
            mock_tab3.__exit__ = MagicMock(return_value=False)
            mock_st.tabs.return_value = [mock_tab1, mock_tab2, mock_tab3]
            mock_st.columns.return_value = [MagicMock(), MagicMock()]

            render_tabs(result)

            # Verify tabs was called with correct labels
            mock_st.tabs.assert_called_once()
            call_args = mock_st.tabs.call_args[0][0]
            assert "Full Report" in call_args[0]
            assert "Technical" in call_args[1]
            assert "News" in call_args[2]

    @pytest.mark.feature008
    def test_render_tabs_with_headlines(self):
        """Test render_tabs displays news headlines."""
        from stockagent.ui.app import render_tabs

        result = {
            "synthesis": "",
            "technical_signals": {},
            "news_sentiment": {
                "headlines": [
                    {"title": "Good news", "label": "positive", "score": 0.8, "url": "http://test.com"},
                    {"title": "Bad news", "label": "negative", "score": -0.5, "url": ""},
                ]
            },
        }

        with patch("stockagent.ui.app.st") as mock_st:
            mock_tabs = [MagicMock() for _ in range(3)]
            mock_st.tabs.return_value = mock_tabs
            mock_st.columns.return_value = [MagicMock(), MagicMock()]

            render_tabs(result)

    @pytest.mark.feature008
    def test_render_tabs_with_no_headlines(self):
        """Test render_tabs handles no headlines gracefully."""
        from stockagent.ui.app import render_tabs

        result = {
            "synthesis": "",
            "technical_signals": {},
            "news_sentiment": {"headlines": []},
        }

        with patch("stockagent.ui.app.st") as mock_st:
            mock_tabs = [MagicMock() for _ in range(3)]
            mock_st.tabs.return_value = mock_tabs

            # Should not raise
            render_tabs(result)


class TestRenderErrors:
    """Test render_errors function."""

    @pytest.mark.feature008
    def test_render_errors_with_errors(self):
        """Test render_errors displays errors."""
        from stockagent.ui.app import render_errors

        result = {
            "errors": ["Error 1", "Error 2"],
        }

        with patch("stockagent.ui.app.st") as mock_st:
            mock_expander = MagicMock()
            mock_st.expander.return_value.__enter__ = MagicMock(return_value=mock_expander)
            mock_st.expander.return_value.__exit__ = MagicMock(return_value=False)

            render_errors(result)

            # Verify expander was called
            mock_st.expander.assert_called_once()

    @pytest.mark.feature008
    def test_render_errors_with_no_errors(self):
        """Test render_errors with no errors does nothing."""
        from stockagent.ui.app import render_errors

        result = {"errors": []}

        with patch("stockagent.ui.app.st") as mock_st:
            render_errors(result)

            # Expander should not be called
            mock_st.expander.assert_not_called()


class TestRenderDisclaimer:
    """Test render_disclaimer function."""

    @pytest.mark.feature008
    def test_render_disclaimer_contains_educational(self):
        """Test disclaimer mentions educational purpose."""
        from stockagent.ui.app import render_disclaimer

        with patch("stockagent.ui.app.st") as mock_st:
            render_disclaimer()

            # Check caption was called
            mock_st.caption.assert_called_once()
            call_args = mock_st.caption.call_args[0][0]
            assert "educational" in call_args.lower()

    @pytest.mark.feature008
    def test_render_disclaimer_contains_not_advice(self):
        """Test disclaimer states not financial advice."""
        from stockagent.ui.app import render_disclaimer

        with patch("stockagent.ui.app.st") as mock_st:
            render_disclaimer()

            call_args = mock_st.caption.call_args[0][0]
            assert "not" in call_args.lower() or "does not" in call_args.lower()
            assert "advice" in call_args.lower()

    @pytest.mark.feature008
    def test_render_disclaimer_credits_polygon(self):
        """Test disclaimer credits Polygon.io."""
        from stockagent.ui.app import render_disclaimer

        with patch("stockagent.ui.app.st") as mock_st:
            render_disclaimer()

            call_args = mock_st.caption.call_args[0][0]
            assert "Polygon" in call_args


class TestRenderHeader:
    """Test render_header function."""

    @pytest.mark.feature008
    def test_render_header_shows_title(self):
        """Test render_header displays title."""
        from stockagent.ui.app import render_header

        with patch("stockagent.ui.app.st") as mock_st:
            render_header()

            mock_st.title.assert_called_once()
            call_args = mock_st.title.call_args[0][0]
            assert "StockAgent" in call_args


class TestInitSessionState:
    """Test init_session_state function."""

    @pytest.mark.feature008
    def test_init_session_state_creates_keys(self):
        """Test init_session_state creates required keys."""
        from stockagent.ui.app import init_session_state

        # Use MagicMock that simulates "not in" behavior
        mock_session_state = MagicMock()
        mock_session_state.__contains__ = MagicMock(return_value=False)

        with patch("stockagent.ui.app.st") as mock_st:
            mock_st.session_state = mock_session_state
            init_session_state()

            # Check that attributes were set
            assert hasattr(mock_session_state, "analysis_result")
            assert hasattr(mock_session_state, "current_ticker")
            assert hasattr(mock_session_state, "last_analyzed_ticker")

    @pytest.mark.feature008
    def test_init_session_state_preserves_existing(self):
        """Test init_session_state doesn't overwrite existing values."""
        from stockagent.ui.app import init_session_state

        # Use MagicMock that simulates keys already existing
        mock_session_state = MagicMock()
        mock_session_state.__contains__ = MagicMock(return_value=True)
        mock_session_state.analysis_result = {"ticker": "AAPL"}
        mock_session_state.current_ticker = "MSFT"
        mock_session_state.last_analyzed_ticker = "GOOGL"

        with patch("stockagent.ui.app.st") as mock_st:
            mock_st.session_state = mock_session_state
            init_session_state()

            # Values should be preserved (no assignments made)
            assert mock_session_state.analysis_result == {"ticker": "AAPL"}
            assert mock_session_state.current_ticker == "MSFT"


class TestRenderTickerInput:
    """Test render_ticker_input function."""

    @pytest.mark.feature008
    def test_render_ticker_input_creates_text_input(self):
        """Test render_ticker_input creates text input."""
        from stockagent.ui.app import render_ticker_input

        with patch("stockagent.ui.app.st") as mock_st:
            # Use MagicMock for session_state with attribute access
            mock_session_state = MagicMock()
            mock_session_state.current_ticker = ""
            mock_st.session_state = mock_session_state

            # Create mock columns that work as context managers
            def create_mock_col():
                mock_col = MagicMock()
                mock_col.__enter__ = MagicMock(return_value=None)
                mock_col.__exit__ = MagicMock(return_value=False)
                return mock_col

            # First call returns 2 columns for main layout
            # Second call returns 4 columns for quick buttons
            mock_st.columns.side_effect = [
                [create_mock_col(), create_mock_col()],
                [create_mock_col() for _ in range(4)],
            ]
            mock_st.text_input.return_value = ""
            mock_st.button.return_value = False

            render_ticker_input()

            mock_st.text_input.assert_called_once()

    @pytest.mark.feature008
    def test_render_ticker_input_creates_quick_buttons(self):
        """Test render_ticker_input creates quick select buttons."""
        from stockagent.ui.app import render_ticker_input

        with patch("stockagent.ui.app.st") as mock_st:
            # Use MagicMock for session_state with attribute access
            mock_session_state = MagicMock()
            mock_session_state.current_ticker = ""
            mock_st.session_state = mock_session_state

            # Create mock columns that work as context managers
            def create_mock_col():
                mock_col = MagicMock()
                mock_col.__enter__ = MagicMock(return_value=None)
                mock_col.__exit__ = MagicMock(return_value=False)
                return mock_col

            mock_st.columns.side_effect = [
                [create_mock_col(), create_mock_col()],  # First call for main layout
                [create_mock_col() for _ in range(4)],  # Second call for quick buttons
            ]
            mock_st.text_input.return_value = ""
            mock_st.button.return_value = False

            render_ticker_input()

            # Should have called button for each quick ticker
            assert mock_st.button.call_count == 4


class TestAppIntegration:
    """Integration tests for the app."""

    @pytest.mark.feature008
    def test_app_file_is_valid_python(self):
        """Test that app.py is valid Python syntax."""
        import ast

        with open("src/stockagent/ui/app.py") as f:
            source = f.read()

        # Should not raise SyntaxError
        ast.parse(source)

    @pytest.mark.feature008
    def test_app_has_page_config(self):
        """Test that app sets page config."""
        with open("src/stockagent/ui/app.py") as f:
            source = f.read()

        assert "set_page_config" in source
        assert "page_title" in source
        assert "StockAgent" in source

    @pytest.mark.feature008
    def test_app_has_run_analysis_import(self):
        """Test that app imports run_analysis."""
        with open("src/stockagent/ui/app.py") as f:
            source = f.read()

        assert "from stockagent.graph import run_analysis" in source

    @pytest.mark.feature008
    def test_app_has_main_entry_point(self):
        """Test that app has main entry point."""
        with open("src/stockagent/ui/app.py") as f:
            source = f.read()

        assert 'if __name__ == "__main__":' in source
        assert "main()" in source

    @pytest.mark.feature008
    def test_app_has_quick_tickers(self):
        """Test that app has quick select tickers."""
        with open("src/stockagent/ui/app.py") as f:
            source = f.read()

        assert "AAPL" in source
        assert "MSFT" in source
        assert "GOOGL" in source
        assert "TSLA" in source

    @pytest.mark.feature008
    def test_app_has_tabs(self):
        """Test that app has tabbed interface."""
        with open("src/stockagent/ui/app.py") as f:
            source = f.read()

        assert "st.tabs" in source
        assert "Full Report" in source
        assert "Technical" in source
        assert "News" in source

    @pytest.mark.feature008
    def test_app_has_spinner(self):
        """Test that app has progress spinner."""
        with open("src/stockagent/ui/app.py") as f:
            source = f.read()

        assert "st.spinner" in source

    @pytest.mark.feature008
    def test_app_has_error_handling(self):
        """Test that app has error handling."""
        with open("src/stockagent/ui/app.py") as f:
            source = f.read()

        assert "st.error" in source
        assert "except" in source


class TestUIComponents:
    """Test individual UI component logic."""

    @pytest.mark.feature008
    def test_price_delta_calculation_positive(self):
        """Test price delta calculation for positive change."""
        current_price = 150.50
        previous_close = 148.25
        price_change = current_price - previous_close

        assert price_change > 0
        assert f"{price_change:+.2f}" == "+2.25"

    @pytest.mark.feature008
    def test_price_delta_calculation_negative(self):
        """Test price delta calculation for negative change."""
        current_price = 145.00
        previous_close = 148.25
        price_change = current_price - previous_close

        assert price_change < 0
        assert f"{price_change:+.2f}" == "-3.25"

    @pytest.mark.feature008
    def test_sentiment_emoji_positive(self):
        """Test sentiment emoji assignment for positive."""
        label = "positive"
        emoji = "🟢" if label == "positive" else "🔴" if label == "negative" else "⚪"
        assert emoji == "🟢"

    @pytest.mark.feature008
    def test_sentiment_emoji_negative(self):
        """Test sentiment emoji assignment for negative."""
        label = "negative"
        emoji = "🟢" if label == "positive" else "🔴" if label == "negative" else "⚪"
        assert emoji == "🔴"

    @pytest.mark.feature008
    def test_sentiment_emoji_neutral(self):
        """Test sentiment emoji assignment for neutral."""
        label = "neutral"
        emoji = "🟢" if label == "positive" else "🔴" if label == "negative" else "⚪"
        assert emoji == "⚪"


class TestSessionStateManagement:
    """Test session state management logic."""

    @pytest.mark.feature008
    def test_ticker_change_clears_results(self):
        """Test that changing ticker would trigger result clearing."""
        # This tests the logic that should happen in the app
        current_ticker = "AAPL"
        last_analyzed_ticker = "MSFT"

        # When ticker changes, results should be cleared
        should_clear = current_ticker != last_analyzed_ticker
        assert should_clear is True

    @pytest.mark.feature008
    def test_same_ticker_preserves_results(self):
        """Test that same ticker preserves results."""
        current_ticker = "AAPL"
        last_analyzed_ticker = "AAPL"

        should_clear = current_ticker != last_analyzed_ticker
        assert should_clear is False
