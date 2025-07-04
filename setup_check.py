#!/usr/bin/env python3
"""
Test script to verify Gmail CLI setup.
"""

import sys
import importlib


def test_imports():
    """Test that all required packages can be imported."""
    required_packages = [
        "google.auth",
        "google_auth_oauthlib",
        "googleapiclient",
        "rich",
        "click",
    ]

    print("Testing package imports...")

    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            return False

    return True


def test_local_imports():
    """Test that local modules can be imported."""
    print("\nTesting local module imports...")

    required_local_modules = [
        "gmail_archive.gmail_client",
        "gmail_archive.email_table_formatter",
        "gmail_archive.message_utils",
        "gmail_archive.main",
    ]

    for module in required_local_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ gmail_archive.{module}: {e}")
            return False

    return True


def main():
    """Run all tests."""
    print("Gmail CLI Setup Test")
    print("=" * 30)

    success = True

    # Test external dependencies
    if not test_imports():
        success = False

    # Test local modules
    if not test_local_imports():
        success = False

    print("\n" + "=" * 30)
    if success:
        print("✅ All tests passed! Setup is complete.")
        print("\nNext steps:")
        print("1. Download your OAuth credentials from Google Cloud Console")
        print("2. Save them as 'credentials.json' in the project root")
        print("3. Run: poetry run gmail-cli")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
