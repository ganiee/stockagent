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
