PRD — StockAgent (LangGraph Stock Analysis Agent)
1) Overview

Product name: stockagent
Purpose: Analyze one stock at a time using real market data + real indicator math + news sentiment, orchestrated through a stateful LangGraph workflow, and displayed in a Streamlit UI.

Core output: Buy/Sell/Hold (plus Strong variants) + confidence score + full explainable report.

Non-goals (for v1):

Not a trading bot (no order placement)

Not portfolio / multi-ticker scanning

Not backtesting (future)

Not “LLM hallucinated” prices (all prices come from Polygon)

Disclaimer: This is educational tooling, not financial advice.

2) Target Users & Use Cases

Users

Individual investor doing quick technical checks

Engineer building an agentic workflow demo

Data/ML person testing LangGraph stateful pipelines

Primary use case

Enter ticker → run analysis → see technical indicators + news sentiment + recommendation + rationale.

3) Success Criteria

Functional

Fetches real data from Polygon for ticker

Computes RSI, MACD, Bollinger Bands, Moving Averages correctly

Pulls recent headlines and produces a basic sentiment score

Graph runs with clear state transitions

Streamlit shows results in a usable dashboard

Quality

Reliable error handling (API key missing, rate limits, invalid ticker)

Deterministic calculations (repeatable for same input data)

Minimal external dependencies; clean structure; testable

4) User Experience (v1)

Streamlit app

Input ticker (text + quick select)

Show price + day change (using prev close endpoint)

“Run Analysis” button runs LangGraph workflow

Output:

Recommendation (BUY/SELL/HOLD) + confidence

Technical details (RSI/MACD/BB/MA + derived signals)

News headlines list with per-headline sentiment tags

Full synthesized report (markdown)

5) System Architecture

Data sources

Polygon.io: aggregates, ticker details, previous close

DuckDuckGo News search: headline feed (via duckduckgo-search)

Core workflow (LangGraph)

fetch_data (Polygon calls)

parallel:

technical_analysis (indicator math)

news_sentiment (keyword-based sentiment)

synthesize

recommend

end

State object

TypedDict StockAnalysisState holding:

input (ticker)

fetched data (price_data, company_name, current_price, fundamental_data)

computed (technical_signals, news_sentiment)

output (synthesis, recommendation, confidence)

errors list

6) Requirements
6.1 Functional Requirements

Project setup

Python venv, .env support

Dependencies pinned (requirements.txt)

Polygon integration

Aggregates (90 days default)

Ticker details

Previous close

Technical indicators

RSI(14)

MACD (simplified acceptable for v1; structured output required)

Bollinger Bands(20)

Moving averages (20/50/200)

Trading signal scoring system

News sentiment

Fetch 8 results, keep top 5

Keyword-based positive/negative counts

Overall sentiment + score (-1..+1)

Synthesis report

Markdown summary with table-like formatting

Include timestamp and data sources

Recommendation

Score thresholds producing: STRONG BUY / BUY / HOLD / SELL / STRONG SELL

Confidence mapped to recommendation strength

Explanation factors appended to report

Streamlit UI

Ticker input + quick select

Metrics row: price, RSI, sentiment, recommendation+confidence

Tabs: Full report, Technical JSON, News list

6.2 Non-Functional Requirements

Performance: Typical run < ~10 seconds on free Polygon tier (rate limits handled gracefully)

Reliability: No crashes if partial data missing; errors appear in UI

Maintainability: Modular code; services isolated; easy to swap UI/backend later

Extensibility: Future migration path to TS backend + React frontend

7) Project Structure (designed for future React/TS migration)

Use a “clean boundary” layout now so later you can replace UI and/or backend.

stockagent/
  README.md
  .env.example
  .gitignore
  requirements.txt

  features/
    001_project_bootstrap/
      spec.md
      tasks.md
      acceptance.md
    002_polygon_client/
      spec.md
      tasks.md
      acceptance.md
    003_indicators/
      spec.md
      tasks.md
      acceptance.md
    004_langgraph_workflow/
      spec.md
      tasks.md
      acceptance.md
    005_news_sentiment/
      spec.md
      tasks.md
      acceptance.md
    006_synthesis_and_recommendation/
      spec.md
      tasks.md
      acceptance.md
    007_streamlit_app/
      spec.md
      tasks.md
      acceptance.md
    008_tests_and_quality/
      spec.md
      tasks.md
      acceptance.md

  src/
    stockagent/
      __init__.py

      config.py
      models.py              # TypedDict + dataclasses if needed

      data/
        polygon_client.py

      analysis/
        indicators.py
        scoring.py
        news_sentiment.py
        synthesis.py

      graph/
        workflow.py           # create_graph(), run()

      ui/
        app.py                # Streamlit entry

      utils/
        logging.py
        time.py

  scripts/
    run_cli.py               # optional CLI runner (later)

8) Acceptance Criteria (must pass before moving on)

python -m stockagent (or scripts/run_cli.py) runs end-to-end and prints report

streamlit run src/stockagent/ui/app.py works and shows results

Invalid ticker / missing API key shows friendly errors (not stack traces)

Indicators output is present even if some are neutral due to limited data

All features are isolated in their own features/00x_* folder with docs

9) Feature Breakdown (reversible, one-at-a-time)

001_project_bootstrap

Create skeleton folders, requirements.txt, .env.example, README

Add src/stockagent/config.py to load env + validate

Add basic “hello” Streamlit page placeholder

002_polygon_client

Implement Polygon client wrapper with:

get_stock_aggregates(ticker, days=90)

get_ticker_details(ticker)

get_previous_close(ticker)

Add rate-limit / non-200 handling

Add small smoke test script

003_indicators

indicators.py implements RSI, MACD, Bollinger, moving averages

Add “indicator unit tests” with fixed sample arrays

004_langgraph_workflow

Define StockAnalysisState in models.py

Implement nodes: fetch_data, technical_analysis

Wire graph edges + compile + runner

005_news_sentiment

Implement DDG news search and keyword sentiment scoring

Add node news_sentiment_node + merge into graph

006_synthesis_and_recommendation

Implement synthesis markdown builder + recommender

Add final nodes + thresholds + confidence mapping

007_streamlit_app

Full UI: input, quick picks, metrics, tabs

State stored in st.session_state

008_tests_and_quality

Add pytest, formatting (ruff/black optional)

Add CI-ish local command: make test (or python -m pytest)

Add “golden run” snapshot-like check for structure