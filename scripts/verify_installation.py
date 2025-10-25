#!/usr/bin/env python
"""
Verification script to check if all dependencies are properly installed.
"""

import sys
import importlib


def check_package(package_name, import_name=None):
    """
    Check if a package is installed.
    
    Args:
        package_name (str): Display name of the package
        import_name (str): Import name (if different from package name)
    
    Returns:
        bool: True if package is installed, False otherwise
    """
    if import_name is None:
        import_name = package_name.lower().replace('-', '_')
    
    try:
        mod = importlib.import_module(import_name)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✓ {package_name}: {version}")
        return True
    except ImportError:
        print(f"✗ {package_name}: NOT INSTALLED")
        return False


def main():
    """Main verification function."""
    print("=" * 60)
    print("ecDNA Classification - Installation Verification")
    print("=" * 60)
    print()
    
    packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        ("xgboost", "xgboost"),
        ("tensorflow", "tensorflow"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
    ]
    
    results = []
    for pkg_name, import_name in packages:
        results.append(check_package(pkg_name, import_name))
    
    print()
    print("=" * 60)
    
    if all(results):
        print("SUCCESS: All required packages are installed!")
        print("You can now run: python main.py")
        return 0
    else:
        print("ERROR: Some packages are missing.")
        print("Please run: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())

