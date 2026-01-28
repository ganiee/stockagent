# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

StockAgent is a LangGraph-based stock analysis agent that analyzes individual stocks using Polygon.io market data, technical indicators, and news sentiment. It provides Buy/Sell/Hold recommendations with confidence scores via a Streamlit UI.

**PRD:** `docs/PRD.md`
**Feature Index:** `features/FEATURE_INDEX.md` (authoritative status tracker)

## Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest -v

# Run tests for a specific feature
pytest -m feature001 -v
pytest -m feature002 -v
# ... etc

# Run tests with coverage
pytest --cov=src/stockagent --cov-report=term-missing

# Run feature tests via script
python scripts/run_feature_tests.py 001

# Run Streamlit UI (after feature 008)
streamlit run src/stockagent/ui/app.py
```

## Environment Setup

Requires `POLYGON_API_KEY` in `.env` file. Copy `.env.example` and add your key.

## Architecture

### LangGraph Workflow
```
fetch_data → [parallel: technical_analysis, news_sentiment] → synthesize → recommend → end
```

### State Object
`StockAnalysisState` TypedDict in `src/stockagent/models.py`:
- **input:** ticker symbol
- **fetched:** price_data, company_name, current_price, previous_close
- **computed:** technical_signals, news_sentiment
- **output:** synthesis, recommendation, confidence
- **errors:** list of error messages

### Module Structure
- `src/stockagent/config.py` - Configuration and API key loading
- `src/stockagent/models.py` - TypedDict definitions for state
- `src/stockagent/data/polygon_client.py` - Polygon.io API wrapper
- `src/stockagent/analysis/` - Technical indicators and news sentiment
- `src/stockagent/graph/workflow.py` - LangGraph state machine
- `src/stockagent/ui/app.py` - Streamlit entry point

### Technical Indicators
- RSI(14), MACD(12/26/9), Bollinger Bands(20), Moving Averages (20/50/200)
- All calculations use real data from Polygon, no LLM-generated prices

## Feature-Based Development

Implementation follows sequential features in `features/00x_*/`:
1. `001_project_bootstrap` - Project structure, config, models, dependencies ✓
2. `002_polygon_client` - Polygon.io API integration
3. `003_technical_indicators` - RSI, MACD, Bollinger, MAs
4. `004_news_sentiment` - DuckDuckGo news + keyword sentiment
5. `005_langgraph_workflow` - State machine wiring
6. `006_recommendation_engine` - Scoring and recommendation logic
7. `007_report_synthesis` - Markdown report generation
8. `008_streamlit_ui` - Full UI with tabs
9. `009_tests_and_quality` - Comprehensive test suite

Each feature folder contains `spec.md`, `tasks.md`, `acceptance.md`, `verify.md`, `rollback.md`.

## Testing

Tests are organized by feature with pytest markers:
- `tests/test_001_project_bootstrap.py` - Feature 001 tests
- Run with: `pytest -m feature001 -v`

All external API calls (Polygon.io, DuckDuckGo) must be mocked in tests.

## Key Dependencies

- langgraph - Workflow orchestration
- streamlit - UI framework
- polygon-api-client - Market data
- duckduckgo-search - News headlines
- pandas/numpy - Indicator calculations
- pytest/pytest-cov/pytest-mock - Testing
