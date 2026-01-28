# Product Requirements Document: StockAgent

**Version:** 1.0
**Status:** Draft
**Date:** 2026-01-27

---

## 1. Overview & Problem Statement

### Product Name
StockAgent

### Problem Statement
Individual investors and developers lack a straightforward tool to quickly analyze a stock's technical health and market sentiment without navigating multiple platforms or relying on expensive subscriptions. Existing solutions either:
- Provide raw data without actionable insights
- Use AI-generated/hallucinated financial data (unreliable)
- Lack transparency in how recommendations are derived
- Are too complex for quick decision-making

### Solution
StockAgent is an educational stock analysis tool that:
- Fetches **real market data** from Polygon.io (no hallucinated prices)
- Computes standard technical indicators using transparent math
- Aggregates news headlines and derives sentiment scores
- Orchestrates analysis through a stateful LangGraph workflow
- Presents results in an explainable, actionable format via Streamlit UI
- Outputs a clear Buy/Sell/Hold recommendation with confidence score and full rationale

### Disclaimer
This is an **educational tool**, not financial advice. It does not execute trades or manage portfolios.

---

## 2. Goals & Non-Goals

### Goals (v1)
1. Provide accurate technical analysis using real market data from Polygon.io
2. Aggregate recent news and compute sentiment scores
3. Generate explainable Buy/Sell/Hold recommendations with confidence levels
4. Present analysis in a clean, usable Streamlit dashboard
5. Maintain modular architecture for future frontend/backend migration
6. Ensure deterministic, repeatable calculations for the same input data

### Non-Goals (v1)
1. **Not a trading bot** — no order placement or broker integration
2. **Not portfolio management** — no multi-ticker scanning or portfolio tracking
3. **Not backtesting** — no historical strategy simulation
4. **Not real-time streaming** — on-demand analysis only
5. **Not LLM-generated prices** — all financial data comes from Polygon.io
6. **Not mobile-optimized** — desktop Streamlit experience only
7. **Not production trading advice** — educational purposes only

---

## 3. Target Users & Use Cases

### Target Users

| User Type | Description |
|-----------|-------------|
| Individual Investor | Wants quick technical checks before making investment decisions |
| Software Engineer | Building or learning agentic workflow patterns with LangGraph |
| Data/ML Practitioner | Exploring stateful pipeline architectures |
| Finance Student | Learning technical analysis concepts with real data |

### Primary Use Cases

**UC-1: Quick Stock Analysis**
> As an individual investor, I want to enter a ticker symbol and receive a comprehensive analysis (technical indicators, news sentiment, recommendation) so I can make informed decisions quickly.

**UC-2: Understanding Technical Signals**
> As a finance student, I want to see how RSI, MACD, and other indicators are calculated and interpreted so I can learn technical analysis concepts.

**UC-3: Workflow Development Reference**
> As a software engineer, I want to examine a well-structured LangGraph workflow so I can learn patterns for building my own agentic applications.

---

## 4. Functional Requirements

### FR-1: Stock Data Retrieval
- Fetch historical price data (OHLCV) for a given ticker
- Retrieve current/previous close price
- Fetch basic company information (name, sector)
- Handle invalid tickers gracefully with user-friendly errors

### FR-2: Technical Indicator Calculation
- **RSI (Relative Strength Index)** — 14-period default
- **MACD (Moving Average Convergence Divergence)** — standard 12/26/9 parameters
- **Bollinger Bands** — 20-period with 2 standard deviations
- **Moving Averages** — SMA 20, 50, 200
- All calculations must be deterministic and use standard formulas

### FR-3: News Sentiment Analysis
- Fetch recent news headlines for the ticker via DuckDuckGo Search
- Apply keyword-based sentiment scoring (positive/negative/neutral)
- Compute aggregate sentiment score (-1.0 to +1.0 scale)
- Display individual headlines with sentiment tags

### FR-4: Workflow Orchestration
- Implement stateful workflow using LangGraph
- Define clear state transitions between analysis phases
- Support parallel execution where dependencies allow
- Capture and propagate errors without crashing

