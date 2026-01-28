# Feature Index

This is the **authoritative control file** for tracking implementation progress of StockAgent.

**PRD Reference:** [docs/PRD.md](../docs/PRD.md)

---

## Feature Status Table

| ID | Feature Name | Status | Summary | Spec | Tasks | Acceptance | Verify | Rollback |
|----|--------------|--------|---------|------|-------|------------|--------|----------|
| 001 | project_bootstrap | Planned | Project structure, config, dependencies | [spec](001_project_bootstrap/spec.md) | [tasks](001_project_bootstrap/tasks.md) | [acceptance](001_project_bootstrap/acceptance.md) | [verify](001_project_bootstrap/verify.md) | [rollback](001_project_bootstrap/rollback.md) |
| 002 | polygon_client | Planned | Polygon.io API client for market data | [spec](002_polygon_client/spec.md) | [tasks](002_polygon_client/tasks.md) | [acceptance](002_polygon_client/acceptance.md) | [verify](002_polygon_client/verify.md) | [rollback](002_polygon_client/rollback.md) |
| 003 | technical_indicators | Planned | RSI, MACD, Bollinger Bands, Moving Averages | [spec](003_technical_indicators/spec.md) | [tasks](003_technical_indicators/tasks.md) | [acceptance](003_technical_indicators/acceptance.md) | [verify](003_technical_indicators/verify.md) | [rollback](003_technical_indicators/rollback.md) |
| 004 | news_sentiment | Planned | DuckDuckGo news search + sentiment scoring | [spec](004_news_sentiment/spec.md) | [tasks](004_news_sentiment/tasks.md) | [acceptance](004_news_sentiment/acceptance.md) | [verify](004_news_sentiment/verify.md) | [rollback](004_news_sentiment/rollback.md) |
| 005 | langgraph_workflow | Planned | LangGraph state machine orchestration | [spec](005_langgraph_workflow/spec.md) | [tasks](005_langgraph_workflow/tasks.md) | [acceptance](005_langgraph_workflow/acceptance.md) | [verify](005_langgraph_workflow/verify.md) | [rollback](005_langgraph_workflow/rollback.md) |
| 006 | recommendation_engine | Planned | Scoring system and recommendation logic | [spec](006_recommendation_engine/spec.md) | [tasks](006_recommendation_engine/tasks.md) | [acceptance](006_recommendation_engine/acceptance.md) | [verify](006_recommendation_engine/verify.md) | [rollback](006_recommendation_engine/rollback.md) |
| 007 | report_synthesis | Planned | Markdown report generation | [spec](007_report_synthesis/spec.md) | [tasks](007_report_synthesis/tasks.md) | [acceptance](007_report_synthesis/acceptance.md) | [verify](007_report_synthesis/verify.md) | [rollback](007_report_synthesis/rollback.md) |
| 008 | streamlit_ui | Planned | Full Streamlit user interface | [spec](008_streamlit_ui/spec.md) | [tasks](008_streamlit_ui/tasks.md) | [acceptance](008_streamlit_ui/acceptance.md) | [verify](008_streamlit_ui/verify.md) | [rollback](008_streamlit_ui/rollback.md) |
| 009 | tests_and_quality | Planned | pytest tests and quality checks | [spec](009_tests_and_quality/spec.md) | [tasks](009_tests_and_quality/tasks.md) | [acceptance](009_tests_and_quality/acceptance.md) | [verify](009_tests_and_quality/verify.md) | [rollback](009_tests_and_quality/rollback.md) |

---

## Status Legend

- **Planned** — Feature designed, not yet implemented
- **In Progress** — Currently being implemented
- **Done** — Implementation complete and verified

---

## Dependency Graph

```
001_project_bootstrap
         │
         ▼
002_polygon_client
         │
         ▼
003_technical_indicators
         │
         ├──────────────────┐
         ▼                  ▼
004_news_sentiment    (parallel path)
         │                  │
         └────────┬─────────┘
                  ▼
005_langgraph_workflow
         │
         ▼
006_recommendation_engine
         │
         ▼
007_report_synthesis
         │
         ▼
008_streamlit_ui
         │
         ▼
009_tests_and_quality
```

---

## Notes

- Features must be implemented in order (001 → 009)
- Each feature is independently reversible via its rollback.md
- Update this file when starting/completing each feature
