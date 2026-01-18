# NSE Charting API v2 - New Feature

## 🎉 What's New

Three new methods added to fetch historical data from NSE's charting API:

1. **`search_charting_symbol()`** - Search for symbols
2. **`get_charting_historical_data()`** - Fetch data with token
3. **`get_ohlc_from_charting_v2()`** ⭐ **RECOMMENDED** - One-call simplified method

## 🚀 Quick Start

```python
from Bharat_sm_data.Base.NSEBase import NSEBase
from datetime import datetime, timedelta

# Initialize
nse = NSEBase()

# Get last 30 days of NIFTY 50 data
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    symbol_type="Index"
)

print(df.head())
```

## 📊 Output

```
                 time      open      high       low     close    volume
0 2025-01-01 00:00:00  23500.50  23650.75  23480.25  23620.40  12345678
1 2025-01-02 00:00:00  23620.40  23720.80  23590.10  23680.55  13456789
...
```

## 🎯 Features

- ✅ No mapping files needed
- ✅ Dynamic symbol search
- ✅ Support for indices and equities
- ✅ Multiple timeframes (1Min to 1Month)
- ✅ Clean DataFrame output
- ✅ Automatic session management

## 📚 Documentation

| File | Description |
|------|-------------|
| `QUICK_START_CHARTING_V2.md` | Quick reference guide |
| `NSE_CHARTING_V2_ANALYSIS.md` | Technical API analysis |
| `MIGRATION_GUIDE.md` | Migrate from old to new API |
| `USAGE_EXAMPLE.py` | 6 complete examples |
| `IMPLEMENTATION_SUMMARY.md` | What was implemented |

## 🔧 Methods

### Method 1: Simple (Recommended)

```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=start,
    end_date=end,
    symbol_type="Index"
)
```

### Method 2: Search First

```python
# Search for symbol
result = nse.search_charting_symbol("RELIANCE")
print(result['data'][0]['scripcode'])  # Get token

# Then fetch data
df = nse.get_ohlc_from_charting_v2("RELIANCE", "1Day", start, end, "Equity")
```

### Method 3: Advanced (Direct Token)

```python
df = nse.get_charting_historical_data(
    symbol="NIFTY 50",
    token="26000",
    symbol_type="Index",
    chart_type="D",
    time_interval=1,
    from_date=int(start.timestamp()),
    to_date=int(end.timestamp())
)
```

## ⏱️ Supported Timeframes

| Timeframe | Description |
|-----------|-------------|
| `"1Min"` | 1-minute candles |
| `"5Min"` | 5-minute candles |
| `"15Min"` | 15-minute candles |
| `"30Min"` | 30-minute candles |
| `"60Min"` | 1-hour candles |
| `"1Day"` | Daily candles |
| `"1Week"` | Weekly candles |
| `"1Month"` | Monthly candles |

## 🏷️ Symbol Types

Use the appropriate symbol_type when fetching data:

| Symbol Type | Description | Use For | Example |
|-------------|-------------|---------|---------|
| `"Index"` | Spot indices | NIFTY 50, BANKNIFTY | Index data |
| `"Equity"` | Stocks | RELIANCE, TCS | Stock data |
| `"Futures"` | Futures contracts | NIFTY FUT, RELIANCE FUT | Futures data |
| `"Options"` | Options contracts | NIFTY CE/PE | Options data |

**Example:**
```python
# Index
df = nse.get_ohlc_from_charting_v2("NIFTY 50", "1Day", symbol_type="Index")

# Equity
df = nse.get_ohlc_from_charting_v2("RELIANCE", "1Day", symbol_type="Equity")

# Futures
df = nse.get_ohlc_from_charting_v2("NIFTY 25JAN2024 FUT", "1Day", symbol_type="Futures")

# Options
df = nse.get_ohlc_from_charting_v2("NIFTY 25JAN2024 23500 CE", "1Day", symbol_type="Options")
```

## 🔍 Segment Filters (NEW!)

Filter search results by market segment for faster and more accurate results:

| Segment | Description | Use Case |
|---------|-------------|----------|
| `""` (empty) | All segments | When you want all matches |
| `"IDX"` | Indices only | For index data (NIFTY, BANKNIFTY) |
| `"EQ"` | Equity only | For stock data (RELIANCE, TCS) |
| `"FO"` | Futures & Options | For derivatives data |

**Example:**
```python
# Search only indices
result = nse.search_charting_symbol("NIFTY", segment="IDX")

# Fetch with segment filter
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    segment="IDX"  # Ensures we get the index, not F&O
)
```

