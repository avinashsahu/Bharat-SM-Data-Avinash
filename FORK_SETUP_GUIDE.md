# Fork Setup Guide - Bharat SM Data Avinash

## Overview

This guide explains how to set up and maintain your fork of the Bharat SM Data library with the new NSE Charting API v2 features.

## Repository Setup

### 1. Fork Information
- **Original Repository**: https://github.com/Sampad-Hegde/Bharat-SM-Data
- **Your Fork**: https://github.com/avinashsahu/Bharat-SM-Data-Avinash
- **Package Name**: `Bharat-sm-data-avinash`
- **PyPI Name**: `Bharat_sm_data_avinash`

### 2. Key Changes Made

#### setup.py Updates
- Package name: `Bharat_sm_data_avinash`
- URL: Updated to your fork
- Author: Updated to your information
- Project URLs: Added reference to original project

#### README.md Updates
- Added fork information and credits
- Updated installation instructions
- Added new API v2 examples
- Updated all GitHub links to your fork

#### Build Commands
- Updated for new package name
- Updated PyPI upload commands

## Installation Commands

### For Users

```bash
# Install your fork
pip install Bharat-sm-data-avinash

# Install original package (for comparison)
pip install Bharat-sm-data
```

### For Development

```bash
# Clone your fork
git clone https://github.com/avinashsahu/Bharat-SM-Data-Avinash.git
cd Bharat-SM-Data-Avinash

# Install in development mode
pip install -e .
```

## Package Distribution

### 1. Build Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build package
python setup.py sdist bdist_wheel

# Check package
twine check dist/*
```

### 2. Upload to PyPI

```bash
# Test PyPI (optional)
twine upload -r testpypi dist/Bharat_sm_data_avinash-4.1.0*

# Production PyPI
twine upload dist/Bharat_sm_data_avinash-4.1.0*
```

### 3. Automated Script

```bash
python package_release.py
```

## Usage Differences

### Your Fork
```python
# After: pip install Bharat-sm-data-avinash
from Bharat_sm_data.Base.NSEBase import NSEBase

nse = NSEBase()

# New API v2 methods available
df = nse.get_ohlc_from_charting_v2(
    symbol="NIFTY 50",
    timeframe="1Day",
    symbol_type="Index",
    segment="IDX"
)
```

### Original Package
```python
# After: pip install Bharat-sm-data
from Bharat_sm_data.Base.NSEBase import NSEBase

nse = NSEBase()

# Only original methods available
df = nse.get_ohlc_from_charting(ticker, timeframe, start_date, end_date)
```

## Maintaining Your Fork

### 1. Keep Track of Original Updates

```bash
# Add original as upstream
git remote add upstream https://github.com/Sampad-Hegde/Bharat-SM-Data.git

# Fetch upstream changes
git fetch upstream

# Merge upstream changes (be careful with conflicts)
git merge upstream/master
```

### 2. Version Management

- Your fork: `4.1.0` (with new features)
- Original: `4.0.1` (without new features)
- Future versions: Increment based on your changes

### 3. Documentation Updates

Keep these files updated:
- `README.md` - Installation and usage
- `CHANGELOG.md` - Version history
- Example scripts - Working examples
- Documentation files - API guides

## Contributing Back

If the original author accepts your changes:

### 1. Create Pull Request
```bash
# Push your changes
git push origin master

# Create PR on GitHub
# Go to: https://github.com/Sampad-Hegde/Bharat-SM-Data
# Click "New Pull Request"
```

### 2. If PR is Accepted
- Your changes will be in the original package
- Users can use the original package name
- You can archive your fork or keep it for additional features

### 3. If PR is Not Accepted
- Continue maintaining your fork
- Keep it updated with upstream changes
- Provide clear documentation about differences

## Package Comparison

| Feature | Original Package | Your Fork |
|---------|------------------|-----------|
| Package Name | `Bharat-sm-data` | `Bharat-sm-data-avinash` |
| Version | 4.0.1 | 4.1.0 |
| NSE Charting API v2 | ❌ | ✅ |
| Segment Filtering | ❌ | ✅ |
| Futures/Options Support | ❌ | ✅ |
| Dynamic Symbol Search | ❌ | ✅ |
| Multiple Timeframes | ❌ | ✅ |

## Support and Issues

### For Your Fork
- Issues: https://github.com/avinashsahu/Bharat-SM-Data-Avinash/issues
- Discussions: GitHub Discussions on your repo

### For Original Package
- Issues: https://github.com/Sampad-Hegde/Bharat-SM-Data/issues
- Documentation: https://bharat-sm-data.readthedocs.io/

## Best Practices

### 1. Clear Attribution
- Always credit the original author
- Maintain license compatibility
- Document what you've added

### 2. Version Management
- Use semantic versioning
- Clearly document changes
- Maintain backward compatibility

### 3. Documentation
- Keep README updated
- Provide clear examples
- Document new features

### 4. Testing
- Test all new features
- Ensure backward compatibility
- Provide test scripts

## Release Checklist

- [ ] Update version in setup.py
- [ ] Update README.md
- [ ] Update CHANGELOG.md
- [ ] Test all features
- [ ] Build package
- [ ] Test installation
- [ ] Upload to PyPI
- [ ] Create GitHub release
- [ ] Update documentation

## Summary

Your fork provides enhanced functionality while maintaining compatibility with the original project. Users can choose between:

1. **Original Package** (`Bharat-sm-data`) - Stable, well-established
2. **Your Fork** (`Bharat-sm-data-avinash`) - Enhanced with new API v2 features

Both packages can coexist, giving users flexibility in their choice.