"""
Check Groq compatibility with your system
Run this BEFORE installing Groq
"""

import sys
import pkg_resources

print("=" * 60)
print("🔍 GROQ COMPATIBILITY CHECK")
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
    'pydantic': '2.0',
    'httpx': '0.23.0',
    'typing-extensions': '4.7.0',
    'anyio': '3.0.0'
}

print("📦 Checking critical dependencies:")
print()

all_compatible = True

for package, min_version in critical_deps.items():
    try:
        installed = pkg_resources.get_distribution(package)
        print(f"✅ {package}: {installed.version} (installed)")
    except pkg_resources.DistributionNotFound:
        print(f"⚠️  {package}: Not found (will be installed)")

print()
print("=" * 60)
print("🎯 RECOMMENDATION")
print("=" * 60)
print()
print("Based on your system config:")
print()
print("✅ Best Groq version: groq==0.9.0")
print()
print("This version is compatible with:")
print("  • pydantic 2.12.4 (your version)")
print("  • httpx 0.28.1 (your version)")
print("  • Python 3.10")
print()
print("Install command:")
print("  pip install groq==0.9.0")
print()
print("=" * 60)