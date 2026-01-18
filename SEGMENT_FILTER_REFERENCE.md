# Segment Filter Quick Reference

## What are Segment Filters?

Segment filters allow you to narrow down symbol searches to specific market segments, making searches faster and more accurate.

## Available Segments

| Segment Code | Description | Use For |
|--------------|-------------|---------|
| `""` (empty) | All segments | When you want all possible matches |
| `"IDX"` | Indices | NIFTY 50, BANKNIFTY, NIFTY IT, etc. |
| `"EQ"` | Equity | RELIANCE, TCS, INFY, etc. |
| `"FO"` | Futures & Options | Derivative contracts |

## Usage

### In search_charting_symbol()

```python
from Bharat_sm_data.Base.NSEBase import NSEBase

nse = NSEBase()

# Search all segments (default)
result = nse.search_charting_symbol("NIFTY")

# Search only indices
result = nse.search_charting_symbol("NIFTY", segment="IDX")

# Search only equities
result = nse.search_charting_symbol("RELIANCE", segment="EQ")

# Search only F&O
result = nse.search_charting_symbol("NIFTY", segment="FO")
```

### In get_ohlc_from_charting_v2()

```python
from datetime import datetime, timedelta

# Fetch index data with segment filter
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    symbol_type="Index",
    segment="IDX"  # Ensures we get the index, not F&O contracts
)

# Fetch equity data with segment filter
df = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="1Day",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    symbol_type="Equity",
    segment="EQ"  # Filter to equity segment only
)
```

## Why Use Segment Filters?

### Without Segment Filter
```python
result = nse.search_charting_symbol("NIFTY")
# Returns: NIFTY 50, NIFTY BANK, NIFTY FUT, NIFTY OPT, etc. (100+ results)
```

### With Segment Filter
```python
result = nse.search_charting_symbol("NIFTY", segment="IDX")
# Returns: Only NIFTY indices (10-20 results)
```

## Benefits

1. **Faster Searches** - Fewer results to process
2. **More Accurate** - Get exactly what you're looking for
3. **Avoid Confusion** - Distinguish between spot, futures, and options
4. **Better Performance** - Less data to transfer and parse

## Common Use Cases

### Use Case 1: Get Index Data (Not Derivatives)
```python
# Problem: "NIFTY" might return futures/options
# Solution: Use IDX segment
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    segment="IDX"  # Ensures spot index, not derivatives
)
```

### Use Case 2: Get Stock Data (Not Derivatives)
```python
# Problem: "RELIANCE" might return futures/options
# Solution: Use EQ segment
df = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="1Day",
    segment="EQ"  # Ensures equity, not derivatives
)
```

### Use Case 3: Find Derivative Contracts
```python
# Get all NIFTY derivative contracts
result = nse.search_charting_symbol("NIFTY", segment="FO")
for contract in result['data']:
    print(f"{contract['symbol']} - {contract['type']}")
```

### Use Case 4: Batch Processing with Filters
```python
# Process multiple indices efficiently
indices = ["NIFTY 50", "BANKNIFTY", "NIFTY IT"]

for index in indices:
    df = nse.get_ohlc_from_charting_v2(
        symbol=index,
        timeframe="1Day",
        segment="IDX"  # Filter ensures we get indices only
    )
    # Process df...
```

## Comparison Table

| Scenario | Without Filter | With Filter |
|----------|----------------|-------------|
| Search "NIFTY" | ~100+ results (all types) | ~10-20 results (specific type) |
| Search "RELIANCE" | ~50+ results (equity + F&O) | ~1-5 results (equity only) |
| Fetch time | Slower (more results) | Faster (fewer results) |
| Accuracy | May get wrong instrument | Gets exact instrument type |

## Error Handling

```python
try:
    result = nse.search_charting_symbol("NIFTY", segment="INVALID")
except ValueError as e:
    print(f"Error: {e}")
    # Output: Invalid segment 'INVALID'. Valid values are: ['', 'FO', 'IDX', 'EQ']
```

## Best Practices

1. **Always use segment filters when you know the instrument type**
   ```python
   # Good
   df = nse.get_ohlc_from_charting_v2("NIFTY 50", "1Day", segment="IDX")
   
   # Less optimal
   df = nse.get_ohlc_from_charting_v2("NIFTY 50", "1Day")
   ```

2. **Use empty segment for exploratory searches**
   ```python
   # When you're not sure what's available
   result = nse.search_charting_symbol("NIFTY", segment="")
   ```

3. **Combine with symbol_type for best results**
   ```python
   df = nse.get_ohlc_from_charting_v2(
       symbol="NIFTY 50",
       timeframe="1Day",
       symbol_type="Index",  # Tells API how to fetch data
       segment="IDX"         # Filters search results
   )
   ```

## Segment vs Symbol Type

**They serve different purposes:**

| Parameter | Purpose | Used In | Values |
|-----------|---------|---------|--------|
| `segment` | Filter search results | `search_charting_symbol()` | "", "IDX", "EQ", "FO" |
| `symbol_type` | Specify data fetch method | `get_charting_historical_data()` | "Index", "Equity" |

**Example:**
```python
# segment: Filters which symbols to search
# symbol_type: Tells API how to fetch the data

df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    segment="IDX",        # Search only indices
    symbol_type="Index"   # Fetch as index data
)
```

## Examples by Instrument Type

### Indices
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    symbol_type="Index",
    segment="IDX"
)
```

### Equities
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="1Day",
    symbol_type="Equity",
    segment="EQ"
)
```

### Futures & Options
```python
# First, search to find available contracts
result = nse.search_charting_symbol("NIFTY", segment="FO")

# Then fetch data for specific contract
# (Note: You'll need to determine the correct symbol_type and token)
```

## Testing Segment Filters

Run the comprehensive examples:
```bash
python3 SEGMENT_FILTERING_EXAMPLES.py
```

This will demonstrate:
- Searching across different segments
- Comparing result counts
- Fetching data with segment filters
- Error handling
- Advanced filtering techniques

## Summary

- Use `segment=""` for broad searches
- Use `segment="IDX"` for indices
- Use `segment="EQ"` for equities
- Use `segment="FO"` for derivatives
- Segment filters make searches faster and more accurate
- Always validate segment values (ValueError raised for invalid segments)

---

**See Also:**
- `QUICK_START_CHARTING_V2.md` - Quick start guide
- `NSE_CHARTING_V2_ANALYSIS.md` - Technical details
- `SEGMENT_FILTERING_EXAMPLES.py` - Working examples
