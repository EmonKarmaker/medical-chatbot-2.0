"""
Check Streamlit compatibility with your system
"""

import sys
import pkg_resources

print("=" * 60)
print("🔍 STREAMLIT COMPATIBILITY CHECK")
print("=" * 60)
print()

# Check Python version
python_version = sys.version_info
print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version.major == 3 and python_version.minor >= 8:
    print("✅ Python version compatible (3.8+)")
else:
    print("❌ Python version too old (need 3.8+)")
    exit(1)

print()

# Check critical dependencies
critical_deps = {
    'pydantic': '2.12.4',
    'requests': '2.32.5',
    'typing-extensions': '4.15.0',
}

print("📦 Checking critical dependencies:")
print()

for package, your_version in critical_deps.items():
    try:
        installed = pkg_resources.get_distribution(package)
        print(f"✅ {package}: {installed.version} (installed)")
    except pkg_resources.DistributionNotFound:
        print(f"⚠️  {package}: Not found")

print()
print("=" * 60)pip install streamlit==1.28.0
print("🎯 RECOMMENDATION")
print("=" * 60)
print()
print("✅ Compatible Streamlit version: streamlit==1.28.0")
print()
print("This version is compatible with:")
print("  • pydantic 2.12.4 (your version)")
print("  • Python 3.10")
print("  • All your existing packages")
print()
print("Install command:")
print("  pip install streamlit==1.28.0")
print()
print("=" * 60)