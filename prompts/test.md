We are working in repo `stockagent` on WSL Ubuntu with an active venv.

GOAL:
Create a pytest-based testing system that:
1) Has tests mapped to EACH feature
2) Forces tests to be created/updated whenever a feature is implemented
3) Ensures tests can be run automatically as part of acceptance criteria
4) Keeps tests stable and not flaky (no uncontrolled network calls)

IMPORTANT CONTEXT:
- We have a feature plan under features/
- We have a control file: features/FEATURE_INDEX.md
- Each feature folder contains spec.md, tasks.md, acceptance.md, verify.md, rollback.md
- Implementation is done one feature at a time
- After each feature is implemented, FEATURE_INDEX.md must be updated (status + links + verify + rollback)
- We use Polygon.io and DuckDuckGo; external calls must be mocked in tests

STRICT RULES:
- DO NOT implement any new product features in this run.
- You MAY create test infrastructure + test files + minimal tooling that supports test execution.
- Tests must NOT depend on live Polygon or DuckDuckGo network access.
- Use mocking (pytest monkeypatch or requests_mock) for external HTTP calls.
- Deterministic tests only.

WHAT YOU MUST DELIVER:
A) Testing Architecture
- Create a `tests/` directory with feature-aligned structure, e.g.:
  tests/
    test_001_project_bootstrap/
    test_002_polygon_client/
    test_003_indicators/
    ...
- OR a single tests/ with naming convention that clearly maps tests to features (you decide).
- Add pytest configuration (pyproject.toml or pytest.ini) to make running easy.
- Add a single command to run everything:
  `pytest -q`

B) Feature Test Contract (very important)
- Update *each* feature’s docs so that:
  - features/00X_*/acceptance.md includes running the relevant tests for that feature
  - features/00X_*/verify.md includes exact test commands
- Update `features/FEATURE_INDEX.md`:
  - Add/standardize Verify Command column entries to include pytest commands per feature
  - Ensure every feature has a test target command (even if minimal for early features)

C) Tests to Create (minimum expectations)
1) Feature 001 bootstrap:
   - test that config loader reads env var safely (monkeypatch env)
   - test that streamlit entry file exists and imports (do NOT run streamlit server)
2) Feature 002 polygon client:
   - test that polygon URL construction is correct
   - test missing API key behavior
   - test non-200 and timeout handling using mocked requests.get
3) Feature 003 indicators:
   - deterministic unit tests for RSI/MACD/Bollinger/MAs using fixed arrays
4) LangGraph workflow features:
   - test that graph compiles
   - test that invoking graph with mocked dependencies produces required keys in state
5) News sentiment:
   - test that sentiment scoring works with synthetic articles (no real DDG calls)
6) Synthesis/recommendation:
   - test that thresholds map to correct recommendation and confidence
7) Streamlit UI:
   - test that UI module imports and that key functions can be called in isolation (no server)

D) Automation for “run tests every feature”
- Add a simple script that can run:
  - all tests, or
  - tests for a single feature by feature id
Example: `python scripts/run_feature_tests.py 002`
(or a Makefile with `make test` and `make test-002`)

OUTPUT REQUIREMENTS:
At the end, print:
1) Files created/changed
2) How to run all tests
3) How to run per-feature tests
4) How the feature docs were updated to enforce tests as acceptance
5) STOP and wait for next instruction

Do not proceed beyond test infrastructure and test updates.
