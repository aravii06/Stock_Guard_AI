import os
import yfinance as yf
import pyotp
from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import json
import data_processor
from tensorflow.keras.models import load_model
import datetime # <-- ADD THIS IMPORT
from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import data_processor
from tensorflow.keras.models import load_model

# ==========================================
# 🛑 THE GATEKEEPER (PLACE THIS EXACTLY HERE)
# ==========================================
def is_market_open():
    now = datetime.datetime.now()
    
    # 1. Check if Weekend (Saturday = 5, Sunday = 6)
    if now.weekday() >= 5:
        print("💤 Market is closed (Weekend). Stock_Guard AI Price Radar is sleeping.")
        return False
        
    # 2. Check 2026 NSE Holidays
    nse_holidays_2026 = ["2026-01-26", "2026-03-03", "2026-04-03", "2026-05-01", "2026-08-15", "2026-10-02", "2026-11-08", "2026-12-25"]
    today_str = now.strftime("%Y-%m-%d")
    if today_str in nse_holidays_2026:
        print(f"💤 Market is closed today (Holiday: {today_str}). Radar sleeping.")
        return False
        
    # 3. Check Market Hours (9:15 AM to 3:30 PM)
    current_minutes = now.hour * 60 + now.minute
    if current_minutes < 555 or current_minutes > 930:
        print("⏳ Market is currently offline. Outside of 9:15 AM - 3:30 PM window.")
        return False

    return True

# If the market is closed, shut down the script immediately
if not is_market_open():
    exit()

# ==========================================
# 🔐 YOUR ANGEL ONE CREDENTIALS (Keep this exactly the same)
# ==========================================
api_key = "..."
# ... (The rest of your AI and WebSocket code continues here) ...

# ==========================================
# 🔐 YOUR ANGEL ONE CREDENTIALS
# ==========================================
api_key = "REPLACE_WITH_STREAMLIT_SECRET"
client_code = "REPLACE_WITH_STREAMLIT_SECRET"
password = "REPLACE_WITH_STREAMLIT_SECRET"
totp_secret = "REPLACE_WITH_STREAMLIT_SECRET"
totp_secret = totp_secret.replace(" ", "").strip()
totp_secret += "=" * ((8 - len(totp_secret) % 8) % 8)

# ==========================================
# 🧠 PRE-LOAD THE AI BRAIN 
# ==========================================
print("🤖 Waking up the Deep Learning Model for SUZLON.NS...")
script_dir = os.path.dirname(os.path.abspath(__file__))
# 1. Change to Suzlon model
model_path = os.path.join(script_dir, "../models/SUZLON.NS_model.h5")

try:
    ai_model = load_model(model_path)
    # 2. Change to Suzlon data
    X, y, scaler = data_processor.load_and_process_data("SUZLON.NS")
    last_60_days = X[-1].reshape(1, 60, 1)
    
    predicted_scaled = ai_model.predict(last_60_days)
    ai_fair_price = float(scaler.inverse_transform(predicted_scaled)[0][0])
    print(f"🎯 AI Pre-Calculated Fair Value: ₹{round(ai_fair_price, 2)}")
except Exception as e:
    print(f"❌ Error loading AI: {e}")
    print("💡 FIX: Run 'py src/model_trainer.py' first to generate the SUZLON brain!")
    exit()

# ==========================================
# 1. AUTHENTICATE
# ==========================================
smartApi = SmartConnect(api_key)
totp = pyotp.TOTP(totp_secret).now()
data = smartApi.generateSession(client_code, password, totp)
feed_token = smartApi.getfeedToken()

# ==========================================
# 2. THE WEBSOCKET (REAL-TIME INFERENCE)
# ==========================================
# 3. Change to Suzlon's exact NSE Token ID
target_tokens = ["33632"] 
sws = SmartWebSocketV2(data['data']['jwtToken'], api_key, client_code, feed_token)

def on_data(wsapp, message):
    # Ensure it's the Suzlon token
    if message.get('token') == '33632' and 'last_traded_price' in message:
        live_price = message['last_traded_price'] / 100.0
        
        # ⚖️ REAL-TIME FRAUD LOGIC
        deviation = ((live_price - ai_fair_price) / ai_fair_price) * 100
        
        print(f"⚡ [LIVE TICK] Price: ₹{live_price:.2f} | AI Fair Value: ₹{ai_fair_price:.2f}")
        
        # We save the status as a variable now, so we can send it to Streamlit AND print it
        if deviation > 15:
            status = f"🔴 RISK ALERT: HIGH MANIPULATION DETECTED (+{deviation:.2f}%)"
            print(f"   {status}")
        elif deviation < -15:
            status = f"🟡 CAUTION: CRASH DETECTED ({deviation:.2f}%)"
            print(f"   {status}")
        else:
            status = f"🟢 SAFE: Organic market movement ({deviation:.2f}%)"
            print(f"   {status}")
        print("-" * 60)

        # 👇 THIS IS THE NEW PART: Saving the exact tick to a JSON file 👇
        live_data = {
            "symbol": "SUZLON.NS",
            "price": round(live_price, 2),
            "fair_value": round(ai_fair_price, 2),
            "deviation": round(deviation, 2),
            "status": status,
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "live_data.json")
        with open(json_path, "w") as f:
            json.dump(live_data, f)

# ==========================================
# 🛑 KEEP ALL OF THIS EXACTLY THE SAME 🛑
# ==========================================
def on_open(wsapp):
    print("🟢 WebSocket Connected! Subscribing to NSE (SUZLON)...")
    sws.subscribe("stream_1", 1, [{"exchangeType": 1, "tokens": target_tokens}])

def on_error(wsapp, error):
    print(f"⚠️ WebSocket Error: {error}")

sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error

print("⏳ Opening WebSocket Tunnel to Angel One...")
sws.connect()