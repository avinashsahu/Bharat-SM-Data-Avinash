# NSE Charting API v2 - Analysis & Implementation

## Overview
This document explains the new NSE Charting API endpoints discovered from analyzing the network requests at https://charting.nseindia.com

## API Flow Analysis

### 1. Request Sequence
When visiting the NSE charting website, the following sequence occurs:

```
1. Sensor Data POST (Anti-bot protection)
   ↓
2. Symbol Search POST
   ↓
3. Historical Data POST
   ↓
4. Periodic Sensor Data POST (Session maintenance)
```

### 2. Key Endpoints

#### A. Symbol Search
- **URL**: `https://charting.nseindia.com/v1/exchanges/symbolsDynamic`
- **Method**: POST
- **Purpose**: Search for symbols and get their metadata including scripcode/token
- **Request Payload**:
  ```json
  {
    "symbol": "NIFTY 50",
    "segment": ""
  }
  ```
- **Segment Values**:
  - `""` (empty) - Search all segments
  - `"IDX"` - Indices only
  - `"EQ"` - Equity only
  - `"FO"` - Futures & Options only
- **Response**:
  ```json
  {
    "status": true,
    "data": [
      {
        "symbol": "NIFTY 50",
        "instrumentType": "0",
        "scripcode": "26000",
        "description": "NIFTY 50",
        "exchange": "NSE",
        "fullname": "NSE:NIFTY 50",
        "type": "Index"
      }
    ]
  }
  ```

#### B. Historical Data
- **URL**: `https://charting.nseindia.com/v1/charts/symbolHistoricalData`
- **Method**: POST
- **Purpose**: Fetch OHLC historical data
- **Request Payload**:
  ```json
  {
    "token": "26000",
    "fromDate": 0,
    "toDate": 1768592211,
    "symbol": "NIFTY 50",
    "symbolType": "Index",
    "chartType": "D",
    "timeInterval": 1
  }
  ```
- **Response**:
  ```json
  {
    "status": true,
    "data": [
      {
        "volume": 0,
        "high": 279.02,
        "low": 279.02,
        "time": 646963200000,
        "close": 279.02,
        "open": 279.02
      }
    ]
  }
  ```

#### C. Anti-Bot Protection
- **URL**: `https://charting.nseindia.com/mb2HgJ135/B1-ZgKvTw/...`
- **Method**: POST
- **Purpose**: Akamai bot detection bypass
- **Payload**: Encrypted sensor_data
- **Note**: This is handled automatically by maintaining session cookies

## Implementation Details

### New Methods Added

#### 1. `search_charting_symbol(symbol, segment="")`
Searches for a symbol and returns metadata including the scripcode/token needed for data fetching.

**Parameters**:
- `symbol` (str): Symbol name (e.g., "NIFTY 50", "RELIANCE")
- `segment` (str, optional): Market segment filter
  - `""` (empty) - Search all segments (default)
  - `"IDX"` - Indices only
  - `"EQ"` - Equity only
  - `"FO"` - Futures & Options only

**Returns**: Dict with symbol information

**Example**:
```python
nse = NSEBase()

# Search all segments
result = nse.search_charting_symbol("NIFTY 50")

# Search only indices
result = nse.search_charting_symbol("NIFTY", segment="IDX")

# Search only equities
result = nse.search_charting_symbol("RELIANCE", segment="EQ")

# Search F&O
result = nse.search_charting_symbol("NIFTY", segment="FO")

token = result['data'][0]['scripcode']  # "26000"
```

#### 2. `get_charting_historical_data(symbol, token, symbol_type, chart_type, time_interval, from_date, to_date)`
Fetches historical OHLC data using the token obtained from symbol search.

**Parameters**:
- `symbol` (str): Symbol name
- `token` (str): Scripcode from search_charting_symbol
- `symbol_type` (str): "Index" or "Equity"
- `chart_type` (str): "D" (Daily), "I" (Intraday), "W" (Weekly), "M" (Monthly)
- `time_interval` (int): Minutes for intraday, 1 for others
- `from_date` (int): Unix timestamp
- `to_date` (int): Unix timestamp

**Returns**: DataFrame with columns: time, open, high, low, close, volume

**Example**:
```python
df = nse.get_charting_historical_data(
    symbol="NIFTY 50",
    token="26000",
    symbol_type="Index",
    chart_type="D",
    time_interval=1,
    from_date=0,
    to_date=int(datetime.now().timestamp())
)
```

#### 3. `get_ohlc_from_charting_v2(symbol, timeframe, start_date, end_date, symbol_type, segment)` ⭐ **Recommended**
Simplified wrapper that automatically searches for the symbol and fetches data in one call.

**Parameters**:
- `symbol` (str): Symbol name
- `timeframe` (str): "1Min", "5Min", "15Min", "30Min", "60Min", "1Day", "1Week", "1Month"
- `start_date` (datetime, optional): Start date
- `end_date` (datetime, optional): End date
- `symbol_type` (str): "Index" or "Equity"
- `segment` (str, optional): Market segment filter
  - `""` (empty) - Search all segments (default)
  - `"IDX"` - Indices only
  - `"EQ"` - Equity only
  - `"FO"` - Futures & Options only

**Returns**: DataFrame with OHLC data

**Example**:
```python
from datetime import datetime, timedelta

nse = NSEBase()
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Get daily data with segment filter
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=start_date,
    end_date=end_date,
    symbol_type="Index",
    segment="IDX"  # Ensures we get the index, not F&O contracts
)

# Get equity data
df = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="1Day",
    start_date=start_date,
    end_date=end_date,
    symbol_type="Equity",
    segment="EQ"  # Filter to equity segment
)

# Get intraday data
df_intraday = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="5Min",
    start_date=datetime.now().replace(hour=9, minute=0),
    end_date=datetime.now(),
    symbol_type="Equity",
    segment="EQ"
)
```

### Changes to Existing Classes

#### CustomRequest.py
Added `post_and_get_data()` method to support POST requests with JSON payloads.

#### NSEBase.py
- Added `_charting_headers` attribute for charting-specific headers
- Added three new methods for charting API v2
- Updated class docstring

## Key Differences from Old API

| Feature | Old API | New API (v2) |
|---------|---------|--------------|
| Method | GET | POST |
| URL Pattern | `/Charts/ChartData` | `/v1/charts/symbolHistoricalData` |
| Symbol Lookup | Required mapping file | Dynamic search endpoint |
| Token Format | Trading symbol | Scripcode (numeric) |
| Response Format | Separate arrays (t, o, h, l, c, v) | Array of objects |
| Date Format | Unix seconds | Unix milliseconds |

## Usage Recommendations

1. **For simple use cases**: Use `get_ohlc_from_charting_v2()` - it handles everything automatically
2. **For batch processing**: Use `search_charting_symbol()` once, cache the token, then call `get_charting_historical_data()` multiple times
3. **For real-time/intraday**: Use timeframes like "1Min", "5Min" with appropriate date ranges

## Testing

Run the test script to verify functionality:
```bash
cd examples
python test_charting_v2.py
```

## Notes

- The API requires proper session cookies (handled automatically by visiting the base URL first)
- Anti-bot protection is bypassed by maintaining session state
- Timestamps in responses are in milliseconds (converted to datetime in the methods)
- Symbol search returns multiple matches - the first one is typically the most relevant

## Future Enhancements

When you provide more request examples (symbol changes, different searches), we can add:
- Symbol autocomplete functionality
- Advanced filtering options
- Support for derivatives/options data
- Real-time quote integration
