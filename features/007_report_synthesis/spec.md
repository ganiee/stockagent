# Feature 007: Report Synthesis

## Purpose

Generate a comprehensive, human-readable markdown report that synthesizes all analysis results into a single document. The report provides transparency into how the recommendation was derived.

## Inputs / Outputs

### Inputs
- Complete StockAnalysisState with all fields populated
- Ticker, company name, prices
- Technical signals with interpretations
- News sentiment with headlines
- Recommendation with confidence and factors

### Outputs
- `generate_report(state: StockAnalysisState) -> str` — Full markdown report

## Boundaries & Non-Goals

### In Scope
- Markdown-formatted report with sections:
  - Header with ticker, company, timestamp
  - Price summary (current, previous close, change)
  - Technical analysis section with indicator values and interpretations
  - News sentiment section with score and top headlines
  - Recommendation section with confidence and explanation factors
  - Disclaimer footer
- Include all indicator values in table format
- Include timestamp and data source attribution

### Non-Goals
- No PDF generation
- No chart/visualization generation
- No historical report storage
- No custom report templates

## Dependencies

- **Feature 001**: Uses StockAnalysisState structure
- **Feature 003**: Technical signals format
- **Feature 004**: Sentiment result format
- **Feature 006**: Recommendation and factors
- **Feature 005**: Will be integrated into workflow's synthesize node

## PRD References

- Section 4: FR-6 Report Generation
- Section 8: UX Requirements (tabbed display includes Full Report)
