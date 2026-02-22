import sys
import yfinance as yf
import tensorflow as tf
import torch

print("\n--- SYSTEM DIAGNOSTIC REPORT ---")
print(f"1. Python Version: {sys.version.split()[0]}")

# Check 1: Stock Data
try:
    print("\n2. Testing Stock Connection...")
    # Fetching Reliance Industries from NSE
    ticker = yf.Ticker("RELIANCE.NS")
    data = ticker.history(period="1d")
    
    if not data.empty:
        price = data['Close'].iloc[-1]
        print(f"   ✅ SUCCESS: Fetched Reliance Price: ₹{price:.2f}")
    else:
        print("   ❌ FAILED: No data received. (Check Internet)")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Check 2: AI Brains
print("\n3. Testing AI Libraries...")
print(f"   ✅ TensorFlow Version: {tf.__version__}")
print(f"   ✅ PyTorch Version: {torch.__version__}")

print("\n--- READY TO START PROJECT ---")