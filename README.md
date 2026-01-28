# StockAgent

An AI-powered stock analysis tool that combines technical indicators, news sentiment analysis, and a scoring engine to generate actionable Buy/Sell/Hold recommendations.

## Overview

StockAgent is a LangGraph-based workflow that analyzes individual stocks using:

- **Technical Indicators**: RSI, MACD, Bollinger Bands, and Moving Averages (SMA 20/50/200)
- **News Sentiment**: Keyword-based sentiment analysis of recent news headlines
- **Scoring Engine**: Weighted composite scoring system that combines all signals
- **Report Generation**: Comprehensive markdown reports with analysis details

The application features a Streamlit web interface for easy interaction.

## Features

- Real-time stock data from Polygon.io API
- Technical analysis with multiple indicators
- News sentiment analysis via DuckDuckGo search
- Weighted scoring system (-100 to +100)
- Recommendations: STRONG BUY, BUY, HOLD, SELL, STRONG SELL
- Confidence scores based on signal strength
- Detailed markdown reports
- Interactive Streamlit UI

## Architecture

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ fetch_data  │  ← Polygon.io API (price data, company details)
└──────┬──────┘
       │
       ├────────────────┐
       ▼                ▼
┌─────────────┐  ┌─────────────────┐
│  technical  │  │ news_sentiment  │  ← Parallel execution
│  analysis   │  │                 │
└──────┬──────┘  └────────┬────────┘
       │                  │
       └────────┬─────────┘
                ▼
        ┌─────────────┐
        │  recommend  │  ← Scoring engine
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │  synthesize │  ← Report generation
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │     END     │
        └─────────────┘
```

## Installation

### Prerequisites

- Python 3.11+
- Polygon.io API key (free tier available at https://polygon.io)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stockagent
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Polygon.io API key:
   ```
   POLYGON_API_KEY=your_api_key_here
   ```

## Usage

### Web Interface (Streamlit)

Run the Streamlit app:

```bash
PYTHONPATH=src streamlit run src/stockagent/ui/app.py
```

Open your browser to `http://localhost:8501` and:
1. Enter a stock ticker (e.g., AAPL, MSFT, GOOGL)
2. Click "Run Analysis"
3. View results in the Summary, Technical Data, and News Headlines tabs

### Programmatic Usage

```python
from stockagent.graph import run_analysis

# Run analysis for a stock
result = run_analysis("AAPL")

# Access results
print(f"Recommendation: {result['recommendation']}")
print(f"Confidence: {result['confidence']:.1f}%")
print(f"Current Price: ${result['current_price']:.2f}")

# Get the full report
print(result['synthesis'])
```

### CLI Quick Test

```bash
PYTHONPATH=src python -c "
from stockagent.graph import run_analysis
result = run_analysis('AAPL')
print(f\"Recommendation: {result['recommendation']} ({result['confidence']:.0f}% confidence)\")
"
```

## Project Structure

```
stockagent/
├── src/stockagent/
│   ├── analysis/           # Analysis modules
│   │   ├── indicators.py   # Technical indicators (RSI, MACD, etc.)
│   │   ├── scoring.py      # Recommendation scoring engine
│   │   ├── news_sentiment.py  # News sentiment analysis
│   │   └── synthesis.py    # Report generation
│   ├── data/
│   │   └── polygon_client.py  # Polygon.io API client
│   ├── graph/
│   │   └── workflow.py     # LangGraph workflow definition
│   ├── ui/
│   │   └── app.py          # Streamlit web interface
│   ├── config.py           # Configuration management
│   └── models.py           # Data models and type definitions
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── test_*.py          # Feature tests
├── features/              # Feature specifications
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── pyproject.toml        # Project configuration
```

## Technical Indicators

| Indicator | Description | Bullish Signal | Bearish Signal |
|-----------|-------------|----------------|----------------|
| RSI (14) | Relative Strength Index | < 30 (oversold) | > 70 (overbought) |
| MACD | Moving Average Convergence Divergence | Positive histogram | Negative histogram |
| Bollinger Bands | Volatility bands | Price near lower band | Price near upper band |
| SMA 20/50/200 | Simple Moving Averages | Price above all SMAs | Price below all SMAs |

## Scoring System

The scoring engine combines signals into a composite score (-100 to +100):

| Component | Weight | Max Contribution |
|-----------|--------|------------------|
| RSI | 20% | ±20 points |
| MACD | 25% | ±25 points |
| Moving Averages | 20% | ±20 points |
| Bollinger Bands | 15% | ±15 points |
| News Sentiment | 20% | ±20 points |

### Recommendation Thresholds

| Score Range | Recommendation |
|-------------|----------------|
| > 60 | STRONG BUY |
| 20 to 60 | BUY |
| -20 to 20 | HOLD |
| -60 to -20 | SELL |
| < -60 | STRONG SELL |

## Running Tests

```bash
# Run all tests
pytest -v

# Run tests for a specific feature
pytest -m feature001 -v

# Run with coverage
pytest --cov=src/stockagent --cov-report=term-missing
```

## Rate Limits

The free Polygon.io tier has the following limits:
- 5 API calls per minute
- Historical data limited to 2 years
- Data is delayed (not real-time)

## Disclaimer

This tool is for **educational and informational purposes only** and does not constitute financial advice. The analysis is based on historical data and automated algorithms, which may not accurately predict future performance.

- Past performance is not indicative of future results
- Always conduct your own research before making investment decisions
- Consider consulting a qualified financial advisor

## License

MIT License

## Acknowledgments

- Market data provided by [Polygon.io](https://polygon.io)
- News headlines sourced via DuckDuckGo Search
- Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Streamlit](https://streamlit.io)
