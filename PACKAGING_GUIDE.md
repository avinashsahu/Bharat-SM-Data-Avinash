# Packaging Guide - Bharat SM Data v4.1.0

## Overview

This guide explains how to package and distribute the updated Bharat SM Data library with the new NSE Charting API v2 features.

## What's New in v4.1.0

- NSE Charting API v2 support
- Segment filtering (IDX, EQ, FO)
- Support for Futures and Options data
- Dynamic symbol search
- Multiple timeframes support
- Enhanced error handling

## Prerequisites

Install required packaging tools:

```bash
pip install wheel twine build
```

## Step-by-Step Packaging Process

### 1. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
```

### 2. Update Version

The version has been updated to `4.1.0` in `setup.py`:

```python
version="4.1.0"
```

### 3. Build the Package

```bash
# Build source distribution and wheel
python setup.py sdist bdist_wheel

# Alternative using build (recommended)
python -m build
```

This creates:
- `dist/Bharat_sm_data-4.1.0.tar.gz` (source distribution)
- `dist/Bharat_sm_data-4.1.0-py3-none-any.whl` (wheel)

### 4. Verify the Package

```bash
# Check package integrity
twine check dist/*
```

Expected output:
```
Checking dist/Bharat_sm_data-4.1.0.tar.gz: PASSED
Checking dist/Bharat_sm_data-4.1.0-py3-none-any.whl: PASSED
```

### 5. Test Installation Locally

```bash
# Install locally to test
pip install dist/Bharat_sm_data-4.1.0-py3-none-any.whl

# Test the new features
python -c "
from Bharat_sm_data.Base.NSEBase import NSEBase
nse = NSEBase()
result = nse.search_charting_symbol('NIFTY 50', segment='IDX')
print('✓ New features working!')
"
```

### 6. Upload to Test PyPI (Optional)

```bash
# Upload to test PyPI first
twine upload -r testpypi dist/Bharat_sm_data-4.1.0*
```

Test installation from test PyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple Bharat-sm-data==4.1.0
```

### 7. Upload to Production PyPI

```bash
# Upload to production PyPI
twine upload dist/Bharat_sm_data-4.1.0*
```

You'll be prompted for your PyPI credentials.

### 8. Verify Installation

```bash
# Install from PyPI
pip install Bharat-sm-data==4.1.0

# Test installation
python -c "
from Bharat_sm_data.Base.NSEBase import NSEBase
print('Package installed successfully!')
"
```

## Package Structure

The package includes:

```
Bharat_sm_data/
├── Base/
│   ├── __init__.py
│   ├── CustomRequest.py      # Enhanced with POST support
│   └── NSEBase.py           # New charting methods added
├── Technical/
│   ├── __init__.py
│   └── NSE.py
├── Derivatives/
│   ├── __init__.py
│   ├── NSE.py
│   └── Sensibull.py
├── Fundamentals/
│   ├── __init__.py
│   ├── BSE.py
│   ├── MoneyControl.py
│   ├── Screener.py
│   └── TickerTape.py
└── __init__.py
```

## New Methods Available

After installation, users can access:

```python
from Bharat_sm_data.Base.NSEBase import NSEBase

nse = NSEBase()

# New methods in v4.1.0:
nse.search_charting_symbol(symbol, segment="")
nse.get_charting_historical_data(symbol, token, symbol_type, ...)
nse.get_ohlc_from_charting_v2(symbol, timeframe, symbol_type, segment, ...)
```

## Usage in Other Projects

### Installation

```bash
pip install Bharat-sm-data==4.1.0
```

### Basic Usage

```python
from Bharat_sm_data.Base.NSEBase import NSEBase
from datetime import datetime, timedelta

# Initialize
nse = NSEBase()

# Get NIFTY 50 data with new API
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    symbol_type="Index",
    segment="IDX"
)

print(df.head())
```

### Advanced Usage

```python
# Search with segment filtering
result = nse.search_charting_symbol("RELIANCE", segment="EQ")
print(f"Found {len(result['data'])} equity matches")

# Get futures data
fo_result = nse.search_charting_symbol("NIFTY", segment="FO")
futures = [s for s in fo_result['data'] if 'FUT' in s['symbol']]

if futures:
    df_futures = nse.get_ohlc_from_charting_v2(
        symbol=futures[0]['symbol'],
        timeframe="1Day",
        symbol_type="Futures",
        segment="FO"
    )
    print(f"Futures data: {len(df_futures)} rows")
```

## Dependencies

The package requires:
- Python >= 3.7
- pandas >= 2.0.3
- requests >= 2.31.0
- Brotli >= 1.0.0
- pydash >= 7.0.6
- beautifulsoup4 >= 4.12.2
- numpy >= 1.25.2
- html5lib >= 1.1
- lxml >= 4.9.3

## Backward Compatibility

✅ **Fully backward compatible**
- All existing methods work unchanged
- New parameters are optional
- No breaking changes

## Documentation

After installation, users can refer to:
- [ReadTheDocs](https://bharat-sm-data.readthedocs.io/en/latest/) (main documentation)
- GitHub repository examples
- Built-in docstrings

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure proper installation
   ```bash
   pip uninstall Bharat-sm-data
   pip install Bharat-sm-data==4.1.0
   ```

2. **Missing Dependencies**: Install with dependencies
   ```bash
   pip install Bharat-sm-data[dev]==4.1.0
   ```

3. **Version Conflicts**: Check installed version
   ```python
   import Bharat_sm_data
   print(Bharat_sm_data.__version__)  # Should show 4.1.0
   ```

## Release Checklist

- [x] Update version in setup.py (4.1.0)
- [x] Update description with new features
- [x] Create CHANGELOG.md
- [x] Update README.md with new features
- [x] Test all new methods
- [x] Verify backward compatibility
- [x] Clean build artifacts
- [x] Build package
- [x] Check with twine
- [x] Test local installation
- [ ] Upload to test PyPI (optional)
- [ ] Upload to production PyPI
- [ ] Create GitHub release tag
- [ ] Update documentation

## GitHub Release

After successful PyPI upload, create a GitHub release:

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag: `v4.1.0`
4. Title: `NSE Charting API v2 Support - v4.1.0`
5. Description: Copy from CHANGELOG.md
6. Attach build artifacts (optional)

## Summary

The package is ready for distribution with:
- ✅ New NSE Charting API v2 methods
- ✅ Segment filtering support
- ✅ Futures & Options support
- ✅ Enhanced error handling
- ✅ Comprehensive documentation
- ✅ Backward compatibility
- ✅ Updated version (4.1.0)

Users can now install and use the enhanced library in their projects!