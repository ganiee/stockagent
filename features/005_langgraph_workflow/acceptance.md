# Feature 005: Acceptance Criteria

## Required Outcomes

### AC-1: Module Imports Successfully
- [ ] `from stockagent.graph import create_workflow, run_analysis` works
- [ ] `from stockagent.graph.workflow import fetch_data, technical_analysis, news_sentiment` works

### AC-2: Workflow Creates Successfully
- [ ] `create_workflow()` returns a compiled StateGraph
- [ ] Graph has all expected nodes: fetch_data, technical_analysis, news_sentiment, synthesize, recommend
- [ ] Graph compiles without errors

### AC-3: run_analysis Returns Complete State
- [ ] `run_analysis("AAPL")` returns StockAnalysisState dict
- [ ] State contains populated fields:
  - `ticker`: "AAPL"
  - `price_data`: non-empty list
  - `company_name`: contains "Apple"
  - `current_price`: float > 0
  - `previous_close`: float > 0
  - `technical_signals`: dict with indicators
  - `news_sentiment`: dict with score and headlines
  - `synthesis`: string (placeholder OK)
  - `recommendation`: string (placeholder OK)
  - `confidence`: float (placeholder OK)

### AC-4: Error Handling Works
- [ ] Invalid ticker → state.errors contains error message
- [ ] Partial failure → other fields still populated
- [ ] No crashes on any input

### AC-5: Parallel Execution Works
- [ ] technical_analysis and news_sentiment can run concurrently
- [ ] Both complete before synthesize runs

### AC-6: State Transitions Correct
- [ ] After fetch_data: price_data populated
- [ ] After technical_analysis: technical_signals populated
- [ ] After news_sentiment: news_sentiment populated
- [ ] After synthesize: synthesis field populated
- [ ] After recommend: recommendation and confidence populated

## Observable Outcomes

1. Full workflow execution completes in < 15 seconds
2. All nodes execute in correct order
3. Final state contains all expected data
4. Errors are captured, not raised

## Automated Tests

All acceptance criteria are validated by automated tests in `tests/test_005_langgraph_workflow.py`.

Run tests with:
```bash
pytest -m feature005 -v
```

Expected: 20 tests pass.

### Test Coverage

| AC | Test Class | Tests |
|----|-----------|-------|
| AC-1 | TestWorkflowImports | test_create_workflow_import, test_run_analysis_import, test_node_functions_import |
| AC-2 | TestCreateWorkflow | test_create_workflow_returns_compiled_graph, test_workflow_compiles_without_error |
| AC-3 | TestRunAnalysis | test_run_analysis_returns_complete_state |
| AC-4 | TestFetchDataNode, TestRunAnalysis | test_fetch_data_with_no_ticker, test_fetch_data_handles_api_error, test_run_analysis_accumulates_errors |
| AC-5 | TestWorkflowIntegration | test_workflow_state_flows_through_nodes |
| AC-6 | TestFetchDataNode, TestTechnicalAnalysisNode, TestNewsSentimentNode, TestPlaceholderNodes | Various state transition tests |
