# Feature 002: Rollback

## Files This Feature Touches

### Created Files
- `src/stockagent/data/polygon_client.py`

### Modified Files
- `src/stockagent/data/__init__.py` (adds exports)

## Rollback Instructions

### Option 1: Git Revert (Recommended)
```bash
# Find the commit hash for feature 002
git log --oneline | head -5

# Revert the specific commit
git revert <commit-hash> --no-edit
```

### Option 2: Manual Removal
```bash
# Remove the polygon client module
rm src/stockagent/data/polygon_client.py

# Reset data/__init__.py to empty
echo "" > src/stockagent/data/__init__.py
```

## Dependencies

- **Feature 003** depends on this feature (uses price data for indicators)
- **Feature 005** depends on this feature (LangGraph fetch_data node)
- Rolling back this feature will break features 003, 005, and all subsequent features

## Verification After Rollback
```bash
# Verify file removed
[ ! -f src/stockagent/data/polygon_client.py ] && echo "polygon_client.py removed"

# Verify import fails (expected)
python -c "from stockagent.data import PolygonClient" 2>&1 | grep -q "cannot import" && echo "Import correctly fails"
```
