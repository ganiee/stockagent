We are working in a repository called `stockagent` on WSL Ubuntu.
A Python virtualenv is already active.

AUTHORITATIVE SOURCE:
- The Product Requirements Document (PRD) is located at:
  docs/PRD.md
- The PRD is the SINGLE source of truth for scope, goals, constraints, and non-goals.

====================================================
PHASE 1: DESIGN & PLANNING ONLY (NO CODE)
====================================================

Your task in THIS RUN is to create a COMPLETE IMPLEMENTATION PLAN
based strictly on docs/PRD.md.

-------------------------
STRICT RULES (MANDATORY)
-------------------------
1. DO NOT implement any application code.
2. DO NOT create or modify files under src/stockagent.
3. DO NOT add tests, scripts, or config yet.
4. This is DESIGN + PLANNING ONLY.
5. You MUST stop after planning and wait for my instruction.

-------------------------
WHAT YOU MUST DO
-------------------------
1. Read docs/PRD.md fully.
2. Derive the full list of features required to implement the PRD (v1 only).
3. Number features sequentially starting at 001.
4. Each feature must be:
   - Independently implementable
   - Reversible without breaking others
   - Scoped to a single responsibility
5. Create a directory structure under `features/` as follows:

   features/
     FEATURE_INDEX.md
     001_<feature_name>/
       spec.md
       tasks.md
       acceptance.md
       verify.md
       rollback.md
     002_<feature_name>/
       spec.md
       tasks.md
       acceptance.md
       verify.md
       rollback.md
     ...

6. For EACH feature:
   - spec.md:
       * Purpose
       * Inputs / Outputs
       * Boundaries & non-goals
       * Dependencies on earlier features
   - tasks.md:
       * Step-by-step checklist for implementation
       * Clear ordering of steps
   - acceptance.md:
       * Clear, testable acceptance criteria
       * Observable outcomes
   - verify.md:
       * Exact local commands to run (CLI / Streamlit / pytest)
   - rollback.md:
       * Which files this feature is allowed to touch
       * How to undo it safely using git

--------------------------------------------------
FEATURE INDEX REQUIREMENT (VERY IMPORTANT)
--------------------------------------------------
Create `features/FEATURE_INDEX.md` as the SINGLE CONTROL FILE.

The index MUST contain a table with these columns:
- Feature ID
- Feature Name
- Status (Planned | In Progress | Done)
- Summary (1–2 lines)
- Spec Link
- Tasks Link
- Acceptance Link
- Verify Link
- Rollback Link

Rules for FEATURE_INDEX.md:
- All features start with Status = "Planned"
- Links must be relative paths to each file
- This file is AUTHORITATIVE for build progress

--------------------------------------------------
PROCESS RULE FOR FUTURE RUNS (BINDING)
--------------------------------------------------
You MUST follow this rule in ALL FUTURE IMPLEMENTATION RUNS:

- When I say: "Implement feature 00X"
  1. Implement ONLY that feature
  2. Update FEATURE_INDEX.md:
     - Change Status → "In Progress" at start
     - Change Status → "Done" at end
     - Fill in Summary (actual outcome)
     - Ensure Verify & Rollback sections are accurate
  3. Print:
     - Files changed
     - Verification commands
     - Rollback instructions
  4. STOP and wait for my next instruction

--------------------------------------------------
EXPECTED OUTPUT FOR THIS RUN
--------------------------------------------------
- All feature folders created
- All planning documents populated
- FEATURE_INDEX.md fully populated (Status = Planned)
- NO application code written

--------------------------------------------------
STOP CONDITION
--------------------------------------------------
After finishing planning:
- Print the ordered list of features
- Confirm explicitly: "No application code was written"
- STOP and wait for me to say:
  “Implement feature 001”

DO NOT PROCEED BEYOND PLANNING.
