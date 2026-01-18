# Migration Guide: Old Charting API → New Charting API v2

## Overview

This guide helps you migrate from `get_ohlc_from_charting()` (old) to `get_ohlc_from_charting_v2()` (new).

## Why Migrate?

The new API offers:
- ✅ No need for pre-fetched mapping files
- ✅ Dynamic symbol search
- ✅ More reliable (direct from NSE charting site)
- ✅ Better error handling
- ✅ Cleaner response format

## Side-by-Side Comparison

### Old Method (Still Works)
```python
from Bharat_sm_data.Base.NSEBase import NSEBase
from datetime import datetime, timedelta

nse = NSEBase()

# Step 1: Get mappings (slow, downloads entire mapping file)
mappings = nse.get_charting_mappings()

# Step 2: Find the ticker
ticker = mappings[mappings['Symbol'] == 'NIFTY 50']['TradingSymbol'].iloc[0]

# Step 3: Fetch data
df = nse.get_ohlc_from_charting(
    ticker=ticker,  # Special ticker format
    timeframe='1Day',
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now()
)
```

### New Method (Recommended)
```python
from Bharat_sm_data.Base.NSEBase import NSEBase
from datetime import datetime, timedelta

nse = NSEBase()

# One call - that's it!
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",  # Direct symbol name
    timeframe="1Day",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    symbol_type="Index"
)
```

## Migration Examples

### Example 1: Index Data

#### Before
```python
mappings = nse.get_charting_mappings()
ticker = mappings[mappings['Symbol'] == 'NIFTY 50']['TradingSymbol'].iloc[0]
df = nse.get_ohlc_from_charting(ticker, '1Day', start_date, end_date)
```

#### After
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=start_date,
    end_date=end_date,
    symbol_type="Index"
)
```

### Example 2: Equity Stock

#### Before
```python
mappings = nse.get_charting_mappings()
ticker = mappings[mappings['Symbol'] == 'RELIANCE']['TradingSymbol'].iloc[0]
df = nse.get_ohlc_from_charting(ticker, '1Day', start_date, end_date)
```

#### After
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="1Day",
    start_date=start_date,
    end_date=end_date,
    symbol_type="Equity"  # Specify it's an equity
)
```

### Example 3: Intraday Data

#### Before
```python
mappings = nse.get_charting_mappings()
ticker = mappings[mappings['Symbol'] == 'NIFTY 50']['TradingSymbol'].iloc[0]
df = nse.get_ohlc_from_charting(ticker, '5Min', start_date, end_date)
```

#### After
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="5Min",
    start_date=start_date,
    end_date=end_date,
    symbol_type="Index"
)
```

## Parameter Mapping

| Old Parameter | New Parameter | Notes |
|---------------|---------------|-------|
| `ticker` | `symbol` | Use direct symbol name (e.g., "NIFTY 50") |
| `timeframe` | `timeframe` | Same values work |
| `start_date` | `start_date` | Same datetime object |
| `end_date` | `end_date` | Same datetime object |
| N/A | `symbol_type` | NEW: "Index" or "Equity" |

## Timeframe Values (Same in Both)

Both methods support:
- `"1Min"`, `"5Min"`, `"15Min"`, `"30Min"`, `"60Min"`
- `"1Day"`, `"1Week"`, `"1Month"`

## Output Format Comparison

### Old Method Output
```
Columns: timestamp, open, high, low, close, volume
```

### New Method Output
```
Columns: time, open, high, low, close, volume
```

**Note**: Column name changed from `timestamp` to `time`, but both are datetime objects.

## Migration Checklist

- [ ] Replace `get_ohlc_from_charting()` with `get_ohlc_from_charting_v2()`
- [ ] Change `ticker` parameter to `symbol`
- [ ] Add `symbol_type` parameter ("Index" or "Equity")
- [ ] Update column references from `timestamp` to `time` (if any)
- [ ] Remove `get_charting_mappings()` calls (no longer needed)
- [ ] Test with your symbols

## Batch Processing Optimization

If you're fetching data for multiple symbols, you can optimize:

### Old Way (Inefficient)
```python
mappings = nse.get_charting_mappings()  # Downloads entire file

for symbol in ['NIFTY 50', 'BANKNIFTY', 'NIFTY IT']:
    ticker = mappings[mappings['Symbol'] == symbol]['TradingSymbol'].iloc[0]
    df = nse.get_ohlc_from_charting(ticker, '1Day', start, end)
    # process df
```

### New Way (Efficient)
```python
# Option 1: Simple (searches each time)
for symbol in ['NIFTY 50', 'BANKNIFTY', 'NIFTY IT']:
    df = nse.get_ohlc_from_charting_v2(symbol, '1Day', start, end, 'Index')
    # process df

# Option 2: Optimized (cache tokens)
symbols = ['NIFTY 50', 'BANKNIFTY', 'NIFTY IT']
tokens = {}

# Search once
for symbol in symbols:
    result = nse.search_charting_symbol(symbol)
    tokens[symbol] = result['data'][0]['scripcode']

# Fetch data using cached tokens
for symbol in symbols:
    df = nse.get_charting_historical_data(
        symbol=symbol,
        token=tokens[symbol],
        symbol_type='Index',
        chart_type='D',
        time_interval=1,
        from_date=int(start.timestamp()),
        to_date=int(end.timestamp())
    )
    # process df
```

## Error Handling

### Old Method
```python
try:
    df = nse.get_ohlc_from_charting(ticker, '1Day', start, end)
except Exception as e:
    print(f"Error: {e}")
```

### New Method
```python
try:
    df = nse.get_ohlc_from_charting_v2(symbol, '1Day', start, end, 'Index')
except ValueError as e:
    print(f"Symbol not found or invalid: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Backward Compatibility

**Good news**: The old method still works! You can migrate gradually:

```python
# Old code continues to work
df_old = nse.get_ohlc_from_charting(ticker, '1Day', start, end)

# New code works alongside
df_new = nse.get_ohlc_from_charting_v2(symbol, '1Day', start, end, 'Index')
```

## Common Issues & Solutions

### Issue 1: "Symbol not found"
**Solution**: Check symbol name spelling or use search:
```python
result = nse.search_charting_symbol("RELI")  # Partial search
print(result['data'])  # See all matches
```

### Issue 2: Empty DataFrame
**Solution**: Check date range and market hours for intraday data
```python
# For intraday, use today's date only
today = datetime.now()
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="5Min",
    start_date=today.replace(hour=9, minute=0),
    end_date=today,
    symbol_type="Index"
)
```

### Issue 3: Wrong symbol_type
**Solution**: Use "Index" for indices, "Equity" for stocks
```python
# Indices
nse.get_ohlc_from_charting_v2("NIFTY 50", ..., symbol_type="Index")

# Stocks
nse.get_ohlc_from_charting_v2("RELIANCE", ..., symbol_type="Equity")
```

## Performance Comparison

| Operation | Old Method | New Method |
|-----------|------------|------------|
| First call | ~5-10s (download mappings) | ~2-3s (search + fetch) |
| Subsequent calls | ~2-3s | ~2-3s |
| Memory usage | High (entire mapping) | Low (only needed data) |

## Recommendation

✅ **Use new method for**:
- New projects
- Single symbol fetches
- When you don't have mappings cached

⚠️ **Keep old method if**:
- You have existing code that works
- You're fetching 100+ symbols (batch with cached mappings)

## Questions?

Check these files:
- `QUICK_START_CHARTING_V2.md` - Quick reference
- `NSE_CHARTING_V2_ANALYSIS.md` - Technical details
- `USAGE_EXAMPLE.py` - Working examples
