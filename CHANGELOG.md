# Changelog

All notable changes to this project will be documented in this file.

## [4.1.0] - 2025-01-18

### Added - NSE Charting API v2 Support

#### New Methods in NSEBase class:
- `search_charting_symbol(symbol, segment="")` - Search for symbols with segment filtering
- `get_charting_historical_data(symbol, token, symbol_type, chart_type, time_interval, from_date, to_date)` - Fetch OHLC data using token
- `get_ohlc_from_charting_v2(symbol, timeframe, start_date, end_date, symbol_type, segment)` - Simplified wrapper method (recommended)

#### New Features:
- **Segment Filtering**: Filter search results by market segment
  - `""` (empty) - All segments
  - `"IDX"` - Indices only
  - `"EQ"` - Equity only
  - `"FO"` - Futures & Options only

- **Extended Symbol Type Support**: Support for all instrument types
  - `"Index"` - Spot indices (NIFTY 50, BANKNIFTY)
  - `"Equity"` - Stocks (RELIANCE, TCS)
  - `"Futures"` - Futures contracts
  - `"Options"` - Options contracts

- **Multiple Timeframes**: Support for various timeframes
  - Intraday: 1Min, 5Min, 15Min, 30Min, 60Min
  - Daily/Weekly/Monthly: 1Day, 1Week, 1Month

#### Enhanced CustomRequest class:
- `post_and_get_data()` method for POST requests with JSON payloads

#### Benefits:
- Faster searches with segment filtering
- More accurate results
- Support for derivatives data
- No need for mapping files
- Dynamic symbol search
- Better error handling

### Documentation Added:
- `NSE_CHARTING_V2_ANALYSIS.md` - Technical API analysis
- `QUICK_START_CHARTING_V2.md` - Quick reference guide
- `CHARTING_V2_README.md` - Feature overview
- `SEGMENT_FILTER_REFERENCE.md` - Segment filtering guide
- `MIGRATION_GUIDE.md` - Migration from old to new API
- `DERIVATIVES_EXAMPLES.py` - Futures & options examples
- `SEGMENT_FILTERING_EXAMPLES.py` - Segment filtering examples
- `USAGE_EXAMPLE.py` - Comprehensive usage examples

### Technical Details:
- Uses new NSE charting endpoints (`/v1/exchanges/symbolsDynamic`, `/v1/charts/symbolHistoricalData`)
- POST-based API calls instead of GET
- Automatic session management and cookie handling
- Input validation for all parameters
- Comprehensive error handling

### Backward Compatibility:
- All existing methods continue to work unchanged
- New parameters are optional with sensible defaults
- No breaking changes to existing functionality

## [4.0.1] - Previous Release
- Previous features and functionality