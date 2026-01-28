# Feature 007: Rollback

## Files This Feature Touches

### Created Files
- `src/stockagent/analysis/synthesis.py`

### Modified Files
- `src/stockagent/analysis/__init__.py` (adds exports)
- `src/stockagent/graph/workflow.py` (updates synthesize node)

## Rollback Instructions

### Option 1: Git Revert (Recommended)
```bash
# Find the commit hash for feature 007
git log --oneline | head -5

# Revert the specific commit
git revert <commit-hash> --no-edit
```

### Option 2: Manual Removal
```bash
# Remove the synthesis module
rm src/stockagent/analysis/synthesis.py

# Edit analysis/__init__.py to remove synthesis exports
# (Keep indicators, news_sentiment, scoring exports)

# Restore workflow.py synthesize node to placeholder
# (Manual edit required)
```

## Dependencies

- **Feature 008** depends on this feature (UI displays the report)
- Rolling back will require updating workflow.py to use placeholder synthesize node
- UI will show empty/placeholder report after rollback

## Verification After Rollback
```bash
# Verify file removed
[ ! -f src/stockagent/analysis/synthesis.py ] && echo "synthesis.py removed"

# Verify import fails (expected)
python -c "from stockagent.analysis.synthesis import generate_report" 2>&1 | grep -q "No module" && echo "Import correctly fails"

# Verify workflow still runs (with placeholder)
python -c "
from stockagent.graph import run_analysis
result = run_analysis('AAPL')
print(f'Workflow runs, synthesis: {result.get(\"synthesis\", \"<empty>\")}')
"
```
