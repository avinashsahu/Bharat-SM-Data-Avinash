"""
Simple test script for the new NSE Charting API v2 methods
Run from project root directory
"""

from datetime import datetime, timedelta
from Bharat_sm_data.Base.NSEBase import NSEBase
import time

print("=" * 80)
print("Testing New NSE Charting API Methods")
print("=" * 80)

# Initialize NSE Base
print("\nInitializing NSE Base...")
nse = NSEBase()
print("✓ Initialized successfully")

# Test 1: Search for a symbol
print("\n" + "=" * 80)
print("Test 1: Searching for 'NIFTY 50' symbol")
print("=" * 80)
try:
    search_result = nse.search_charting_symbol("NIFTY 50")
    print(f"Status: {search_result.get('status')}")
    if search_result.get('data'):
        for symbol_info in search_result['data']:
            print(f"  ✓ Symbol: {symbol_info['symbol']}")
            print(f"    Scripcode: {symbol_info['scripcode']}")
            print(f"    Type: {symbol_info['type']}")
            print(f"    Exchange: {symbol_info['exchange']}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Get historical data using simplified method
print("\n" + "=" * 80)
print("Test 2: Fetching last 10 days of NIFTY 50 data")
print("=" * 80)
time.sleep(2)
try:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)
    
    df = nse.get_ohlc_from_charting_v2(
        symbol="NIFTY 50",
        timeframe="1Day",
        start_date=start_date,
        end_date=end_date,
        symbol_type="Index"
    )
    
    print(f"✓ Data fetched successfully")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print("\nFirst 3 rows:")
    print(df.head(3))
    print("\nLast 3 rows:")
    print(df.tail(3))
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Search for equity stock
print("\n" + "=" * 80)
print("Test 3: Searching for 'RELIANCE' stock")
print("=" * 80)
time.sleep(2)
try:
    search_reliance = nse.search_charting_symbol("RELIANCE")
    print(f"Status: {search_reliance.get('status')}")
    if search_reliance.get('data'):
        print(f"✓ Found {len(search_reliance['data'])} results")
        for i, symbol_info in enumerate(search_reliance['data'][:3], 1):
            print(f"  {i}. {symbol_info['symbol']} (Token: {symbol_info['scripcode']}) - {symbol_info['type']}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("Testing Complete!")
print("=" * 80)
