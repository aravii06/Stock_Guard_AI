import json
import time
import datetime
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "live_data.json")

print("🚨 INJECTING FAKE SCAM SPIKE IN 3 SECONDS...")
time.sleep(3)

fake_data = {
    "symbol": "SUZLON.NS",
    "price": 58.50, # Massive spike!
    "fair_value": 48.75,
    "deviation": 20.0,
    "status": "🔴 RISK ALERT: HIGH MANIPULATION DETECTED (+20.00%)",
    "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
}

with open(json_path, "w") as f:
    json.dump(fake_data, f)

print("💥 SPIKE INJECTED! Look at your Streamlit Dashboard!")