# Symbol Type Update - Futures & Options Support

## What's New

Extended `symbol_type` parameter to support **Futures** and **Options** contracts in addition to Index and Equity.

## Symbol Type Values

| Value | Description | Use For | Segment |
|-------|-------------|---------|---------|
| `"Index"` | Spot indices | NIFTY 50, BANKNIFTY, NIFTY IT | IDX |
| `"Equity"` | Stocks | RELIANCE, TCS, INFY | EQ |
| `"Futures"` | Futures contracts | NIFTY FUT, RELIANCE FUT | FO |
| `"Options"` | Options contracts | NIFTY CE/PE, RELIANCE CE/PE | FO |

## Updated Methods

Both methods now support all four symbol types:

### 1. get_charting_historical_data()

**Before:**
```python
df = nse.get_charting_historical_data(
    symbol="NIFTY 50",
    token="26000",
    symbol_type="Index"  # Only Index or Equity
)
```

**After:**
```python
# Index
df = nse.get_charting_historical_data(..., symbol_type="Index")

# Equity
df = nse.get_charting_historical_data(..., symbol_type="Equity")

# Futures (NEW!)
df = nse.get_charting_historical_data(..., symbol_type="Futures")

# Options (NEW!)
df = nse.get_charting_historical_data(..., symbol_type="Options")
```

### 2. get_ohlc_from_charting_v2()

**Before:**
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    symbol_type="Index"  # Only Index or Equity
)
```

**After:**
```python
# Futures (NEW!)
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 25JAN2024 FUT",
    timeframe="1Day",
    symbol_type="Futures",
    segment="FO"
)

# Options (NEW!)
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 25JAN2024 23500 CE",
    timeframe="1Day",
    symbol_type="Options",
    segment="FO"
)
```

## Complete Examples

### Example 1: Fetch Futures Data

```python
from Bharat_sm_data.Base.NSEBase import NSEBase
from datetime import datetime, timedelta

nse = NSEBase()

# Step 1: Search for futures contracts
result = nse.search_charting_symbol("NIFTY", segment="FO")

# Step 2: Filter for futures
futures = [s for s in result['data'] if 'FUT' in s['symbol'].upper()]

# Step 3: Fetch data for a futures contract
if futures:
    df = nse.get_ohlc_from_charting_v2(
        symbol=futures[0]['symbol'],
        timeframe="1Day",
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        symbol_type="Futures",  # Specify it's a futures contract
        segment="FO"
    )
    print(df.tail())
```

### Example 2: Fetch Options Data

```python
# Step 1: Search for options contracts
result = nse.search_charting_symbol("NIFTY", segment="FO")

# Step 2: Filter for call options
calls = [s for s in result['data'] if 'CE' in s['symbol']]

# Step 3: Fetch data for a call option
if calls:
    df = nse.get_ohlc_from_charting_v2(
        symbol=calls[0]['symbol'],
        timeframe="1Day",
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        symbol_type="Options",  # Specify it's an options contract
        segment="FO"
    )
    print(df.tail())
```

### Example 3: Compare Spot vs Futures

```python
# Get spot index data
df_spot = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    symbol_type="Index",
    segment="IDX"
)

# Get futures data
result = nse.search_charting_symbol("NIFTY", segment="FO")
futures = [s for s in result['data'] if 'FUT' in s['symbol'].upper()]

df_futures = nse.get_ohlc_from_charting_v2(
    symbol=futures[0]['symbol'],
    timeframe="1Day",
    symbol_type="Futures",
    segment="FO"
)

# Calculate basis
spot_close = df_spot['close'].iloc[-1]
futures_close = df_futures['close'].iloc[-1]
basis = futures_close - spot_close
print(f"Basis: {basis:.2f} ({(basis/spot_close)*100:.2f}%)")
```

## Validation

The symbol_type parameter is now validated:

```python
try:
    df = nse.get_ohlc_from_charting_v2(
        symbol="NIFTY 50",
        timeframe="1Day",
        symbol_type="INVALID"
    )
except ValueError as e:
    print(e)
    # Output: Invalid symbol_type 'INVALID'. Valid values are: ['Index', 'Equity', 'Futures', 'Options']
