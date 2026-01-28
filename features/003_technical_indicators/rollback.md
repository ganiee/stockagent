# Feature 003: Rollback

## Files This Feature Touches

### Created Files
- `src/stockagent/analysis/indicators.py`

### Modified Files
- `src/stockagent/analysis/__init__.py` (adds exports)

## Rollback Instructions

### Option 1: Git Revert (Recommended)
```bash
# Find the commit hash for feature 003
git log --oneline | head -5

# Revert the specific commit
git revert <commit-hash> --no-edit
```

### Option 2: Manual Removal
```bash
# Remove the indicators module
rm src/stockagent/analysis/indicators.py

# Reset analysis/__init__.py to empty
echo "" > src/stockagent/analysis/__init__.py
```

## Dependencies

- **Feature 005** depends on this feature (technical_analysis node)
- **Feature 006** depends on this feature (uses indicator values for scoring)
- Rolling back will break features 005, 006, and subsequent features

## Verification After Rollback
```bash
# Verify file removed
[ ! -f src/stockagent/analysis/indicators.py ] && echo "indicators.py removed"

# Verify import fails (expected)
python -c "from stockagent.analysis import calculate_all_indicators" 2>&1 | grep -q "cannot import" && echo "Import correctly fails"
```
