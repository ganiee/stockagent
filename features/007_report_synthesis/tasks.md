# Feature 007: Tasks

## Implementation Checklist

### 1. Create Synthesis Module
- [ ] Create `src/stockagent/analysis/synthesis.py`
- [ ] Import datetime for timestamps

### 2. Implement Header Section
- [ ] Create `_generate_header(ticker: str, company_name: str) -> str`
- [ ] Include report title with ticker
- [ ] Include company name
- [ ] Include generation timestamp (UTC)
- [ ] Format as markdown heading

### 3. Implement Price Summary Section
- [ ] Create `_generate_price_summary(state: dict) -> str`
- [ ] Show current price with currency formatting
- [ ] Show previous close
- [ ] Calculate and show price change (absolute and percentage)
- [ ] Color-code direction (green/red indicators in text)

### 4. Implement Technical Analysis Section
- [ ] Create `_generate_technical_section(technical_signals: dict) -> str`
- [ ] Create markdown table with columns: Indicator, Value, Signal
- [ ] Include RSI with interpretation
- [ ] Include MACD (line, signal, histogram) with interpretation
- [ ] Include Bollinger Bands (upper, middle, lower)
- [ ] Include Moving Averages (SMA-20, SMA-50, SMA-200)
- [ ] Handle None/missing values gracefully

### 5. Implement News Sentiment Section
- [ ] Create `_generate_sentiment_section(sentiment: dict) -> str`
- [ ] Show overall sentiment score and label
- [ ] List top headlines with individual sentiment tags
- [ ] Include headline count
- [ ] Format as bullet list

### 6. Implement Recommendation Section
- [ ] Create `_generate_recommendation_section(recommendation: str, confidence: float, factors: list) -> str`
- [ ] Display recommendation prominently (bold/large)
- [ ] Show confidence percentage
- [ ] List explanation factors as bullet points
- [ ] Format for easy scanning

### 7. Implement Disclaimer Section
- [ ] Create `_generate_disclaimer() -> str`
- [ ] Standard educational disclaimer
- [ ] Not financial advice warning
- [ ] Data source attribution (Polygon.io, DuckDuckGo)

### 8. Implement Main Report Function
- [ ] Create `generate_report(state: StockAnalysisState) -> str`
- [ ] Call all section generators
- [ ] Concatenate with appropriate spacing
- [ ] Handle missing sections gracefully
- [ ] Return complete markdown string

### 9. Update Workflow
- [ ] Update `src/stockagent/graph/workflow.py` synthesize node
- [ ] Replace placeholder with `generate_report()` call
- [ ] Store result in state.synthesis

### 10. Export from Package
- [ ] Update `src/stockagent/analysis/__init__.py` to export `generate_report`

## Order of Steps

1. Create module file (task 1)
2. Implement header section (task 2)
3. Implement price summary (task 3)
4. Implement technical section (task 4)
5. Implement sentiment section (task 5)
6. Implement recommendation section (task 6)
7. Implement disclaimer (task 7)
8. Implement main function (task 8)
9. Update workflow (task 9)
10. Export from package (task 10)
