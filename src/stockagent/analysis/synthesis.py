"""Report synthesis for stock analysis."""

from datetime import datetime, timezone
from typing import Any


def _format_price(value: float | None) -> str:
    """Format a price value with currency symbol."""
    if value is None or value == 0:
        return "N/A"
    return f"${value:,.2f}"


def _format_number(value: float | None, decimals: int = 2) -> str:
    """Format a number with specified decimal places."""
    if value is None:
        return "N/A"
    return f"{value:.{decimals}f}"


def _format_percentage(value: float | None) -> str:
    """Format a value as percentage."""
    if value is None:
        return "N/A"
    return f"{value:.1f}%"


def _generate_header(ticker: str, company_name: str) -> str:
    """Generate report header section.

    Args:
        ticker: Stock ticker symbol
        company_name: Company name

    Returns:
        Markdown header section
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""# Stock Analysis Report: {ticker}

**Company:** {company_name}
**Generated:** {timestamp}

---
"""


def _generate_price_summary(state: dict[str, Any]) -> str:
    """Generate price summary section.

    Args:
        state: StockAnalysisState dict

    Returns:
        Markdown price summary section
    """
    current_price = state.get("current_price", 0.0)
    previous_close = state.get("previous_close", 0.0)

    # Calculate change
    if current_price and previous_close:
        change = current_price - previous_close
        change_pct = (change / previous_close) * 100
        direction = "+" if change >= 0 else ""
        trend = "up" if change >= 0 else "down"
    else:
        change = 0.0
        change_pct = 0.0
        direction = ""
        trend = "unchanged"

    return f"""## Price Summary

| Metric | Value |
|--------|-------|
| Current Price | {_format_price(current_price)} |
| Previous Close | {_format_price(previous_close)} |
| Change | {direction}{_format_price(abs(change) if change else None)} ({direction}{change_pct:.2f}%) |
| Trend | {trend.capitalize()} |

"""


def _generate_technical_section(technical_signals: dict[str, Any]) -> str:
    """Generate technical analysis section.

    Args:
        technical_signals: TechnicalSignals dict

    Returns:
        Markdown technical analysis section
    """
    # Extract values
    rsi = technical_signals.get("rsi")
    rsi_interp = technical_signals.get("rsi_interpretation", "N/A")
    macd = technical_signals.get("macd")
    macd_interp = technical_signals.get("macd_interpretation", "N/A")
    bollinger = technical_signals.get("bollinger")
    sma_20 = technical_signals.get("sma_20")
    sma_50 = technical_signals.get("sma_50")
    sma_200 = technical_signals.get("sma_200")
    current_price = technical_signals.get("current_price", 0.0)

    # Format MACD values
    if macd:
        macd_line = _format_number(macd.get("macd_line"))
        signal_line = _format_number(macd.get("signal_line"))
        histogram = _format_number(macd.get("histogram"))
    else:
        macd_line = "N/A"
        signal_line = "N/A"
        histogram = "N/A"

    # Format Bollinger values
    if bollinger:
        bb_upper = _format_price(bollinger.get("upper"))
        bb_middle = _format_price(bollinger.get("middle"))
        bb_lower = _format_price(bollinger.get("lower"))
    else:
        bb_upper = "N/A"
        bb_middle = "N/A"
        bb_lower = "N/A"

    return f"""## Technical Analysis

### Momentum Indicators

| Indicator | Value | Signal |
|-----------|-------|--------|
| RSI (14) | {_format_number(rsi)} | {rsi_interp.capitalize()} |
| MACD Line | {macd_line} | {macd_interp.capitalize()} |
| MACD Signal | {signal_line} | - |
| MACD Histogram | {histogram} | - |

### Trend Indicators

| Indicator | Value |
|-----------|-------|
| SMA (20) | {_format_price(sma_20)} |
| SMA (50) | {_format_price(sma_50)} |
| SMA (200) | {_format_price(sma_200)} |
| Current Price | {_format_price(current_price)} |

### Volatility Indicators

| Bollinger Bands | Value |
|-----------------|-------|
| Upper Band | {bb_upper} |
| Middle Band | {bb_middle} |
| Lower Band | {bb_lower} |

"""


def _generate_sentiment_section(sentiment: dict[str, Any]) -> str:
    """Generate news sentiment section.

    Args:
        sentiment: SentimentResult dict

    Returns:
        Markdown sentiment section
    """
    overall_score = sentiment.get("overall_score", 0.0)
    overall_label = sentiment.get("overall_label", "neutral")
    headlines = sentiment.get("headlines", [])
    headline_count = sentiment.get("headline_count", len(headlines))

    # Build headlines list
    headlines_text = ""
    if headlines:
        for headline in headlines[:5]:  # Limit to 5 headlines
            title = headline.get("title", "")
            label = headline.get("label", "neutral")
            score = headline.get("score", 0.0)
            headlines_text += f"- {title} **[{label}]** ({score:+.2f})\n"
    else:
        headlines_text = "- No recent headlines found\n"

    return f"""## News Sentiment

**Overall Sentiment:** {overall_label.capitalize()} ({overall_score:+.2f})
**Headlines Analyzed:** {headline_count}

### Recent Headlines

{headlines_text}
"""


def _generate_recommendation_section(
    recommendation: str, confidence: float, factors: list[str]
) -> str:
    """Generate recommendation section.

    Args:
        recommendation: Recommendation string (BUY, SELL, HOLD, etc.)
        confidence: Confidence percentage (0-100)
        factors: List of explanation factors

    Returns:
        Markdown recommendation section
    """
    # Build factors list
    factors_text = ""
    if factors:
        for factor in factors:
            factors_text += f"- {factor}\n"
    else:
        factors_text = "- No specific factors identified\n"

    return f"""## Recommendation

### **{recommendation}**

**Confidence:** {confidence:.0f}%

### Contributing Factors

{factors_text}
"""


def _generate_disclaimer() -> str:
    """Generate disclaimer section.

    Returns:
        Markdown disclaimer section
    """
    return """---

## Disclaimer

This report is generated for **educational and informational purposes only** and does not constitute financial advice. The analysis is based on historical data and automated algorithms, which may not accurately predict future performance.

**Data Sources:**
- Market data provided by [Polygon.io](https://polygon.io)
- News headlines sourced via DuckDuckGo Search

**Important:**
- Past performance is not indicative of future results
- Always conduct your own research before making investment decisions
- Consider consulting a qualified financial advisor

---
*Generated by StockAgent*
"""


def generate_report(state: dict[str, Any]) -> str:
    """Generate complete markdown report from analysis state.

    Args:
        state: Complete StockAnalysisState dict

    Returns:
        Full markdown report string
    """
    ticker = state.get("ticker") or "UNKNOWN"
    company_name = state.get("company_name") or ticker
    technical_signals = state.get("technical_signals") or {}
    sentiment = state.get("news_sentiment") or {}
    recommendation = state.get("recommendation") or "HOLD"
    confidence = state.get("confidence") or 0.0
    factors = state.get("explanation_factors") or []
    errors = state.get("errors", [])

    # Build report sections
    sections = [
        _generate_header(ticker, company_name),
        _generate_price_summary(state),
        _generate_technical_section(technical_signals),
        _generate_sentiment_section(sentiment),
        _generate_recommendation_section(recommendation, confidence, factors),
    ]

    # Add errors section if any
    if errors:
        errors_text = "## Analysis Warnings\n\n"
        for error in errors:
            errors_text += f"- {error}\n"
        errors_text += "\n"
        sections.append(errors_text)

    # Add disclaimer
    sections.append(_generate_disclaimer())

    return "".join(sections)
