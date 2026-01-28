We are starting a new project called `stockagent`.

Your task in THIS RUN is to generate a PRODUCT REQUIREMENTS DOCUMENT (PRD).
This is a DRAFT that I will review and approve.

--------------------------------------------------
CONTEXT
--------------------------------------------------
- Domain: Stock analysis (educational, not trading)
- Language (v1): Python
- Frameworks: LangGraph, Streamlit
- Data source: Polygon.io (real market data only)
- News source: DuckDuckGo Search
- Scope (v1): Analyze ONE stock at a time
- Output: Technical indicators + news sentiment + buy/sell/hold recommendation with confidence
- Architecture must support future migration to:
  - React frontend
  - TypeScript backend

--------------------------------------------------
STRICT RULES
--------------------------------------------------
- DO NOT write any application code.
- DO NOT define features yet.
- DO NOT create folders or files.
- This is PRD ONLY.

--------------------------------------------------
PRD MUST INCLUDE
--------------------------------------------------
1. Overview & problem statement
2. Goals & non-goals (explicit)
3. Target users & use cases
4. Functional requirements
5. Non-functional requirements
6. System architecture (high-level)
7. Data sources & constraints
8. UX requirements (Streamlit v1)
9. Out of scope / future ideas
10. Success metrics

--------------------------------------------------
STOP CONDITION
--------------------------------------------------
After writing the PRD:
- STOP
- Ask me explicitly: “Do you approve this PRD, or would you like changes?”

Do not proceed beyond PRD generation.
