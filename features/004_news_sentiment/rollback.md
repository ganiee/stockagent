# Feature 004: Rollback

## Files This Feature Touches

### Created Files
- `src/stockagent/analysis/news_sentiment.py`

### Modified Files
- `src/stockagent/analysis/__init__.py` (adds exports)

## Rollback Instructions

### Option 1: Git Revert (Recommended)
```bash
# Find the commit hash for feature 004
git log --oneline | head -5

# Revert the specific commit
git revert <commit-hash> --no-edit
```

### Option 2: Manual Removal
```bash
# Remove the news sentiment module
rm src/stockagent/analysis/news_sentiment.py

# Edit analysis/__init__.py to remove news_sentiment exports
# (Keep indicators exports from feature 003)
```

## Dependencies

- **Feature 005** depends on this feature (news_sentiment node in workflow)
- **Feature 006** depends on this feature (uses sentiment for recommendation)
- Rolling back will break features 005, 006, and subsequent features

## Verification After Rollback
```bash
# Verify file removed
[ ! -f src/stockagent/analysis/news_sentiment.py ] && echo "news_sentiment.py removed"

# Verify import fails (expected)
python -c "from stockagent.analysis import analyze_news_sentiment" 2>&1 | grep -q "cannot import" && echo "Import correctly fails"

# Verify indicators still work (feature 003 intact)
python -c "from stockagent.analysis import calculate_all_indicators; print('Indicators still work')"
```
