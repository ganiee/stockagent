# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

StockAgent is a LangGraph-based stock analysis agent that analyzes individual stocks using Polygon.io market data, technical indicators, and news sentiment. It provides Buy/Sell/Hold recommendations with confidence scores via a Streamlit UI.

**Status:** Early development - PRD exists in `docs/prd.md`, implementation follows feature-based development.

## Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (once requirements.txt exists)
pip install -r requirements.txt

# Run Streamlit UI
streamlit run src/stockagent/ui/app.py

# Run CLI analysis
python -m stockagent

# Run tests (once implemented)
python -m pytest
```

## Environment Setup

Requires `POLYGON_API_KEY` in `.env` file. Copy `.env.example` and add your key.

## Architecture

### LangGraph Workflow
```
fetch_data → [parallel: technical_analysis, news_sentiment] → synthesize → recommend → end
```

### State Object
`StockAnalysisState` TypedDict with fields:
- **input:** ticker symbol
- **fetched:** price_data, company_name, current_price, fundamental_data
- **computed:** technical_signals, news_sentiment
- **output:** synthesis, recommendation, confidence
- **errors:** list of error messages

### Module Structure
- `src/stockagent/data/polygon_client.py` - Polygon.io API wrapper (aggregates, ticker details, previous close)
- `src/stockagent/analysis/` - Technical indicators (RSI, MACD, Bollinger, MAs) and news sentiment
- `src/stockagent/graph/workflow.py` - LangGraph state machine
- `src/stockagent/ui/app.py` - Streamlit entry point

### Technical Indicators
- RSI(14), MACD, Bollinger Bands(20), Moving Averages (20/50/200)
- All calculations use real data from Polygon, no LLM-generated prices

## Feature-Based Development

Implementation follows sequential features in `features/00x_*/`:
1. `001_project_bootstrap` - Skeleton, config, placeholder UI
2. `002_polygon_client` - Data integration with rate limiting
3. `003_indicators` - Technical analysis math
4. `004_langgraph_workflow` - State machine wiring
5. `005_news_sentiment` - DuckDuckGo news + keyword sentiment
6. `006_synthesis_and_recommendation` - Report generation + scoring thresholds
7. `007_streamlit_app` - Full UI with tabs
8. `008_tests_and_quality` - pytest, formatting

Each feature folder contains `spec.md`, `tasks.md`, and `acceptance.md`.

## Key Dependencies

- LangGraph for workflow orchestration
- Streamlit for UI
- Polygon.io SDK for market data
- duckduckgo-search for news headlines
- pandas/numpy for indicator calculations