```

## Workflow for Derivatives

### For Futures:
1. Search with `segment="FO"`
2. Filter results for contracts with "FUT" in symbol
3. Fetch data with `symbol_type="Futures"`

### For Options:
1. Search with `segment="FO"`
2. Filter results for contracts with "CE" (Call) or "PE" (Put) in symbol
3. Fetch data with `symbol_type="Options"`

## Symbol Type vs Segment

They work together:

| Instrument | symbol_type | segment | Example |
|------------|-------------|---------|---------|
| Spot Index | `"Index"` | `"IDX"` | NIFTY 50 |
| Stock | `"Equity"` | `"EQ"` | RELIANCE |
| Futures | `"Futures"` | `"FO"` | NIFTY 25JAN2024 FUT |
| Options | `"Options"` | `"FO"` | NIFTY 25JAN2024 23500 CE |

**Example:**
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 25JAN2024 FUT",
    timeframe="1Day",
    symbol_type="Futures",  # Tells API how to fetch data
    segment="FO"            # Filters search to F&O segment
)
```

## Backward Compatibility

✅ **Fully backward compatible** - Existing code continues to work:

```python
# Old code still works
df = nse.get_ohlc_from_charting_v2("NIFTY 50", "1Day", symbol_type="Index")
df = nse.get_ohlc_from_charting_v2("RELIANCE", "1Day", symbol_type="Equity")
```

## Documentation

### New Files:
- `DERIVATIVES_EXAMPLES.py` - 7 comprehensive examples for futures & options
- `SYMBOL_TYPE_UPDATE.md` - This file

### Updated Files:
- `Bharat_sm_data/Base/NSEBase.py` - Added validation for all 4 symbol types
- `CHARTING_V2_README.md` - Updated with futures & options examples
- `QUICK_START_CHARTING_V2.md` - Added derivatives examples
- `NSE_CHARTING_V2_ANALYSIS.md` - Updated symbol_type documentation

## Testing

Run the derivatives examples:
```bash
python3 DERIVATIVES_EXAMPLES.py
```

This demonstrates:
1. Searching for futures contracts
2. Searching for options contracts
3. Fetching futures data
4. Fetching options data
5. Comparing spot vs futures
6. Symbol type validation
7. Advanced options filtering

## Important Notes

1. **Contract Symbols**: Futures and options have specific symbol formats (e.g., "NIFTY 25JAN2024 FUT", "NIFTY 25JAN2024 23500 CE")
2. **Search First**: Always search to find exact contract symbols before fetching data
3. **Data Availability**: Not all contracts may have historical data available
4. **Expiry Dates**: Contracts expire, so recent contracts are more likely to have data
5. **Segment Filter**: Use `segment="FO"` when searching for derivatives

## Quick Reference

```python
from Bharat_sm_data.Base.NSEBase import NSEBase

nse = NSEBase()

# Valid symbol_type values
symbol_types = {
    "Index": "Spot indices",
    "Equity": "Stocks",
    "Futures": "Futures contracts",
    "Options": "Options contracts"
}

# Fetch data by type
df_index = nse.get_ohlc_from_charting_v2("NIFTY 50", "1Day", symbol_type="Index", segment="IDX")
df_equity = nse.get_ohlc_from_charting_v2("RELIANCE", "1Day", symbol_type="Equity", segment="EQ")
df_futures = nse.get_ohlc_from_charting_v2("NIFTY FUT", "1Day", symbol_type="Futures", segment="FO")
df_options = nse.get_ohlc_from_charting_v2("NIFTY CE", "1Day", symbol_type="Options", segment="FO")
```

## Best Practices

1. **Use correct symbol_type** for the instrument you're fetching
   ```python
   # Good
   df = nse.get_ohlc_from_charting_v2("NIFTY FUT", "1Day", symbol_type="Futures")
   
   # Wrong - will likely fail or return incorrect data
   df = nse.get_ohlc_from_charting_v2("NIFTY FUT", "1Day", symbol_type="Index")
   ```

2. **Combine with segment filter** for best results
   ```python
   df = nse.get_ohlc_from_charting_v2(
       symbol="NIFTY FUT",
       timeframe="1Day",
       symbol_type="Futures",
       segment="FO"  # Ensures we search in F&O segment
   )
   ```

3. **Search before fetching** to find exact contract symbols
   ```python
   # Search first
   result = nse.search_charting_symbol("NIFTY", segment="FO")
   
   # Then fetch
   df = nse.get_ohlc_from_charting_v2(
       symbol=result['data'][0]['symbol'],
       timeframe="1Day",
       symbol_type="Futures"
   )
   ```

## Summary

✅ Added support for `symbol_type="Futures"` and `symbol_type="Options"`
✅ Validation for all 4 symbol types
✅ Backward compatible
✅ Comprehensive examples for derivatives
✅ Updated documentation

The NSE Charting API v2 now supports fetching data for all instrument types: indices, equities, futures, and options!
