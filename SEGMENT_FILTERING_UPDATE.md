# Segment Filtering Feature - Update Summary

## What's New

Added support for **segment filtering** in the NSE Charting API v2 methods, allowing you to narrow down search results by market segment.

## Segment Values

| Segment | Description | Example Symbols |
|---------|-------------|-----------------|
| `""` (empty) | All segments | Everything |
| `"IDX"` | Indices only | NIFTY 50, BANKNIFTY, NIFTY IT |
| `"EQ"` | Equity only | RELIANCE, TCS, INFY |
| `"FO"` | Futures & Options | NIFTY FUT, RELIANCE OPT |

## Updated Methods

### 1. search_charting_symbol()

**Before:**
```python
result = nse.search_charting_symbol("NIFTY")
# Returns all matches (100+ results)
```

**After:**
```python
# Search only indices
result = nse.search_charting_symbol("NIFTY", segment="IDX")
# Returns only index matches (10-20 results)

# Search only equities
result = nse.search_charting_symbol("RELIANCE", segment="EQ")

# Search F&O
result = nse.search_charting_symbol("NIFTY", segment="FO")
```

### 2. get_ohlc_from_charting_v2()

**Before:**
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    symbol_type="Index"
)
```

**After:**
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    symbol_type="Index",
    segment="IDX"  # NEW: Filter to indices only
)
```

## Benefits

1. **Faster Searches** - Fewer results to process
2. **More Accurate** - Get exactly what you're looking for
3. **Avoid Confusion** - Distinguish between spot, futures, and options
4. **Better Performance** - Less data to transfer

## Example Comparison

### Without Segment Filter
```python
result = nse.search_charting_symbol("NIFTY")
print(f"Found {len(result['data'])} results")
# Output: Found 120 results
# Includes: NIFTY 50, NIFTY BANK, NIFTY FUT JAN, NIFTY FUT FEB, etc.
```

### With Segment Filter
```python
result = nse.search_charting_symbol("NIFTY", segment="IDX")
print(f"Found {len(result['data'])} results")
# Output: Found 15 results
# Includes: Only NIFTY indices (NIFTY 50, NIFTY BANK, NIFTY IT, etc.)
```

## Use Cases

### Use Case 1: Get Index Data (Not Derivatives)
```python
# Ensures you get the spot index, not futures/options
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    symbol_type="Index",
    segment="IDX"
)
```

### Use Case 2: Get Stock Data (Not Derivatives)
```python
# Ensures you get the equity, not futures/options
df = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="1Day",
    symbol_type="Equity",
    segment="EQ"
)
```

### Use Case 3: Find All Derivative Contracts
```python
# Get all NIFTY derivative contracts
result = nse.search_charting_symbol("NIFTY", segment="FO")
for contract in result['data']:
    print(f"{contract['symbol']} - Token: {contract['scripcode']}")
```

## Validation

The segment parameter is validated:
```python
try:
    result = nse.search_charting_symbol("NIFTY", segment="INVALID")
except ValueError as e:
    print(e)
    # Output: Invalid segment 'INVALID'. Valid values are: ['', 'FO', 'IDX', 'EQ']
```

## Backward Compatibility

✅ **Fully backward compatible** - The `segment` parameter is optional and defaults to `""` (all segments).

**Old code continues to work:**
```python
# This still works exactly as before
result = nse.search_charting_symbol("NIFTY")
df = nse.get_ohlc_from_charting_v2("NIFTY 50", "1Day")
```

## Documentation

New documentation files:
- `SEGMENT_FILTER_REFERENCE.md` - Complete guide to segment filtering
- `SEGMENT_FILTERING_EXAMPLES.py` - 9 working examples

Updated documentation:
- `QUICK_START_CHARTING_V2.md` - Added segment filter examples
- `NSE_CHARTING_V2_ANALYSIS.md` - Added segment parameter details
- `CHARTING_V2_README.md` - Added segment filter section
- `IMPLEMENTATION_SUMMARY.md` - Updated with segment filtering info

## Testing

Run the segment filtering examples:
```bash
python3 SEGMENT_FILTERING_EXAMPLES.py
```

This demonstrates:
1. Search all segments
2. Search index only
3. Search equity only
4. Search F&O only
5. Fetch data with segment filter
6. Compare segments
7. Equity with filter
8. Error handling
9. Advanced filtering

## Code Changes

### Modified Files
- `Bharat_sm_data/Base/NSEBase.py`
  - Updated `search_charting_symbol()` - Added segment validation
  - Updated `get_ohlc_from_charting_v2()` - Added segment parameter
  - Updated class docstring

### New Files
- `SEGMENT_FILTER_REFERENCE.md` - Complete reference guide
- `SEGMENT_FILTERING_EXAMPLES.py` - 9 comprehensive examples
- `SEGMENT_FILTERING_UPDATE.md` - This file

## Quick Reference

```python
from Bharat_sm_data.Base.NSEBase import NSEBase

nse = NSEBase()

# Segment filters
segments = {
    "": "All segments",
    "IDX": "Indices only",
    "EQ": "Equity only",
    "FO": "Futures & Options only"
}

# Search with filter
result = nse.search_charting_symbol("NIFTY", segment="IDX")

# Fetch with filter
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    symbol_type="Index",
    segment="IDX"
)
```

## Best Practices

1. **Use segment filters when you know the instrument type**
   ```python
   # Good - Fast and accurate
   df = nse.get_ohlc_from_charting_v2("NIFTY 50", "1Day", segment="IDX")
   
   # Less optimal - Slower, might get wrong instrument
   df = nse.get_ohlc_from_charting_v2("NIFTY 50", "1Day")
   ```

2. **Use empty segment for exploratory searches**
   ```python
   # When you're not sure what's available
   result = nse.search_charting_symbol("NIFTY", segment="")
   ```

3. **Combine segment with symbol_type**
   ```python
   df = nse.get_ohlc_from_charting_v2(
       symbol="NIFTY 50",
       timeframe="1Day",
       symbol_type="Index",  # How to fetch
       segment="IDX"         # What to search
   )
   ```

## Summary

✅ Added segment filtering support
✅ Backward compatible (optional parameter)
✅ Validated input (raises ValueError for invalid segments)
✅ Comprehensive documentation
✅ 9 working examples
✅ Faster and more accurate searches

The segment filtering feature makes the NSE Charting API v2 methods more powerful and easier to use, especially when dealing with symbols that exist in multiple segments (like NIFTY in both spot and derivatives).
