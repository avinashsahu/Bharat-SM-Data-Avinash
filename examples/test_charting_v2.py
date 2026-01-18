"""
Test script for the new NSE Charting API v2 methods
Demonstrates how to use the new charting endpoints
"""

from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for local development
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Bharat_sm_data.Base.NSEBase import NSEBase
import time

# Initialize NSE Base
nse = NSEBase()

print("=" * 80)
print("Testing New NSE Charting API Methods")
print("=" * 80)

# Test 1: Search for a symbol
print("\n1. Searching for 'NIFTY 50' symbol...")
search_result = nse.search_charting_symbol("NIFTY 50")
print(f"Status: {search_result.get('status')}")
if search_result.get('data'):
    for symbol_info in search_result['data']:
        print(f"  - Symbol: {symbol_info['symbol']}")
        print(f"    Scripcode: {symbol_info['scripcode']}")
        print(f"    Type: {symbol_info['type']}")
        print(f"    Exchange: {symbol_info['exchange']}")

# Test 2: Get historical data using token directly
print("\n2. Fetching historical data for NIFTY 50 using token...")
time.sleep(2)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)  # Last 30 days

df_direct = nse.get_charting_historical_data(
    symbol="NIFTY 50",
    token="26000",  # Token for NIFTY 50
    symbol_type="Index",
    chart_type="D",  # Daily
    time_interval=1,
    from_date=int(start_date.timestamp()),
    to_date=int(end_date.timestamp())
)

print(f"Data shape: {df_direct.shape}")
print("\nFirst 5 rows:")
print(df_direct.head())
print("\nLast 5 rows:")
print(df_direct.tail())

# Test 3: Use simplified wrapper method
print("\n3. Using simplified wrapper method (get_ohlc_from_charting_v2)...")
time.sleep(2)
df_simple = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=start_date,
    end_date=end_date,
    symbol_type="Index"
)

print(f"Data shape: {df_simple.shape}")
print("\nFirst 5 rows:")
print(df_simple.head())

# Test 4: Try different timeframes
print("\n4. Testing different timeframes (Intraday - 5Min)...")
time.sleep(2)
today = datetime.now()
df_intraday = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="5Min",
    start_date=today.replace(hour=0, minute=0, second=0),
    end_date=today,
    symbol_type="Index"
)

print(f"Intraday data shape: {df_intraday.shape}")
if not df_intraday.empty:
    print("\nFirst 5 rows:")
    print(df_intraday.head())
    print("\nLast 5 rows:")
    print(df_intraday.tail())

# Test 5: Search and fetch for an equity stock
print("\n5. Testing with an equity stock (RELIANCE)...")
time.sleep(2)
search_reliance = nse.search_charting_symbol("RELIANCE")
print(f"Search status: {search_reliance.get('status')}")
if search_reliance.get('data'):
    print(f"Found {len(search_reliance['data'])} results")
    for symbol_info in search_reliance['data'][:3]:  # Show first 3 results
        print(f"  - {symbol_info['symbol']} ({symbol_info['scripcode']}) - {symbol_info['type']}")

# Fetch RELIANCE data
time.sleep(2)
df_reliance = nse.get_ohlc_from_charting_v2(
    symbol="RELIANCE",
    timeframe="1Day",
    start_date=end_date - timedelta(days=30),
    end_date=end_date,
    symbol_type="Equity"
)

print(f"\nRELIANCE data shape: {df_reliance.shape}")
if not df_reliance.empty:
    print("\nFirst 5 rows:")
    print(df_reliance.head())

print("\n" + "=" * 80)
print("Testing Complete!")
print("=" * 80)
