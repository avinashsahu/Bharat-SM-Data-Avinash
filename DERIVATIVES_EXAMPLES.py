"""
Derivatives (Futures & Options) Examples for NSE Charting API v2

This demonstrates how to fetch data for Futures and Options contracts using:
- symbol_type="Futures" for futures contracts
- symbol_type="Options" for options contracts
- segment="FO" to filter F&O instruments

To run: python3 DERIVATIVES_EXAMPLES.py
"""

from datetime import datetime, timedelta
from Bharat_sm_data.Base.NSEBase import NSEBase
import time

def example_1_search_futures():
    """Example 1: Search for futures contracts"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Search for NIFTY Futures Contracts")
    print("="*80)
    
    nse = NSEBase()
    
    # Search for NIFTY futures
    result = nse.search_charting_symbol("NIFTY", segment="FO")
    
    if result.get('status') and result.get('data'):
        print(f"\n✓ Found {len(result['data'])} F&O instruments")
        
        # Filter for futures only
        futures = [s for s in result['data'] if 'FUT' in s['symbol'].upper()]
        
        print(f"\nFutures contracts ({len(futures)}):")
        for i, contract in enumerate(futures[:10], 1):  # Show first 10
            print(f"  {i:2}. {contract['symbol']:40} | Token: {contract['scripcode']:10} | Type: {contract['type']}")
    
    return result

def example_2_search_options():
    """Example 2: Search for options contracts"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Search for NIFTY Options Contracts")
    print("="*80)
    
    nse = NSEBase()
    
    # Search for NIFTY options
    result = nse.search_charting_symbol("NIFTY", segment="FO")
    
    if result.get('status') and result.get('data'):
        # Filter for options only (CE = Call, PE = Put)
        options = [s for s in result['data'] if 'CE' in s['symbol'] or 'PE' in s['symbol']]
        
        print(f"\n✓ Found {len(options)} options contracts")
        
        # Separate calls and puts
        calls = [s for s in options if 'CE' in s['symbol']]
        puts = [s for s in options if 'PE' in s['symbol']]
        
        print(f"\nCall Options ({len(calls)}):")
        for i, contract in enumerate(calls[:5], 1):  # Show first 5
            print(f"  {i}. {contract['symbol']:40} | Token: {contract['scripcode']}")
        
        print(f"\nPut Options ({len(puts)}):")
        for i, contract in enumerate(puts[:5], 1):  # Show first 5
            print(f"  {i}. {contract['symbol']:40} | Token: {contract['scripcode']}")
    
    return result

def example_3_fetch_futures_data():
    """Example 3: Fetch historical data for a futures contract"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Fetch Futures Contract Data")
    print("="*80)
    
    nse = NSEBase()
    
    # First, search for a specific futures contract
    result = nse.search_charting_symbol("NIFTY", segment="FO")
    
    if result.get('status') and result.get('data'):
        # Find a futures contract
        futures = [s for s in result['data'] if 'FUT' in s['symbol'].upper()]
        
        if futures:
            contract = futures[0]
            print(f"\n✓ Selected contract: {contract['symbol']}")
            print(f"  Token: {contract['scripcode']}")
            
            # Fetch data for this futures contract
            try:
                df = nse.get_ohlc_from_charting_v2(
                    symbol=contract['symbol'],
                    timeframe="1Day",
                    start_date=datetime.now() - timedelta(days=10),
                    end_date=datetime.now(),
                    symbol_type="Futures",  # Specify it's a futures contract
                    segment="FO"
                )
                
                print(f"\n✓ Fetched {len(df)} days of data")
                print("\nLatest 5 days:")
                print(df.tail(5))
                
                return df
            except Exception as e:
                print(f"\n✗ Error fetching data: {e}")
                print("Note: Some contracts may not have data available")
        else:
            print("\n✗ No futures contracts found")

def example_4_fetch_options_data():
    """Example 4: Fetch historical data for an options contract"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Fetch Options Contract Data")
    print("="*80)
    
    nse = NSEBase()
    
    # Search for options
    result = nse.search_charting_symbol("NIFTY", segment="FO")
    
    if result.get('status') and result.get('data'):
        # Find a call option
        options = [s for s in result['data'] if 'CE' in s['symbol']]
        
        if options:
            contract = options[0]
            print(f"\n✓ Selected contract: {contract['symbol']}")
            print(f"  Token: {contract['scripcode']}")
            
            # Fetch data for this options contract
            try:
                df = nse.get_ohlc_from_charting_v2(
                    symbol=contract['symbol'],
                    timeframe="1Day",
                    start_date=datetime.now() - timedelta(days=10),
                    end_date=datetime.now(),
                    symbol_type="Options",  # Specify it's an options contract
                    segment="FO"
                )
                
                print(f"\n✓ Fetched {len(df)} days of data")
                print("\nLatest 5 days:")
                print(df.tail(5))
                
                return df
            except Exception as e:
                print(f"\n✗ Error fetching data: {e}")
                print("Note: Some contracts may not have data available")
        else:
            print("\n✗ No options contracts found")

