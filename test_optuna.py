#!/usr/bin/env python
"""Test script to verify Optuna installation"""

try:
    import optuna
    print(f"✅ Optuna is installed! Version: {optuna.__version__}")
except ImportError as e:
    print(f"❌ Optuna is NOT installed: {e}")
    print("Please run: uv add optuna")

