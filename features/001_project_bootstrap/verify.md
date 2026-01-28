# Feature 001: Verification

## Local Commands to Run

### 1. Verify Directory Structure
```bash
ls -la src/stockagent/
ls -la src/stockagent/data/
ls -la src/stockagent/analysis/
ls -la src/stockagent/graph/
ls -la src/stockagent/ui/
ls -la src/stockagent/utils/
```

Expected: All directories exist with `__init__.py` files.

### 2. Verify Dependencies Install
```bash
source venv/bin/activate
pip install -r requirements.txt
echo $?
```

Expected: Exit code 0 (success).

### 3. Verify Package Imports
```bash
python -c "
import langgraph
import streamlit
import polygon
from duckduckgo_search import DDGS
import pandas
import numpy
from dotenv import load_dotenv
print('All imports successful')
"
```

Expected: "All imports successful" printed.

### 4. Verify Config Module
```bash
# First, create a test .env file
cp .env.example .env
echo "POLYGON_API_KEY=test_key_123" > .env

# Test config loading
python -c "
from stockagent.config import load_config
config = load_config()
assert 'POLYGON_API_KEY' in config
print(f'Config loaded: {list(config.keys())}')
"
```

Expected: Config loaded message with POLYGON_API_KEY in keys.

### 5. Verify Config Error Handling
```bash
# Remove .env to test error handling
rm .env

python -c "
from stockagent.config import load_config
try:
    load_config()
    print('ERROR: Should have raised ValueError')
except ValueError as e:
    print(f'Correct error raised: {e}')
"
```

Expected: "Correct error raised:" with descriptive message.

### 6. Verify Models Module
```bash
python -c "
from stockagent.models import StockAnalysisState
from typing import get_type_hints
hints = get_type_hints(StockAnalysisState)
print(f'StockAnalysisState fields: {list(hints.keys())}')
"
```

Expected: List of all state fields printed.

## Quick Verification (All-in-One)
```bash
source venv/bin/activate && \
pip install -r requirements.txt -q && \
python -c "
from stockagent.config import load_config
from stockagent.models import StockAnalysisState
print('Feature 001 verification: PASSED')
"
```

## Run Automated Tests (Recommended)
```bash
# Run all feature 001 tests
pytest -m feature001 -v

# Or use the feature test script
python scripts/run_feature_tests.py 001

# Run with coverage
pytest -m feature001 --cov=src/stockagent --cov-report=term-missing
```

Expected: All 18 tests pass.
