# Feature 008: Tasks

## Implementation Checklist

### 1. Create Streamlit App Module
- [ ] Create `src/stockagent/ui/app.py`
- [ ] Import streamlit as st
- [ ] Import run_analysis from graph module
- [ ] Configure page settings (title, icon, layout)

### 2. Implement Page Header
- [ ] Add title: "StockAgent - Stock Analysis Tool"
- [ ] Add subtitle/description
- [ ] Set page config with wide layout

### 3. Implement Ticker Input Section
- [ ] Create text input for ticker symbol
- [ ] Add placeholder text (e.g., "Enter ticker symbol (e.g., AAPL)")
- [ ] Create row of quick-select buttons: AAPL, MSFT, GOOGL, TSLA
- [ ] Quick-select updates the input field
- [ ] Store selected ticker in session state

### 4. Implement Run Analysis Button
- [ ] Create prominent "Run Analysis" button
- [ ] Disable button if no ticker entered
- [ ] On click, trigger analysis workflow

### 5. Implement Progress Indicator
- [ ] Show spinner with "Analyzing {ticker}..." during workflow
- [ ] Use st.spinner() context manager
- [ ] Hide spinner when complete

### 6. Implement Metrics Row
- [ ] Create 4-column layout
- [ ] Column 1: Current Price with day change (delta)
- [ ] Column 2: RSI with interpretation label
- [ ] Column 3: Sentiment score with label
- [ ] Column 4: Recommendation with confidence
- [ ] Use st.metric() for each
- [ ] Handle missing data gracefully

### 7. Implement Tabbed Interface
- [ ] Create 3 tabs: "Full Report", "Technical Data", "News Headlines"
- [ ] Tab 1: Display synthesis markdown using st.markdown()
- [ ] Tab 2: Display technical_signals as formatted JSON
- [ ] Tab 3: Display news headlines as list with sentiment tags

### 8. Implement Error Display
- [ ] Check for errors in analysis result
- [ ] Display errors using st.error()
- [ ] Show user-friendly messages
- [ ] Don't show raw stack traces

### 9. Implement Session State
- [ ] Store analysis results in st.session_state
- [ ] Persist results across reruns
- [ ] Clear results when ticker changes

### 10. Implement Disclaimer Footer
- [ ] Add disclaimer at bottom of page
- [ ] Use st.caption() for smaller text
- [ ] Include educational purpose statement

### 11. Add Entry Point
- [ ] Ensure app runs with `streamlit run src/stockagent/ui/app.py`
- [ ] Update `src/stockagent/ui/__init__.py` if needed

## Order of Steps

1. Create module file with page config (task 1)
2. Implement page header (task 2)
3. Implement ticker input and quick-select (task 3)
4. Implement session state (task 9)
5. Implement run button with progress (tasks 4, 5)
6. Implement metrics row (task 6)
7. Implement tabbed interface (task 7)
8. Implement error display (task 8)
9. Implement disclaimer (task 10)
10. Test entry point (task 11)
