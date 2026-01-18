#!/usr/bin/env python3
"""
Automated packaging script for Bharat SM Data Avinash Fork v4.1.0
Handles cleaning, building, checking, and uploading the package
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"Command: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} failed")
        print(f"Error: {result.stderr}")
        return False
    
    return True

def clean_build_artifacts():
    """Clean previous build artifacts"""
    print("\n🧹 Cleaning build artifacts...")
    
    dirs_to_remove = ['build', 'dist', 'Bharat_sm_data_avinash.egg-info']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed: {dir_name}")
    
    print("✅ Build artifacts cleaned")

def check_requirements():
    """Check if required tools are installed"""
    print("\n🔍 Checking requirements...")
    
    required_packages = ['wheel', 'twine', 'build']
    missing_packages = []
    
    # Try pip3 first, then pip
    pip_cmd = 'pip3' if subprocess.run("which pip3", shell=True, capture_output=True).returncode == 0 else 'pip'
    
    for package in required_packages:
        result = subprocess.run(f"{pip_cmd} show {package}", shell=True, capture_output=True)
        if result.returncode != 0:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print(f"Install with: {pip_cmd} install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def build_package():
    """Build the package"""
    return run_command("python setup.py sdist bdist_wheel", "Building package")

def check_package():
    """Check package integrity"""
    return run_command("twine check dist/*", "Checking package integrity")

def test_local_install():
    """Test local installation"""
    print("\n🧪 Testing local installation...")
    
    # Find the wheel file
    dist_files = list(Path('dist').glob('*.whl'))
    if not dist_files:
        print("❌ No wheel file found")
        return False
    
    wheel_file = dist_files[0]
    
    # Test installation
    test_cmd = f"pip3 install {wheel_file} --force-reinstall --quiet"
    if not run_command(test_cmd, "Installing package locally"):
        return False
    
    # Test import
    test_import = """
python -c "
try:
    from Bharat_sm_data.Base.NSEBase import NSEBase
    nse = NSEBase()
    print('✅ Package import successful')
    print('✅ NSEBase initialization successful')
    
    # Test new methods exist
    assert hasattr(nse, 'search_charting_symbol'), 'search_charting_symbol method missing'
    assert hasattr(nse, 'get_ohlc_from_charting_v2'), 'get_ohlc_from_charting_v2 method missing'
    print('✅ New methods are available')
    
except Exception as e:
    print(f'❌ Import test failed: {e}')
    exit(1)
"
"""
    
    return run_command(test_import, "Testing package import")

def upload_to_test_pypi():
    """Upload to test PyPI"""
    response = input("\n📤 Upload to test PyPI? (y/N): ").lower()
    if response == 'y':
        return run_command("twine upload -r testpypi dist/*", "Uploading to test PyPI")
    return True

def upload_to_pypi():
    """Upload to production PyPI"""
    response = input("\n📤 Upload to production PyPI? (y/N): ").lower()
    if response == 'y':
        print("\n⚠️  WARNING: This will upload to production PyPI!")
        confirm = input("Are you sure? Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            return run_command("twine upload dist/*", "Uploading to production PyPI")
    return True

def main():
    """Main packaging workflow"""
    print("🚀 Bharat SM Data Avinash Fork v4.1.0 - Packaging Script")
    print("=" * 60)
    
    # Check current directory
    if not os.path.exists('setup.py'):
        print("❌ setup.py not found. Run this script from the project root.")
        sys.exit(1)
    
    # Step 1: Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Step 2: Clean build artifacts
    clean_build_artifacts()
    
    # Step 3: Build package
    if not build_package():
        sys.exit(1)
    
    # Step 4: Check package
    if not check_package():
        sys.exit(1)
    
    # Step 5: Test local installation
    if not test_local_install():
        print("⚠️  Local installation test failed, but continuing...")
    
    # Step 6: Show build results
    print("\n📦 Build Results:")
    if os.path.exists('dist'):
        for file in os.listdir('dist'):
            file_path = os.path.join('dist', file)
            size = os.path.getsize(file_path)
            print(f"  📄 {file} ({size:,} bytes)")
    
    # Step 7: Upload options
    upload_to_test_pypi()
    upload_to_pypi()
    
    print("\n🎉 Packaging process completed!")
    print("\nNext steps:")
    print("1. Test installation: pip3 install Bharat-sm-data-avinash==4.1.0")
    print("2. Create GitHub release: https://github.com/avinashsahu/Bharat-SM-Data-Avinash/releases")
    print("3. Update documentation if needed")

if __name__ == "__main__":
    main()