# Feature 008: Acceptance Criteria

## Required Outcomes

### AC-1: App Launches Successfully
- [ ] `streamlit run src/stockagent/ui/app.py` starts without errors
- [ ] Browser opens to app URL
- [ ] Page title shows "StockAgent"

### AC-2: Ticker Input Works
- [ ] Text input field visible and functional
- [ ] Can type ticker symbol
- [ ] Quick-select buttons visible (AAPL, MSFT, GOOGL, TSLA)
- [ ] Clicking quick-select updates input field

### AC-3: Analysis Runs Successfully
- [ ] "Run Analysis" button visible
- [ ] Clicking button with valid ticker starts analysis
- [ ] Progress spinner shown during analysis
- [ ] Results appear after analysis completes

### AC-4: Metrics Row Displays Correctly
- [ ] 4 metrics visible in row
- [ ] Price shows current value and delta (change)
- [ ] RSI shows value and interpretation
- [ ] Sentiment shows score and label
- [ ] Recommendation shows value and confidence

### AC-5: Tabs Work Correctly
- [ ] 3 tabs visible: Full Report, Technical Data, News Headlines
- [ ] Full Report tab shows markdown-rendered report
- [ ] Technical Data tab shows JSON data
- [ ] News Headlines tab shows list of headlines
- [ ] Switching tabs works without page reload

### AC-6: Error Handling Works
- [ ] Invalid ticker shows error message
- [ ] Error message is user-friendly (not stack trace)
- [ ] App doesn't crash on errors
- [ ] Can retry with different ticker after error

### AC-7: Session State Persists
- [ ] Results remain after interacting with tabs
- [ ] Changing ticker clears previous results
- [ ] Analysis doesn't re-run on tab switch

### AC-8: Disclaimer Present
- [ ] Disclaimer visible at bottom of page
- [ ] States educational purpose
- [ ] Not financial advice warning

## Observable Outcomes

1. Complete user flow: enter ticker → click analyze → view results
2. All analysis data visible in UI
3. Errors handled gracefully
4. Responsive during analysis (spinner visible)
