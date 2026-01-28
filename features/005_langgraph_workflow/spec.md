# Feature 005: LangGraph Workflow

## Purpose

Implement the stateful workflow orchestration using LangGraph. This ties together data fetching, technical analysis, and news sentiment into a single executable graph with clear state transitions.

## Inputs / Outputs

### Inputs
- Ticker symbol (string)

### Outputs
- `create_workflow()` → Compiled LangGraph StateGraph
- `run_analysis(ticker)` → Completed StockAnalysisState with all fields populated

## Boundaries & Non-Goals

### In Scope
- Define workflow graph with nodes: fetch_data, technical_analysis, news_sentiment, synthesize, recommend
- Implement parallel execution for technical_analysis and news_sentiment
- Wire graph edges according to PRD state machine diagram
- Propagate errors in state without crashing
- Return partially complete state if some nodes fail

### Non-Goals
- No recommendation logic implementation (that's feature 006)
- No report synthesis implementation (that's feature 007)
- No UI integration (that's feature 008)
- No retry/recovery mechanisms

## Dependencies

- **Feature 001**: Uses StockAnalysisState from models.py
- **Feature 002**: Uses PolygonClient for fetch_data node
- **Feature 003**: Uses calculate_all_indicators for technical_analysis node
- **Feature 004**: Uses analyze_news_sentiment for news_sentiment node

## PRD References

- Section 4: FR-4 Workflow Orchestration
- Section 6: Workflow State Machine diagram
- Section 6: State Object Structure
