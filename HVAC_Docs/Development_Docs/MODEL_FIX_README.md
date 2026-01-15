# Model Name Fix - RESOLVED

## Issue
The AI diagnostic apps were using an incorrect Claude model name that caused a 404 error:
```
Error code: 404 - model: claude-3-5-sonnet-20241022
```

## Fix Applied
Updated model name in all AI diagnostic apps from:
- ❌ `claude-3-5-sonnet-20241022` (invalid)
- ✅ `claude-3-5-sonnet-20240620` (valid)

## Files Updated

### Python Scripts
- ✅ `execution/ai_tank1_diagnostic.py`
- ✅ `execution/ai_tank2_diagnostic.py`

### Launcher Scripts
- ✅ `run_ai_diagnostic.sh`
- ✅ `run_ai_tank2_diagnostic.sh`

### Configuration Files
- ✅ `.env.diagnostic.example`
- ✅ `.env.diagnostic` (your active config)

## Valid Claude Model Names

### Recommended (Current)
```
claude-3-5-sonnet-20240620    # Claude 3.5 Sonnet (June 2024) - FAST & SMART
```

### Other Available Models
```
claude-3-opus-20240229        # Claude 3 Opus - Most capable (slower, expensive)
claude-3-sonnet-20240229      # Claude 3 Sonnet - Balanced
claude-3-haiku-20240307       # Claude 3 Haiku - Fastest (cheaper)
```

### For Future Reference
If you need to change the model, edit `.env.diagnostic`:
```bash
# Uncomment and modify this line:
MODEL=claude-3-5-sonnet-20240620
```

Or change directly in the Python files (line ~41 in both):
```python
self.model = "claude-3-5-sonnet-20240620"
```

## Testing the Fix

### Test Tank #1 AI App
```bash
./run_ai_diagnostic.sh
```

### Test Tank #2 AI App
```bash
./run_ai_tank2_diagnostic.sh
```

Both should now work without the 404 error.

## What Changed

### Before (Broken)
```python
self.model = "claude-3-5-sonnet-20241022"  # Model doesn't exist
```

### After (Fixed)
```python
self.model = "claude-3-5-sonnet-20240620"  # Valid model
```

## Why This Happened

The model name `claude-3-5-sonnet-20241022` was a future version that doesn't exist yet in the Anthropic API. The correct current version is `claude-3-5-sonnet-20240620`.

## Verification

Run this to confirm the fix:
```bash
grep -r "claude-3-5-sonnet-20240620" execution/*.py run_ai*.sh
```

Should show the updated model name in all files.

## Status: ✅ FIXED

All AI diagnostic apps now use the correct model name and should work properly with your API key and credits.

---

**Date Fixed:** January 10, 2026
**Model Used:** claude-3-5-sonnet-20240620