## 📝 Examples

### Example 1: Index Data
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    symbol_type="Index"
)
```

### Example 2: Stock Data
```python
df = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="1Day",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    symbol_type="Equity"
)
```

### Example 3: Intraday Data
```python
today = datetime.now()
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="5Min",
    start_date=today.replace(hour=9, minute=0, second=0),
    end_date=today,
    symbol_type="Index"
)
```

### Example 4: Futures Data
```python
# Search for futures contract first
result = nse.search_charting_symbol("NIFTY", segment="FO")
futures_symbol = [s for s in result['data'] if 'FUT' in s['symbol']][0]['symbol']

# Fetch futures data
df = nse.get_ohlc_from_charting_v2(
    symbol=futures_symbol,
    timeframe="1Day",
    symbol_type="Futures",  # Specify it's a futures contract
    segment="FO"
)
```

### Example 5: Options Data
```python
# Search for options contract
result = nse.search_charting_symbol("NIFTY", segment="FO")
options_symbol = [s for s in result['data'] if 'CE' in s['symbol']][0]['symbol']

# Fetch options data
df = nse.get_ohlc_from_charting_v2(
    symbol=options_symbol,
    timeframe="1Day",
    symbol_type="Options",  # Specify it's an options contract
    segment="FO"
)
```

### Example 6: Search Symbols
```python
result = nse.search_charting_symbol("RELIANCE")
for symbol in result['data']:
    print(f"{symbol['symbol']} - Token: {symbol['scripcode']}")

# With segment filter for more precise results
result = nse.search_charting_symbol("NIFTY", segment="IDX")  # Index only
result = nse.search_charting_symbol("RELIANCE", segment="EQ")  # Equity only
```

## 🧪 Testing

Run the examples:

```bash
# Simple test
python3 test_charting_simple.py

# Complete examples
python3 USAGE_EXAMPLE.py

# Segment filtering examples
python3 SEGMENT_FILTERING_EXAMPLES.py

# Derivatives (Futures & Options) examples
python3 DERIVATIVES_EXAMPLES.py

# Detailed test suite
python3 examples/test_charting_v2.py
```

## 🔄 Migration from Old API

If you're using `get_ohlc_from_charting()`, see `MIGRATION_GUIDE.md` for step-by-step migration instructions.

**TL;DR**: Replace this:
```python
mappings = nse.get_charting_mappings()
ticker = mappings[mappings['Symbol'] == 'NIFTY 50']['TradingSymbol'].iloc[0]
df = nse.get_ohlc_from_charting(ticker, '1Day', start, end)
```

With this:
```python
df = nse.get_ohlc_from_charting_v2('NIFTY 50', '1Day', start, end, 'Index')
```

## 🐛 Common Issues

### Empty DataFrame
- Check date range (intraday data only available for current day)
- Verify market is open for intraday data
- Confirm symbol name is correct

### Symbol Not Found
```python
# Use search to find correct symbol name
result = nse.search_charting_symbol("RELI")
print(result['data'])  # Shows all matches
```

### Wrong Symbol Type
- Use `"Index"` for NIFTY 50, BANKNIFTY, etc.
- Use `"Equity"` for RELIANCE, TCS, etc.

## 📊 Known Tokens

| Symbol | Token | Type |
|--------|-------|------|
| NIFTY 50 | 26000 | Index |
| NIFTY 500 | 26006 | Index |

Use `search_charting_symbol()` to find tokens for other symbols.

## 🎓 Learn More

1. **Quick Start**: `QUICK_START_CHARTING_V2.md`
2. **Technical Details**: `NSE_CHARTING_V2_ANALYSIS.md`
3. **Migration Guide**: `MIGRATION_GUIDE.md`
4. **Examples**: `USAGE_EXAMPLE.py`

## 💡 Tips

1. **Reuse NSEBase instance** - Don't create new instance for each call
2. **Cache tokens** - For batch processing, search once and cache tokens
3. **Use appropriate timeframes** - Intraday data only for current day
4. **Handle errors** - Wrap calls in try-except blocks

## 🤝 Contributing

Found a bug or have a suggestion? Please provide:
- Sample request/response from browser DevTools
- Expected vs actual behavior
- Code snippet to reproduce

## 📄 License

Same as the main Bharat-SM-Data package.

## ✅ Status

- ✅ Implementation complete
- ✅ Syntax validated
- ✅ Documentation complete
- ⏳ Awaiting runtime testing
- ⏳ Awaiting additional request examples

---

**Need help?** Check the documentation files or run `USAGE_EXAMPLE.py` for working examples.
