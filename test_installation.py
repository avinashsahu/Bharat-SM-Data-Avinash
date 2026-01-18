#!/usr/bin/env python3
"""
Test script to verify the Bharat SM Data package installation and new features
"""

def test_basic_import():
    """Test basic package import"""
    print("🔍 Testing basic import...")
    try:
        from Bharat_sm_data.Base.NSEBase import NSEBase
        print("✅ NSEBase import successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_initialization():
    """Test NSEBase initialization"""
    print("\n🔍 Testing NSEBase initialization...")
    try:
        from Bharat_sm_data.Base.NSEBase import NSEBase
        nse = NSEBase()
        print("✅ NSEBase initialization successful")
        return True, nse
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False, None

def test_new_methods(nse):
    """Test new methods are available"""
    print("\n🔍 Testing new methods availability...")
    
    new_methods = [
        'search_charting_symbol',
        'get_charting_historical_data', 
        'get_ohlc_from_charting_v2'
    ]
    
    for method in new_methods:
        if hasattr(nse, method):
            print(f"✅ {method} method available")
        else:
            print(f"❌ {method} method missing")
            return False
    
    return True

def test_method_signatures(nse):
    """Test method signatures"""
    print("\n🔍 Testing method signatures...")
    
    try:
        # Test search_charting_symbol signature
        import inspect
        sig = inspect.signature(nse.search_charting_symbol)
        params = list(sig.parameters.keys())
        expected_params = ['symbol', 'segment']
        
        if all(param in params for param in expected_params):
            print("✅ search_charting_symbol signature correct")
        else:
            print(f"❌ search_charting_symbol signature incorrect. Expected: {expected_params}, Got: {params}")
            return False
        
        # Test get_ohlc_from_charting_v2 signature
        sig = inspect.signature(nse.get_ohlc_from_charting_v2)
        params = list(sig.parameters.keys())
        expected_params = ['symbol', 'timeframe', 'start_date', 'end_date', 'symbol_type', 'segment']
        
        if all(param in params for param in expected_params):
            print("✅ get_ohlc_from_charting_v2 signature correct")
        else:
            print(f"❌ get_ohlc_from_charting_v2 signature incorrect. Expected: {expected_params}, Got: {params}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Signature test failed: {e}")
        return False

def test_validation():
    """Test input validation"""
    print("\n🔍 Testing input validation...")
    
    try:
        from Bharat_sm_data.Base.NSEBase import NSEBase
        nse = NSEBase()
        
        # Test invalid segment
        try:
            nse.search_charting_symbol("NIFTY", segment="INVALID")
            print("❌ Invalid segment validation failed")
            return False
        except ValueError:
            print("✅ Invalid segment validation working")
        
        # Test invalid symbol_type
        try:
            nse.get_ohlc_from_charting_v2("NIFTY 50", symbol_type="INVALID")
            print("❌ Invalid symbol_type validation failed")
            return False
        except ValueError:
            print("✅ Invalid symbol_type validation working")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False

def test_backward_compatibility():
    """Test backward compatibility"""
    print("\n🔍 Testing backward compatibility...")
    
    try:
        from Bharat_sm_data.Base.NSEBase import NSEBase
        nse = NSEBase()
        
        # Test old methods still exist
        old_methods = [
            'get_market_status_and_current_val',
            'get_last_traded_date',
            'get_second_wise_data',
            'get_ohlc_data',
            'search'
        ]
        
        for method in old_methods:
            if hasattr(nse, method):
                print(f"✅ {method} (old method) still available")
            else:
                print(f"❌ {method} (old method) missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Bharat SM Data Avinash Fork v4.1.0 - Installation Test")
    print("=" * 60)
    
    # Test 1: Basic import
    if not test_basic_import():
        print("\n❌ Basic import test failed. Package may not be installed correctly.")
        return False
    
    # Test 2: Initialization
    success, nse = test_initialization()
    if not success:
        print("\n❌ Initialization test failed.")
        return False
    
    # Test 3: New methods
    if not test_new_methods(nse):
        print("\n❌ New methods test failed.")
        return False
    
    # Test 4: Method signatures
    if not test_method_signatures(nse):
        print("\n❌ Method signatures test failed.")
        return False
    
    # Test 5: Input validation
    if not test_validation():
        print("\n❌ Input validation test failed.")
        return False
    
    # Test 6: Backward compatibility
    if not test_backward_compatibility():
        print("\n❌ Backward compatibility test failed.")
        return False
    
    print("\n🎉 All tests passed!")
    print("\n✅ Package is correctly installed and working")
    print("✅ New NSE Charting API v2 features are available")
    print("✅ Backward compatibility maintained")
    print("✅ Input validation working")
    
    print("\n📚 Quick usage example:")
    print("""
from Bharat_sm_data.Base.NSEBase import NSEBase
from datetime import datetime, timedelta

nse = NSEBase()

# Search with segment filter
result = nse.search_charting_symbol("NIFTY 50", segment="IDX")

# Get historical data
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=datetime.now() - timedelta(days=30),
    symbol_type="Index",
    segment="IDX"
)

# Install command for this fork:
# pip install Bharat-sm-data-avinash
""")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)