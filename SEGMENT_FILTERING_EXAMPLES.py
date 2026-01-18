"""
Segment Filtering Examples for NSE Charting API v2

This demonstrates how to use segment filters to narrow down search results:
- "" (empty) - Search all segments
- "FO" - Futures & Options only
- "IDX" - Indices only
- "EQ" - Equity only

To run: python3 SEGMENT_FILTERING_EXAMPLES.py
"""

from datetime import datetime, timedelta
from Bharat_sm_data.Base.NSEBase import NSEBase
import time

def example_1_search_all_segments():
    """Example 1: Search without segment filter (all segments)"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Search 'NIFTY' in ALL Segments")
    print("="*80)
    
    nse = NSEBase()
    
    result = nse.search_charting_symbol("NIFTY", segment="")
    
    if result.get('status') and result.get('data'):
        print(f"\n✓ Found {len(result['data'])} results:")
        for i, symbol in enumerate(result['data'][:10], 1):  # Show first 10
            print(f"  {i:2}. {symbol['symbol']:30} | Token: {symbol['scripcode']:10} | Type: {symbol['type']:15} | Exchange: {symbol['exchange']}")
    
    return result

def example_2_search_index_only():
    """Example 2: Search indices only"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Search 'NIFTY' in INDEX Segment Only (IDX)")
    print("="*80)
    
    nse = NSEBase()
    
    result = nse.search_charting_symbol("NIFTY", segment="IDX")
    
    if result.get('status') and result.get('data'):
        print(f"\n✓ Found {len(result['data'])} index results:")
        for i, symbol in enumerate(result['data'], 1):
            print(f"  {i:2}. {symbol['symbol']:30} | Token: {symbol['scripcode']:10} | Type: {symbol['type']}")
    
    return result

def example_3_search_equity_only():
    """Example 3: Search equities only"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Search 'RELIANCE' in EQUITY Segment Only (EQ)")
    print("="*80)
    
    nse = NSEBase()
    
    result = nse.search_charting_symbol("RELIANCE", segment="EQ")
    
    if result.get('status') and result.get('data'):
        print(f"\n✓ Found {len(result['data'])} equity results:")
        for i, symbol in enumerate(result['data'], 1):
            print(f"  {i:2}. {symbol['symbol']:30} | Token: {symbol['scripcode']:10} | Type: {symbol['type']}")
    
    return result

def example_4_search_futures_options():
    """Example 4: Search futures & options only"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Search 'NIFTY' in FUTURES & OPTIONS Segment (FO)")
    print("="*80)
    
    nse = NSEBase()
    
    result = nse.search_charting_symbol("NIFTY", segment="FO")
    
    if result.get('status') and result.get('data'):
        print(f"\n✓ Found {len(result['data'])} F&O results:")
        for i, symbol in enumerate(result['data'][:10], 1):  # Show first 10
            print(f"  {i:2}. {symbol['symbol']:40} | Token: {symbol['scripcode']:10} | Type: {symbol['type']}")
    
    return result

def example_5_fetch_data_with_segment():
    """Example 5: Fetch data using segment filter"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Fetch NIFTY 50 Data with IDX Segment Filter")
    print("="*80)
    
    nse = NSEBase()
    
    # Using segment filter ensures we get the exact index, not F&O contracts
    df = nse.get_ohlc_from_charting_v2(
        symbol="NIFTY 50",
        timeframe="1Day",
        start_date=datetime.now() - timedelta(days=10),
        end_date=datetime.now(),
        symbol_type="Index",
        segment="IDX"  # Filter to index segment only
    )
    
    print(f"\n✓ Fetched {len(df)} days of data")
    print("\nLatest 5 days:")
    print(df.tail(5))
    
    return df

def example_6_compare_segments():
    """Example 6: Compare search results across segments"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Compare 'NIFTY' Search Across Different Segments")
    print("="*80)
    
    nse = NSEBase()
    
    segments = {
        "All": "",
        "Index": "IDX",
        "Equity": "EQ",
        "F&O": "FO"
    }
    
    print(f"\n{'Segment':<15} | {'Results Count':<15} | {'Sample Result'}")
    print("-" * 80)
    
    for name, segment in segments.items():
        result = nse.search_charting_symbol("NIFTY", segment=segment)
        count = len(result.get('data', []))
        sample = result['data'][0]['symbol'] if result.get('data') else "N/A"
        print(f"{name:<15} | {count:<15} | {sample}")
        time.sleep(1)