def example_5_compare_spot_vs_futures():
    """Example 5: Compare spot index vs futures"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Compare NIFTY Spot vs Futures")
    print("="*80)
    
    nse = NSEBase()
    
    # Get spot index data
    print("\nFetching NIFTY 50 Spot data...")
    df_spot = nse.get_ohlc_from_charting_v2(
        symbol="NIFTY 50",
        timeframe="1Day",
        start_date=datetime.now() - timedelta(days=5),
        end_date=datetime.now(),
        symbol_type="Index",
        segment="IDX"
    )
    
    print(f"✓ Spot data: {len(df_spot)} days")
    if not df_spot.empty:
        print(f"  Latest Close: {df_spot['close'].iloc[-1]:.2f}")
    
    # Get futures data
    print("\nSearching for NIFTY Futures...")
    result = nse.search_charting_symbol("NIFTY", segment="FO")
    
    if result.get('data'):
        futures = [s for s in result['data'] if 'FUT' in s['symbol'].upper()]
        if futures:
            contract = futures[0]
            print(f"✓ Found futures: {contract['symbol']}")
            
            try:
                df_futures = nse.get_ohlc_from_charting_v2(
                    symbol=contract['symbol'],
                    timeframe="1Day",
                    start_date=datetime.now() - timedelta(days=5),
                    end_date=datetime.now(),
                    symbol_type="Futures",
                    segment="FO"
                )
                
                print(f"✓ Futures data: {len(df_futures)} days")
                if not df_futures.empty:
                    print(f"  Latest Close: {df_futures['close'].iloc[-1]:.2f}")
                    
                    # Calculate basis (futures - spot)
                    if not df_spot.empty and not df_futures.empty:
                        spot_close = df_spot['close'].iloc[-1]
                        futures_close = df_futures['close'].iloc[-1]
                        basis = futures_close - spot_close
                        print(f"\n📊 Basis (Futures - Spot): {basis:.2f}")
                        print(f"   Premium: {(basis/spot_close)*100:.2f}%")
            except Exception as e:
                print(f"✗ Error: {e}")

def example_6_symbol_type_validation():
    """Example 6: Demonstrate symbol_type validation"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Symbol Type Validation")
    print("="*80)
    
    nse = NSEBase()
    
    valid_types = ["Index", "Equity", "Futures", "Options"]
    
    print("\n✓ Valid symbol_type values:")
    for symbol_type in valid_types:
        print(f"  - {symbol_type}")
    
    print("\n✗ Testing invalid symbol_type:")
    try:
        df = nse.get_ohlc_from_charting_v2(
            symbol="NIFTY 50",
            timeframe="1Day",
            symbol_type="INVALID"
        )
    except ValueError as e:
        print(f"  Correctly caught error: {e}")

def example_7_advanced_options_filtering():
    """Example 7: Advanced options filtering by strike and type"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Advanced Options Filtering")
    print("="*80)
    
    nse = NSEBase()
    
    # Search for NIFTY options
    result = nse.search_charting_symbol("NIFTY", segment="FO")
    
    if result.get('data'):
        options = [s for s in result['data'] if 'CE' in s['symbol'] or 'PE' in s['symbol']]
        
        print(f"\n✓ Found {len(options)} options contracts")
        
        # Group by expiry (assuming format contains date)
        print("\nSample contracts by type:")
        
        # ATM-ish strikes (around 23000-24000 range as example)
        atm_calls = [s for s in options if 'CE' in s['symbol'] and any(strike in s['symbol'] for strike in ['23000', '23500', '24000'])]
        atm_puts = [s for s in options if 'PE' in s['symbol'] and any(strike in s['symbol'] for strike in ['23000', '23500', '24000'])]
        
        print(f"\nATM Call Options ({len(atm_calls)}):")
        for contract in atm_calls[:5]:
            print(f"  - {contract['symbol']:40} | Token: {contract['scripcode']}")
        
        print(f"\nATM Put Options ({len(atm_puts)}):")
        for contract in atm_puts[:5]:
            print(f"  - {contract['symbol']:40} | Token: {contract['scripcode']}")

def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("NSE CHARTING API v2 - DERIVATIVES (FUTURES & OPTIONS) EXAMPLES")
    print("="*80)
    print("\nSymbol Types:")
    print("  'Index'    - For spot indices")
    print("  'Equity'   - For stocks")
    print("  'Futures'  - For futures contracts")
    print("  'Options'  - For options contracts")
    print("\nSegment Filter:")
    print("  'FO' - Futures & Options segment")
    
    try:
        example_1_search_futures()
        time.sleep(2)
        
        example_2_search_options()
        time.sleep(2)
        
        example_3_fetch_futures_data()
        time.sleep(2)
        
        example_4_fetch_options_data()
        time.sleep(2)
        
        example_5_compare_spot_vs_futures()
        time.sleep(2)
        
        example_6_symbol_type_validation()
        time.sleep(2)
        
        example_7_advanced_options_filtering()
        
        print("\n" + "="*80)
        print("✓ ALL EXAMPLES COMPLETED!")
        print("="*80)
        print("\n💡 Key Takeaways:")
        print("  1. Use symbol_type='Futures' for futures contracts")
        print("  2. Use symbol_type='Options' for options contracts")
        print("  3. Use segment='FO' to filter F&O instruments")
        print("  4. Search first to find exact contract symbols")
        print("  5. Not all contracts may have historical data available")
        
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
