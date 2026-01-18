"""
Complete Usage Example for NSE Charting API v2

This demonstrates all three new methods:
1. search_charting_symbol() - Search for symbols
2. get_charting_historical_data() - Get data with token
3. get_ohlc_from_charting_v2() - Simplified one-call method (RECOMMENDED)

To run: python3 USAGE_EXAMPLE.py
"""

from datetime import datetime, timedelta
from Bharat_sm_data.Base.NSEBase import NSEBase
import time

def example_1_simple_daily_data():
    """Example 1: Get daily data for NIFTY 50 (simplest method)"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple Daily Data Fetch")
    print("="*80)
    
    nse = NSEBase()
    
    # Get last 30 days of data
    df = nse.get_ohlc_from_charting_v2(
        symbol="NIFTY 50",
        timeframe="1Day",
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        symbol_type="Index"
    )
    
    print(f"\n✓ Fetched {len(df)} days of NIFTY 50 data")
    print(f"\nLatest data:")
    print(df.tail(5))
    
    return df

def example_2_intraday_data():
    """Example 2: Get intraday 5-minute data"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Intraday 5-Minute Data")
    print("="*80)
    
    nse = NSEBase()
    
    today = datetime.now()
    df = nse.get_ohlc_from_charting_v2(
        symbol="NIFTY 50",
        timeframe="5Min",
        start_date=today.replace(hour=9, minute=0, second=0, microsecond=0),
        end_date=today,
        symbol_type="Index"
    )
    
    print(f"\n✓ Fetched {len(df)} 5-minute candles")
    if not df.empty:
        print(f"\nFirst few candles:")
        print(df.head(3))
        print(f"\nLatest candles:")
        print(df.tail(3))
    else:
        print("No intraday data available (market might be closed)")
    
    return df

def example_3_search_symbols():
    """Example 3: Search for symbols"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Search for Symbols")
    print("="*80)
    
    nse = NSEBase()
    
    # Search for RELIANCE
    result = nse.search_charting_symbol("RELIANCE")
    
    if result.get('status') and result.get('data'):
        print(f"\n✓ Found {len(result['data'])} matches for 'RELIANCE':")
        for i, symbol in enumerate(result['data'][:5], 1):
            print(f"  {i}. {symbol['symbol']:20} | Token: {symbol['scripcode']:10} | Type: {symbol['type']}")
    
    return result

def example_4_equity_stock_data():
    """Example 4: Get equity stock data"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Equity Stock Data (RELIANCE)")
    print("="*80)
    
    nse = NSEBase()
    
    df = nse.get_ohlc_from_charting_v2(
        symbol="RELIANCE",
        timeframe="1Day",
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        symbol_type="Equity"
    )
    
    print(f"\n✓ Fetched {len(df)} days of RELIANCE data")
    print(f"\nLatest prices:")
    print(df.tail(5))
    
    # Calculate some basic stats
    if not df.empty:
        print(f"\n📊 Statistics (Last 30 days):")
        print(f"  Highest: ₹{df['high'].max():.2f}")
        print(f"  Lowest: ₹{df['low'].min():.2f}")
        print(f"  Average Close: ₹{df['close'].mean():.2f}")
        print(f"  Latest Close: ₹{df['close'].iloc[-1]:.2f}")
    
    return df

def example_5_advanced_with_token():
    """Example 5: Advanced usage with direct token"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Advanced - Using Token Directly")
    print("="*80)
    
    nse = NSEBase()
    
    # Step 1: Search for symbol to get token
    search_result = nse.search_charting_symbol("NIFTY 50")
    token = search_result['data'][0]['scripcode']
    print(f"\n✓ Found token for NIFTY 50: {token}")
    
    # Step 2: Use token directly to fetch data
    df = nse.get_charting_historical_data(
        symbol="NIFTY 50",
        token=token,
        symbol_type="Index",
        chart_type="D",  # D=Daily, I=Intraday, W=Weekly, M=Monthly
        time_interval=1,
        from_date=int((datetime.now() - timedelta(days=7)).timestamp()),
        to_date=int(datetime.now().timestamp())
    )
    
    print(f"\n✓ Fetched {len(df)} days using direct token method")
    print(f"\nData:")
    print(df)
    
    return df

def example_6_multiple_timeframes():
    """Example 6: Compare different timeframes"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Multiple Timeframes Comparison")
    print("="*80)
    
    nse = NSEBase()
    
    timeframes = ["1Day", "1Week", "1Month"]
    
    for tf in timeframes:
        df = nse.get_ohlc_from_charting_v2(
            symbol="NIFTY 50",
            timeframe=tf,
            start_date=datetime.now() - timedelta(days=90),
            end_date=datetime.now(),
            symbol_type="Index"
        )
        print(f"\n{tf:10} : {len(df):3} candles | Latest Close: {df['close'].iloc[-1]:.2f}")
        time.sleep(1)

def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("NSE CHARTING API v2 - COMPLETE USAGE EXAMPLES")
    print("="*80)
    
    try:
        # Run examples
        example_1_simple_daily_data()
        time.sleep(2)
        
        example_2_intraday_data()
        time.sleep(2)
        
        example_3_search_symbols()
        time.sleep(2)
        
        example_4_equity_stock_data()
        time.sleep(2)
        
        example_5_advanced_with_token()
        time.sleep(2)
        
        example_6_multiple_timeframes()
        
        print("\n" + "="*80)
        print("✓ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