def example_7_equity_with_filter():
    """Example 7: Fetch equity data with EQ segment filter"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Fetch RELIANCE Data with EQ Segment Filter")
    print("="*80)
    
    nse = NSEBase()
    
    df = nse.get_ohlc_from_charting_v2(
        symbol="RELIANCE",
        timeframe="1Day",
        start_date=datetime.now() - timedelta(days=10),
        end_date=datetime.now(),
        symbol_type="Equity",
        segment="EQ"  # Filter to equity segment only
    )
    
    print(f"\n✓ Fetched {len(df)} days of RELIANCE data")
    print("\nLatest 5 days:")
    print(df.tail(5))
    
    if not df.empty:
        print(f"\n📊 Quick Stats:")
        print(f"  Latest Close: ₹{df['close'].iloc[-1]:.2f}")
        print(f"  Highest: ₹{df['high'].max():.2f}")
        print(f"  Lowest: ₹{df['low'].min():.2f}")
    
    return df

def example_8_invalid_segment():
    """Example 8: Handle invalid segment"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Error Handling - Invalid Segment")
    print("="*80)
    
    nse = NSEBase()
    
    try:
        result = nse.search_charting_symbol("NIFTY", segment="INVALID")
        print("✗ Should have raised an error!")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")

def example_9_advanced_filtering():
    """Example 9: Advanced - Search and filter by type"""
    print("\n" + "="*80)
    print("EXAMPLE 9: Advanced Filtering - Find Specific Symbol Types")
    print("="*80)
    
    nse = NSEBase()
    
    # Search in F&O segment
    result = nse.search_charting_symbol("NIFTY", segment="FO")
    
    if result.get('data'):
        # Group by type
        types = {}
        for symbol in result['data']:
            symbol_type = symbol.get('type', 'Unknown')
            if symbol_type not in types:
                types[symbol_type] = []
            types[symbol_type].append(symbol['symbol'])
        
        print(f"\n✓ Found {len(result['data'])} F&O instruments")
        print("\nGrouped by type:")
        for symbol_type, symbols in types.items():
            print(f"\n  {symbol_type} ({len(symbols)} instruments):")
            for symbol in symbols[:3]:  # Show first 3 of each type
                print(f"    - {symbol}")
            if len(symbols) > 3:
                print(f"    ... and {len(symbols) - 3} more")

def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("NSE CHARTING API v2 - SEGMENT FILTERING EXAMPLES")
    print("="*80)
    print("\nSegment Values:")
    print("  '' (empty) - Search all segments")
    print("  'FO'       - Futures & Options only")
    print("  'IDX'      - Indices only")
    print("  'EQ'       - Equity only")
    
    try:
        example_1_search_all_segments()
        time.sleep(2)
        
        example_2_search_index_only()
        time.sleep(2)
        
        example_3_search_equity_only()
        time.sleep(2)
        
        example_4_search_futures_options()
        time.sleep(2)
        
        example_5_fetch_data_with_segment()
        time.sleep(2)
        
        example_6_compare_segments()
        time.sleep(2)
        
        example_7_equity_with_filter()
        time.sleep(2)
        
        example_8_invalid_segment()
        time.sleep(2)
        
        example_9_advanced_filtering()
        
        print("\n" + "="*80)
        print("✓ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\n💡 Key Takeaways:")
        print("  1. Use segment filters to narrow down search results")
        print("  2. 'IDX' for indices, 'EQ' for stocks, 'FO' for derivatives")
        print("  3. Empty segment searches all categories")
        print("  4. Segment filtering makes searches faster and more accurate")
        
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
