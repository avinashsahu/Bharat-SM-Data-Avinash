#!/usr/bin/env python3
"""
Setup script for Bharat SM Data Avinash Fork
Helps initialize the fork with proper configuration
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completed")
        if result.stdout:
            print(result.stdout.strip())
    else:
        print(f"❌ {description} failed")
        if result.stderr:
            print(f"Error: {result.stderr.strip()}")
        return False
    
    return True

def check_git_setup():
    """Check if git is properly configured"""
    print("\n🔍 Checking Git setup...")
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository")
        return False
    
    # Check remote origin
    result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        origin_url = result.stdout.strip()
        print(f"✅ Origin: {origin_url}")
        
        if "avinashsahu/Bharat-SM-Data-Avinash" in origin_url:
            print("✅ Fork URL is correct")
        else:
            print("⚠️  Origin URL doesn't match expected fork URL")
    
    return True

def setup_upstream():
    """Setup upstream remote"""
    print("\n🔄 Setting up upstream remote...")
    
    # Check if upstream already exists
    result = subprocess.run("git remote get-url upstream", shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        upstream_url = result.stdout.strip()
        print(f"✅ Upstream already configured: {upstream_url}")
    else:
        # Add upstream remote
        upstream_url = "https://github.com/Sampad-Hegde/Bharat-SM-Data.git"
        if run_command(f"git remote add upstream {upstream_url}", "Adding upstream remote"):
            print(f"✅ Upstream added: {upstream_url}")
        else:
            return False
    
    # Fetch upstream
    return run_command("git fetch upstream", "Fetching upstream changes")

def check_python_setup():
    """Check Python environment"""
    print("\n🔍 Checking Python setup...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    
    # Check required packages
    required_packages = ['wheel', 'twine', 'build', 'pandas', 'requests']
    missing_packages = []
    
    # Try pip3 first, then pip
    pip_cmd = 'pip3' if subprocess.run("which pip3", shell=True, capture_output=True).returncode == 0 else 'pip'
    
    for package in required_packages:
        result = subprocess.run(f"{pip_cmd} show {package}", shell=True, capture_output=True)
        if result.returncode != 0:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        response = input("Install missing packages? (y/N): ").lower()
        if response == 'y':
            install_cmd = f"{pip_cmd} install {' '.join(missing_packages)}"
            return run_command(install_cmd, "Installing missing packages")
        else:
            print("❌ Required packages not installed")
            return False
    else:
        print("✅ All required packages are installed")
    
    return True

def test_package_import():
    """Test if the package can be imported"""
    print("\n🧪 Testing package import...")
    
    try:
        from Bharat_sm_data.Base.NSEBase import NSEBase
        print("✅ Package import successful")
        
        nse = NSEBase()
        print("✅ NSEBase initialization successful")
        
        # Check new methods
        new_methods = ['search_charting_symbol', 'get_ohlc_from_charting_v2']
        for method in new_methods:
            if hasattr(nse, method):
                print(f"✅ {method} method available")
            else:
                print(f"❌ {method} method missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎯 Next Steps:")
    print("=" * 50)
    
    print("\n1. Development:")
    print("   - Make your changes to the code")
    print("   - Test your changes")
    print("   - Update documentation")
    
    print("\n2. Testing:")
    print("   - Run: python test_installation.py")
    print("   - Run example scripts to test functionality")
    
    print("\n3. Building:")
    print("   - Run: python package_release.py")
    print("   - This will build and optionally upload to PyPI")
    
    print("\n4. Publishing:")
    print("   - Package name: Bharat-sm-data-avinash")
    print("   - Install command: pip install Bharat-sm-data-avinash")
    
    print("\n5. GitHub:")
    print("   - Create releases on your fork")
    print("   - Update README and documentation")
    print("   - Consider creating PR to original repo")
    
    print("\n📚 Documentation:")
    print("   - FORK_SETUP_GUIDE.md - Fork maintenance guide")
    print("   - PACKAGING_GUIDE.md - Packaging instructions")
    print("   - CHARTING_V2_README.md - New features overview")

def main():
    """Main setup workflow"""
    print("🚀 Bharat SM Data Avinash Fork - Setup Script")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('setup.py'):
        print("❌ setup.py not found. Run this script from the project root.")
        sys.exit(1)
    
    success = True
    
    # Step 1: Check Git setup
    if not check_git_setup():
        success = False
    
    # Step 2: Setup upstream
    if not setup_upstream():
        success = False
    
    # Step 3: Check Python setup
    if not check_python_setup():
        success = False
    
    # Step 4: Test package import
    if not test_package_import():
        print("⚠️  Package import failed, but this might be expected if not installed")
    
    if success:
        print("\n🎉 Fork setup completed successfully!")
        show_next_steps()
    else:
        print("\n❌ Some setup steps failed. Please review and fix the issues.")
        sys.exit(1)

if __name__ == "__main__":
    main()