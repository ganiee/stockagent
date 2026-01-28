# Feature 005: Tasks

## Implementation Checklist

### 1. Create Workflow Module
- [ ] Create `src/stockagent/graph/workflow.py`
- [ ] Import langgraph StateGraph, START, END
- [ ] Import all required components from features 002-004

### 2. Define State Schema
- [ ] Import StockAnalysisState from models
- [ ] Ensure state schema matches PRD structure
- [ ] Add any missing fields for intermediate state

### 3. Implement fetch_data Node
- [ ] Create `fetch_data(state: StockAnalysisState) -> dict`
- [ ] Extract ticker from state
- [ ] Call PolygonClient.get_stock_aggregates()
- [ ] Call PolygonClient.get_ticker_details()
- [ ] Call PolygonClient.get_previous_close()
- [ ] Return updated state fields: price_data, company_name, current_price, previous_close
- [ ] Catch errors and append to state.errors

### 4. Implement technical_analysis Node
- [ ] Create `technical_analysis(state: StockAnalysisState) -> dict`
- [ ] Extract price_data from state
- [ ] Call calculate_all_indicators()
- [ ] Return updated state field: technical_signals
- [ ] Handle missing/insufficient data gracefully

### 5. Implement news_sentiment Node
- [ ] Create `news_sentiment(state: StockAnalysisState) -> dict`
- [ ] Extract ticker and company_name from state
- [ ] Call analyze_news_sentiment()
- [ ] Return updated state field: news_sentiment
- [ ] Handle API errors gracefully

### 6. Create Placeholder Nodes
- [ ] Create `synthesize(state: StockAnalysisState) -> dict` — placeholder, returns empty synthesis
- [ ] Create `recommend(state: StockAnalysisState) -> dict` — placeholder, returns HOLD with 50% confidence

### 7. Wire Graph Edges
- [ ] Create `create_workflow() -> CompiledGraph`
- [ ] Add all nodes to graph
- [ ] Wire edges:
  - START → fetch_data
  - fetch_data → [technical_analysis, news_sentiment] (parallel)
  - technical_analysis → synthesize
  - news_sentiment → synthesize
  - synthesize → recommend
  - recommend → END
- [ ] Compile graph

### 8. Implement Runner Function
- [ ] Create `run_analysis(ticker: str) -> StockAnalysisState`
- [ ] Initialize state with ticker
- [ ] Invoke compiled graph
- [ ] Return final state

### 9. Export from Package
- [ ] Update `src/stockagent/graph/__init__.py` to export `create_workflow`, `run_analysis`

## Order of Steps

1. Create module file (task 1)
2. Define state schema usage (task 2)
3. Implement fetch_data node (task 3)
4. Implement technical_analysis node (task 4)
5. Implement news_sentiment node (task 5)
6. Create placeholder nodes (task 6)
7. Wire graph edges (task 7)
8. Implement runner function (task 8)
9. Export from package (task 9)
