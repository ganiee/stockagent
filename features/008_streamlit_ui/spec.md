# Feature 008: Streamlit UI

## Purpose

Implement the full Streamlit user interface that allows users to input a ticker, run analysis, and view results. This is the primary user-facing component of StockAgent.

## Inputs / Outputs

### Inputs (User)
- Ticker symbol via text input or quick-select buttons
- "Run Analysis" button click

### Outputs (Display)
- Current price and day change
- Metrics row: Price, RSI, Sentiment, Recommendation
- Tabbed interface: Full Report, Technical Data, News Headlines
- Error messages when applicable
- Progress indicator during analysis

## Boundaries & Non-Goals

### In Scope
- Streamlit app entry point (`src/stockagent/ui/app.py`)
- Text input for ticker symbol
- Quick-select buttons for popular tickers (AAPL, MSFT, GOOGL, TSLA)
- "Run Analysis" button
- Metrics row with 4 columns
- Three tabs: Full Report (markdown), Technical Data (JSON), News Headlines
- Session state management
- Progress spinner during analysis
- Error display (user-friendly, not stack traces)
- Disclaimer footer

### Non-Goals
- No user authentication
- No saved/history of analyses
- No custom indicator parameters
- No mobile-responsive design
- No charts/visualizations (v1)

## Dependencies

- **Feature 005**: Uses `run_analysis()` function
- **Feature 006**: Recommendation and confidence for display
- **Feature 007**: Synthesis markdown for Full Report tab

## PRD References

- Section 4: FR-7 User Interface
- Section 8: UX Requirements (layout structure, interaction flow, error states)
