# Quick Start Guide - NSE Charting API v2

## Installation
```bash
pip install -r requirements.txt
```

## Basic Usage

### 1. Simple Daily Data Fetch
```python
from Bharat_sm_data.Base.NSEBase import NSEBase
from datetime import datetime, timedelta

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

### 2. Intraday Data
```python
# Get today's 5-minute data for RELIANCE
today = datetime.now()
df = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="5Min",
    start_date=today.replace(hour=9, minute=0, second=0),
    end_date=today,
    symbol_type="Equity"
)
```

### 3. Search for Symbols
```python
# Search for a symbol
result = nse.search_charting_symbol("RELIANCE")

if result.get('status'):
    for symbol_info in result['data']:
        print(f"{symbol_info['symbol']} - Token: {symbol_info['scripcode']}")

# Search with segment filter (more precise)
result = nse.search_charting_symbol("NIFTY", segment="IDX")  # Index only
result = nse.search_charting_symbol("RELIANCE", segment="EQ")  # Equity only
result = nse.search_charting_symbol("NIFTY", segment="FO")  # Futures & Options only
```

### 4. Advanced: Direct Token Usage
```python
# If you already know the token, use it directly
df = nse.get_charting_historical_data(
    symbol="NIFTY 50",
    token="26000",
    symbol_type="Index",
    chart_type="D",
    time_interval=1,
    from_date=0,  # All available data
    to_date=int(datetime.now().timestamp())
)
```

### 5. Futures Data
```python
# Search for futures contract
result = nse.search_charting_symbol("NIFTY", segment="FO")
futures = [s for s in result['data'] if 'FUT' in s['symbol']]

# Fetch futures data
df = nse.get_ohlc_from_charting_v2(
    symbol=futures[0]['symbol'],
    timeframe="1Day",
    symbol_type="Futures",
    segment="FO"
)
```

### 6. Options Data
```python
# Search for options contract
result = nse.search_charting_symbol("NIFTY", segment="FO")
options = [s for s in result['data'] if 'CE' in s['symbol']]

# Fetch options data
df = nse.get_ohlc_from_charting_v2(
    symbol=options[0]['symbol'],
    timeframe="1Day",
    symbol_type="Options",
    segment="FO"
)
```

## Supported Timeframes
- `"1Min"` - 1 minute candles
- `"5Min"` - 5 minute candles
- `"15Min"` - 15 minute candles
- `"30Min"` - 30 minute candles
- `"60Min"` - 1 hour candles
- `"1Day"` - Daily candles
- `"1Week"` - Weekly candles
- `"1Month"` - Monthly candles

## Symbol Types
- `"Index"` - For spot indices (NIFTY 50, BANKNIFTY, etc.)
- `"Equity"` - For stocks (RELIANCE, TCS, etc.)
- `"Futures"` - For futures contracts (NIFTY FUT, etc.)
- `"Options"` - For options contracts (NIFTY CE/PE, etc.)

## Segment Filters
Use segment filters in `search_charting_symbol()` and `get_ohlc_from_charting_v2()` to narrow down results:
- `""` (empty) - Search all segments (default)
- `"IDX"` - Indices only
- `"EQ"` - Equity only
- `"FO"` - Futures & Options only

**Example:**
```python
# Search only indices
result = nse.search_charting_symbol("NIFTY", segment="IDX")

# Fetch data with segment filter
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    segment="IDX"  # Ensures we get the index, not F&O contracts
)
```

## Common Tokens
| Symbol | Token | Type |
|--------|-------|------|
| NIFTY 50 | 26000 | Index |
| NIFTY 500 | 26006 | Index |
| BANKNIFTY | 26009 | Index |

Use `search_charting_symbol()` to find tokens for other symbols.

## Output DataFrame Structure
```
Columns: time, open, high, low, close, volume
- time: datetime object
- open, high, low, close: float (price)
- volume: int (trading volume)
```

## Error Handling
```python
try:
    df = nse.get_ohlc_from_charting_v2(
        symbol="INVALID_SYMBOL",
        timeframe="1Day"
    )
except ValueError as e:
    print(f"Error: {e}")
```

## Tips
1. Always initialize `NSEBase()` once and reuse the object
2. For batch processing, search symbols first and cache tokens
3. Use appropriate date ranges for intraday data (same day only)
4. The API returns data in IST timezone
5. Empty DataFrames are returned if no data is available

## Run Test Script
```bash
cd examples
python test_charting_v2.py
```
