# Feature 008: Rollback

## Files This Feature Touches

### Created Files
- `src/stockagent/ui/app.py`

### Modified Files
- `src/stockagent/ui/__init__.py` (may add imports)

## Rollback Instructions

### Option 1: Git Revert (Recommended)
```bash
# Find the commit hash for feature 008
git log --oneline | head -5

# Revert the specific commit
git revert <commit-hash> --no-edit
```

### Option 2: Manual Removal
```bash
# Remove the app module
rm src/stockagent/ui/app.py

# Reset ui/__init__.py to empty
echo "" > src/stockagent/ui/__init__.py
```

## Dependencies

- **Feature 009** depends on this feature (tests may include UI tests)
- Rolling back will remove the user interface
- Backend (features 001-007) will still work via Python API

## Verification After Rollback
```bash
# Verify file removed
[ ! -f src/stockagent/ui/app.py ] && echo "app.py removed"

# Verify streamlit run fails (expected)
streamlit run src/stockagent/ui/app.py 2>&1 | grep -q "No such file" && echo "App correctly removed"

# Verify backend still works
python -c "
from stockagent.graph import run_analysis
result = run_analysis('AAPL')
print(f'Backend still works: {result.get(\"recommendation\")}')
"
```