### FR-5: Recommendation Engine
- Combine technical signals and sentiment into a composite score
- Map score to recommendation: STRONG BUY / BUY / HOLD / SELL / STRONG SELL
- Calculate confidence level (0-100%)
- Provide explanation factors for the recommendation

### FR-6: Report Generation
- Generate markdown-formatted analysis report
- Include timestamp and data sources
- Display all indicator values with interpretations
- Show recommendation rationale

### FR-7: User Interface
- Text input for ticker symbol
- Quick-select buttons for popular tickers
- "Run Analysis" action button
- Display current price and day change
- Show recommendation with confidence prominently
- Tabbed interface for detailed views (Report, Technical Data, News)

### FR-8: Error Handling
- Validate API key presence at startup
- Handle rate limits gracefully (Polygon free tier)
- Display user-friendly error messages (not stack traces)
- Continue analysis with partial data when possible

---

## 5. Non-Functional Requirements

### NFR-1: Performance
- Complete full analysis in <15 seconds on Polygon free tier
- UI remains responsive during analysis (show progress)

### NFR-2: Reliability
- No crashes on invalid input or missing data
- Graceful degradation when external services are unavailable
- Errors displayed in UI, not silent failures

### NFR-3: Maintainability
- Modular code structure with clear separation of concerns
- Each component independently testable
- Configuration externalized (environment variables)

### NFR-4: Extensibility
- Architecture supports future React frontend replacement
- Backend logic decoupled from Streamlit UI
- Data layer abstracted for potential provider changes

### NFR-5: Security
- API keys stored in environment variables, never in code
- No sensitive data logged or displayed
- Input validation on all user inputs

### NFR-6: Testability
- Pure functions for indicator calculations
- Mock-friendly API client design
- State objects serializable for snapshot testing

---

## 6. System Architecture (High-Level)

### Component Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI                             │
│  (Ticker Input, Metrics Display, Tabbed Results)                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Workflow                           │
│  (State Machine: fetch → analyze → synthesize → recommend)      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────────┐ ┌───────────────┐ ┌───────────────────┐
│   Data Layer    │ │Analysis Layer │ │  Synthesis Layer  │
│ (Polygon Client)│ │(Indicators,   │ │ (Report Builder,  │
│                 │ │ Sentiment)    │ │  Recommender)     │
└────────┬────────┘ └───────────────┘ └───────────────────┘
         │
         ▼
┌─────────────────┐ ┌───────────────┐
│  Polygon.io API │ │ DuckDuckGo    │
│  (Market Data)  │ │ (News Search) │
└─────────────────┘ └───────────────┘
```

### Workflow State Machine

```
START
  │
  ▼
[fetch_data] ─────────────────────────────────┐
  │                                           │
  ▼                                           │
[technical_analysis] ◄──── parallel ────► [news_sentiment]
  │                                           │
  └─────────────────────┬─────────────────────┘
                        ▼
                  [synthesize]
                        │
                        ▼
                  [recommend]
                        │
                        ▼
                       END
```

### State Object Structure

```
StockAnalysisState:
  ├── input
  │     └── ticker: str
  ├── fetched
  │     ├── price_data: list[OHLCV]
  │     ├── company_name: str
  │     ├── current_price: float
  │     └── previous_close: float
  ├── computed
  │     ├── technical_signals: TechnicalSignals
  │     └── news_sentiment: SentimentResult
  ├── output
  │     ├── synthesis: str (markdown)
  │     ├── recommendation: str
  │     └── confidence: float
  └── errors: list[str]
