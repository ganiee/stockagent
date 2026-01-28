# Feature 001: Acceptance Criteria

## Required Outcomes

### AC-1: Directory Structure Exists
- [ ] `src/stockagent/` directory exists
- [ ] All subdirectories exist: `data/`, `analysis/`, `graph/`, `ui/`, `utils/`
- [ ] All `__init__.py` files exist

### AC-2: Dependencies Install Successfully
- [ ] `pip install -r requirements.txt` completes without errors
- [ ] All required packages are importable:
  ```python
  import langgraph
  import streamlit
  import polygon
  from duckduckgo_search import DDGS
  import pandas
  import numpy
  from dotenv import load_dotenv
  ```

### AC-3: Configuration Module Works
- [ ] `from stockagent.config import load_config` imports successfully
- [ ] With valid `.env` file, `load_config()` returns config dict with `POLYGON_API_KEY`
- [ ] Without `.env` or missing key, `load_config()` raises `ValueError` with clear message

### AC-4: Models Module Works
- [ ] `from stockagent.models import StockAnalysisState` imports successfully
- [ ] `StockAnalysisState` is a valid TypedDict with all required fields:
  - `ticker: str`
  - `price_data: list`
  - `company_name: str`
  - `current_price: float`
  - `previous_close: float`
  - `technical_signals: dict`
  - `news_sentiment: dict`
  - `synthesis: str`
  - `recommendation: str`
  - `confidence: float`
  - `errors: list`

### AC-5: Environment Template Exists
- [ ] `.env.example` file exists in project root
- [ ] Contains `POLYGON_API_KEY=your_api_key_here`

## Observable Outcomes

1. Running `ls src/stockagent/` shows all expected directories
2. Running `pip freeze | grep -E "langgraph|streamlit|polygon|pandas|numpy"` shows installed packages
3. Python REPL can import all modules without errors
4. Missing API key produces human-readable error, not stack trace

## Automated Tests

Run feature 001 tests:
```bash
pytest -m feature001 -v
```

Or using the feature test script:
```bash
python scripts/run_feature_tests.py 001
```

All 18 tests in `tests/test_001_project_bootstrap.py` must pass.
