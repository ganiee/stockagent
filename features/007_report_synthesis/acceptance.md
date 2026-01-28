# Feature 007: Acceptance Criteria

## Required Outcomes

### AC-1: Module Imports Successfully
- [ ] `from stockagent.analysis import generate_report` works
- [ ] `from stockagent.analysis.synthesis import generate_report` works

### AC-2: Report Contains All Sections
- [ ] Report contains header with ticker and timestamp
- [ ] Report contains price summary section
- [ ] Report contains technical analysis section
- [ ] Report contains news sentiment section
- [ ] Report contains recommendation section
- [ ] Report contains disclaimer

### AC-3: Report is Valid Markdown
- [ ] Report renders correctly in markdown viewer
- [ ] Headings are properly formatted (##, ###)
- [ ] Tables are properly formatted
- [ ] Bullet lists are properly formatted

### AC-4: Technical Section Shows All Indicators
- [ ] RSI value and interpretation displayed
- [ ] MACD values (line, signal, histogram) displayed
- [ ] Bollinger Bands (upper, middle, lower) displayed
- [ ] Moving averages (20, 50, 200) displayed
- [ ] "N/A" or similar for missing indicators

### AC-5: Sentiment Section Shows Headlines
- [ ] Overall score and label displayed
- [ ] At least one headline listed (if available)
- [ ] Individual sentiment tags on headlines
- [ ] Graceful handling of no headlines

### AC-6: Recommendation Section is Clear
- [ ] Recommendation is prominent/bold
- [ ] Confidence percentage shown
- [ ] At least one explanation factor listed
- [ ] Easy to scan quickly

### AC-7: Timestamp and Attribution Present
- [ ] Report includes generation timestamp
- [ ] Polygon.io credited as data source
- [ ] Disclaimer clearly states educational purpose

### AC-8: Workflow Integration Works
- [ ] `run_analysis()` returns populated synthesis field
- [ ] Synthesis is a non-empty markdown string

## Observable Outcomes

1. Report is readable and well-organized
2. All relevant data from analysis is included
3. User can understand recommendation rationale
4. Report can be displayed in Streamlit markdown widget

## Automated Tests

All acceptance criteria are validated by automated tests in `tests/test_007_report_synthesis.py`.

Run tests with:
```bash
pytest -m feature007 -v
```

Expected: 46 tests pass.

### Test Coverage

| AC | Test Class | Tests |
|----|-----------|-------|
| AC-1 | TestSynthesisImports | test_generate_report_import_from_synthesis, test_generate_report_import_from_analysis |
| AC-2 | TestGenerateReport | test_generate_report_contains_all_sections |
| AC-3 | TestGenerateReport, TestTechnicalSection | test_generate_report_valid_markdown, test_technical_section_is_markdown_table |
| AC-4 | TestTechnicalSection | test_technical_section_shows_rsi, test_technical_section_shows_macd, test_technical_section_shows_bollinger, test_technical_section_shows_smas, test_technical_section_handles_none_values |
| AC-5 | TestSentimentSection | test_sentiment_section_shows_headlines, test_sentiment_section_shows_headline_tags, test_sentiment_section_handles_no_headlines |
| AC-6 | TestRecommendationSection | test_recommendation_section_shows_recommendation, test_recommendation_section_is_bold, test_recommendation_section_shows_confidence, test_recommendation_section_shows_factors |
| AC-7 | TestReportHeader, TestDisclaimer | test_header_contains_timestamp, test_disclaimer_credits_polygon, test_disclaimer_contains_educational_warning |
| AC-8 | TestWorkflowIntegration | test_synthesize_returns_report, test_synthesize_not_placeholder, test_run_analysis_returns_populated_synthesis |
