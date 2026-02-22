import streamlit as st
import json
import time
import os

st.set_page_config(page_title="Stock_Guard AI", layout="wide", page_icon="🛡️")

st.title("🛡️ Stock_Guard AI: Real-Time Fraud Radar")
st.markdown("Monitoring the Indian Equity Market for abnormal price deviations and pump-and-dump manipulation.")
st.divider()

# Create an empty placeholder container
# This allows Streamlit to update the numbers without refreshing the whole webpage
dashboard_placeholder = st.empty()

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "live_data.json")

# The Infinite Loop to continuously read the live data
while True:
    try:
        # Read the file that the WebSocket is updating
        with open(json_path, "r") as f:
            data = json.load(f)
            
        with dashboard_placeholder.container():
            st.subheader(f"Live Target: {data['symbol']}")
            
            # Create three columns for a beautiful metric display
            col1, col2, col3 = st.columns(3)
            
            col1.metric("Live Market Price", f"₹{data['price']}")
            col2.metric("AI Predicted Fair Value", f"₹{data['fair_value']}")
            col3.metric("Deviation %", f"{data['deviation']}%")
            
            st.markdown("### System Alert Status")
            # Display the colored alert box
            if "🔴" in data['status']:
                st.error(f"**{data['status']}** - Trading restricted.")
            elif "🟡" in data['status']:
                st.warning(f"**{data['status']}** - High volatility.")
            else:
                st.success(f"**{data['status']}**")
                
            st.caption(f"Last updated: {data['timestamp']} (Millisecond Latency)")
            
    except FileNotFoundError:
        with dashboard_placeholder.container():
            st.info("⏳ Waiting for the Live Radar WebSocket to connect to the NSE...")
    except json.JSONDecodeError:
        # Ignore errors if the file is currently being overwritten by the WebSocket
        pass
        
    # Wait half a second before checking the file again
    time.sleep(0.5)