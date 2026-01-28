# Feature 001: Tasks

## Implementation Checklist

### 1. Create Directory Structure
- [ ] Create `src/stockagent/` directory
- [ ] Create `src/stockagent/data/` directory
- [ ] Create `src/stockagent/analysis/` directory
- [ ] Create `src/stockagent/graph/` directory
- [ ] Create `src/stockagent/ui/` directory
- [ ] Create `src/stockagent/utils/` directory
- [ ] Create `scripts/` directory

### 2. Create Package Init Files
- [ ] Create `src/stockagent/__init__.py` with version info
- [ ] Create `src/stockagent/data/__init__.py`
- [ ] Create `src/stockagent/analysis/__init__.py`
- [ ] Create `src/stockagent/graph/__init__.py`
- [ ] Create `src/stockagent/ui/__init__.py`
- [ ] Create `src/stockagent/utils/__init__.py`

### 3. Create Configuration Module
- [ ] Create `src/stockagent/config.py`
- [ ] Implement `load_config()` function
- [ ] Load `POLYGON_API_KEY` from environment
- [ ] Validate required environment variables
- [ ] Raise clear error if API key missing

### 4. Create Models Module
- [ ] Create `src/stockagent/models.py`
- [ ] Define `StockAnalysisState` TypedDict
- [ ] Define sub-types: `OHLCV`, `TechnicalSignals`, `SentimentResult`
- [ ] Add type hints for all fields

### 5. Create Requirements File
- [ ] Create `requirements.txt` with pinned versions:
  - langgraph
  - streamlit
  - polygon-api-client
  - duckduckgo-search
  - pandas
  - numpy
  - python-dotenv

### 6. Create Environment Template
- [ ] Create `.env.example` with:
  - `POLYGON_API_KEY=your_api_key_here`

### 7. Verify Installation
- [ ] Run `pip install -r requirements.txt`
- [ ] Verify all imports work
- [ ] Verify config loading works

## Order of Steps

1. Directory structure (task 1)
2. Init files (task 2)
3. Models module (task 4) — defines state types
4. Config module (task 3) — may use models
5. Requirements file (task 5)
6. Environment template (task 6)
7. Verify installation (task 7)
