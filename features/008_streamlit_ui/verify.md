# Feature 008: Verification

## Prerequisites
- Features 001-007 completed
- Valid `.env` file with `POLYGON_API_KEY`

## Local Commands to Run

### 1. Verify Module Exists
```bash
ls -la src/stockagent/ui/app.py && echo "app.py exists"
```

### 2. Verify Module Imports
```bash
python -c "
import sys
sys.path.insert(0, 'src')
from stockagent.ui import app
print('Module imports successfully')
"
```

### 3. Verify Streamlit App Launches
```bash
# Run in background, check if it starts
timeout 10 streamlit run src/stockagent/ui/app.py --server.headless true 2>&1 | head -20

# Expected output should include:
# "You can now view your Streamlit app in your browser"
# or similar success message
```

### 4. Manual Verification Checklist

Launch the app:
```bash
streamlit run src/stockagent/ui/app.py
```

Then manually verify:

- [ ] **Page loads** — Title "StockAgent" visible
- [ ] **Input section** — Text input field visible
- [ ] **Quick-select** — AAPL, MSFT, GOOGL, TSLA buttons visible
- [ ] **Run button** — "Run Analysis" button visible
- [ ] **Click AAPL** — Input field updates to "AAPL"
- [ ] **Click Run Analysis** — Spinner appears
- [ ] **Analysis completes** — Metrics row appears
- [ ] **Metrics show** — Price, RSI, Sentiment, Recommendation visible
- [ ] **Tabs visible** — Full Report, Technical Data, News Headlines
- [ ] **Full Report tab** — Shows formatted markdown
- [ ] **Technical Data tab** — Shows JSON data
- [ ] **News Headlines tab** — Shows list of headlines
- [ ] **Disclaimer** — Visible at bottom

### 5. Verify Error Handling (Manual)

```bash
streamlit run src/stockagent/ui/app.py
```

Then:
1. Enter "INVALIDXYZ123" as ticker
2. Click "Run Analysis"
3. Verify: Error message appears (not stack trace)
4. Verify: Can enter new ticker and retry

### 6. Verify Quick Verification Script
```bash
python -c "
# Verify all required imports work
from stockagent.graph import run_analysis
from stockagent.analysis import generate_report

# Verify analysis still works (for UI to use)
result = run_analysis('AAPL')
assert result.get('synthesis') is not None
assert result.get('recommendation') is not None
print('Backend for UI: PASSED')
"
```

## Quick Verification Summary

1. `streamlit run src/stockagent/ui/app.py` launches without error
2. Can complete full analysis flow in browser
3. All UI elements match PRD wireframe
4. Errors display user-friendly messages

## Note

Streamlit UI verification is primarily manual. The automated checks verify:
- Module structure is correct
- Backend integration works
- App can start

Full UI testing requires manual browser interaction.
