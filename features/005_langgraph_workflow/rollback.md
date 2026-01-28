# Feature 005: Rollback

## Files This Feature Touches

### Created Files
- `src/stockagent/graph/workflow.py`

### Modified Files
- `src/stockagent/graph/__init__.py` (adds exports)

## Rollback Instructions

### Option 1: Git Revert (Recommended)
```bash
# Find the commit hash for feature 005
git log --oneline | head -5

# Revert the specific commit
git revert <commit-hash> --no-edit
```

### Option 2: Manual Removal
```bash
# Remove the workflow module
rm src/stockagent/graph/workflow.py

# Reset graph/__init__.py to empty
echo "" > src/stockagent/graph/__init__.py
```

## Dependencies

- **Feature 006** depends on this feature (recommendation logic)
- **Feature 007** depends on this feature (synthesis integration)
- **Feature 008** depends on this feature (UI calls run_analysis)
- Rolling back will break features 006, 007, 008, and 009

## Verification After Rollback
```bash
# Verify file removed
[ ! -f src/stockagent/graph/workflow.py ] && echo "workflow.py removed"

# Verify import fails (expected)
python -c "from stockagent.graph import run_analysis" 2>&1 | grep -q "cannot import" && echo "Import correctly fails"

# Verify features 002-004 still work (independent)
python -c "
from stockagent.data import PolygonClient
from stockagent.analysis import calculate_all_indicators, analyze_news_sentiment
print('Features 002-004 still work')
"
```