```

---

## 7. Data Sources & Constraints

### Polygon.io (Market Data)

| Endpoint | Purpose | Rate Limit (Free Tier) |
|----------|---------|------------------------|
| Aggregates | Historical OHLCV bars | 5 calls/minute |
| Ticker Details | Company info | 5 calls/minute |
| Previous Close | Latest close price | 5 calls/minute |

**Constraints:**
- Free tier: 5 API calls per minute
- Historical data: Limited to 2 years on free tier
- Delayed data (not real-time) on free tier
- Requires API key (free registration)

### DuckDuckGo Search (News)

| Method | Purpose | Constraints |
|--------|---------|-------------|
| News Search | Recent headlines | No API key required |

**Constraints:**
- No official API (uses duckduckgo-search library)
- Rate limiting may apply with heavy usage
- Results quality varies by ticker popularity
- No guaranteed freshness of results

---

## 8. UX Requirements (Streamlit v1)

### Layout Structure

```
┌────────────────────────────────────────────────────────────┐
│  StockAgent - Stock Analysis Tool                          │
├────────────────────────────────────────────────────────────┤
│  [Ticker Input: ________] [AAPL] [MSFT] [GOOGL] [TSLA]     │
│                                                            │
│  [ Run Analysis ]                                          │
├────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │  Price   │ │   RSI    │ │Sentiment │ │Recommendation│   │
│  │ $150.25  │ │   45.2   │ │  +0.35   │ │   BUY (75%)  │   │
│  │  +1.2%   │ │ Neutral  │ │ Positive │ │              │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘│
├────────────────────────────────────────────────────────────┤
│  [Full Report] [Technical Data] [News Headlines]           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                                                      │  │
│  │  (Tab content area)                                  │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────┤
│  Disclaimer: Educational tool only, not financial advice   │
└────────────────────────────────────────────────────────────┘
```

### Interaction Flow
1. User enters ticker or clicks quick-select button
2. Current price loads immediately (if available)
3. User clicks "Run Analysis"
4. Progress indicator shown during analysis
5. Results populate metrics row and tabs
6. User can switch tabs to explore details

### Error States
- Invalid ticker: "Ticker not found. Please check the symbol."
- API key missing: "Polygon API key not configured. See setup instructions."
- Rate limited: "API rate limit reached. Please wait and try again."
- Network error: "Unable to fetch data. Check your connection."

---

## 9. Out of Scope / Future Ideas

### Explicitly Out of Scope for v1
- Multiple ticker comparison
- Portfolio tracking and management
- Real-time price streaming
- Trade execution or broker integration
- Mobile app or responsive design
- User accounts or saved analyses
- Custom indicator parameters
- Backtesting or historical simulation
- Alerts or notifications
- Social sharing features

### Future Ideas (Post-v1)
- **React Frontend Migration** — Replace Streamlit with React SPA
- **TypeScript Backend** — Port Python logic to TypeScript
- **Multi-ticker Analysis** — Compare multiple stocks
- **Watchlists** — Save and monitor favorite tickers
- **Historical Analysis** — View past analyses
- **Custom Indicators** — User-defined technical indicators
- **LLM Integration** — AI-generated narrative summaries
- **Backtesting Module** — Test strategies against historical data
- **Export Reports** — PDF/CSV export functionality

---

## 10. Success Metrics

### Functional Success Criteria
| Metric | Target | Measurement |
|--------|--------|-------------|
| Data Accuracy | 100% match with Polygon source | Manual verification |
| Indicator Correctness | Match standard formulas | Unit tests with known values |
| Workflow Completion | No crashes on valid input | End-to-end testing |
| Error Handling | All error types show user message | Manual testing |

### Quality Success Criteria
| Metric | Target | Measurement |
|--------|--------|-------------|
| Analysis Time | <15 seconds | Stopwatch measurement |
| Code Coverage | >80% for core logic | pytest-cov |
| Determinism | Same input = same output | Repeated runs |
| Modularity | Each layer independently testable | Code review |

### User Experience Success Criteria
| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to First Analysis | <30 seconds from launch | Manual testing |
| Learning Curve | Usable without documentation | User testing |
| Error Recovery | Clear path to resolution | User testing |

---

## Appendix: Glossary

| Term | Definition |
|------|------------|
| RSI | Relative Strength Index - momentum oscillator (0-100) |
| MACD | Moving Average Convergence Divergence - trend indicator |
| Bollinger Bands | Volatility bands around moving average |
| SMA | Simple Moving Average |
| OHLCV | Open, High, Low, Close, Volume - price bar data |
| LangGraph | Framework for building stateful AI workflows |
| Polygon.io | Financial data API provider |

---

*End of PRD*