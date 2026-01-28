# Feature 006: Rollback

## Files This Feature Touches

### Created Files
- `src/stockagent/analysis/scoring.py`

### Modified Files
- `src/stockagent/analysis/__init__.py` (adds exports)
- `src/stockagent/graph/workflow.py` (updates recommend node)

## Rollback Instructions

### Option 1: Git Revert (Recommended)
```bash
# Find the commit hash for feature 006
git log --oneline | head -5

# Revert the specific commit
git revert <commit-hash> --no-edit
```

### Option 2: Manual Removal
```bash
# Remove the scoring module
rm src/stockagent/analysis/scoring.py

# Edit analysis/__init__.py to remove scoring exports
# (Keep indicators and news_sentiment exports)

# Restore workflow.py recommend node to placeholder
# (Manual edit required)
```

## Dependencies

- **Feature 007** depends on this feature (report includes recommendation)
- **Feature 008** depends on this feature (UI displays recommendation)
- Rolling back will require updating workflow.py to use placeholder recommend node

## Verification After Rollback
```bash
# Verify file removed
[ ! -f src/stockagent/analysis/scoring.py ] && echo "scoring.py removed"

# Verify import fails (expected)
python -c "from stockagent.analysis.scoring import calculate_composite_score" 2>&1 | grep -q "No module" && echo "Import correctly fails"

# Verify workflow still runs (with placeholder)
python -c "
from stockagent.graph import run_analysis
result = run_analysis('AAPL')
print(f'Workflow still runs: {result.get(\"ticker\")}')
"
```
