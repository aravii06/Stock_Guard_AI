import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import data_processor # Re-using your processor

def predict_stock_price(ticker_symbol):
    print(f"------------------------------------------------")
    print(f"🔮 STARTING PREDICTION FOR: {ticker_symbol}")

    # 1. Load the Data (We need the last 60 days to predict tomorrow)
    # The 'scaler' is essential to convert 0.5 back to ₹2500
    X, y, scaler = data_processor.load_and_process_data(ticker_symbol)
    
    # 2. Load the Saved Brain (.h5 file)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, f"../models/{ticker_symbol}_model.h5")
    
    if not os.path.exists(model_path):
        print(f"❌ ERROR: Model not found at {model_path}")
        return

    print("🧠 Loading the AI Model...")
    model = load_model(model_path)

    # 3. Get the Last 60 Days of Data
    # The AI needs the most recent "exam question" (last 60 hours) to answer
    # We take the very last sequence from our data
    last_60_days = X[-1] 
    # Reshape it to [1, 60, 1] because the AI expects a batch
    last_60_days = np.reshape(last_60_days, (1, last_60_days.shape[0], 1))

    # 4. Ask the AI to Predict
    predicted_price_scaled = model.predict(last_60_days)

    # 5. Convert the Answer back to Rupees (Undo the 0-1 scaling)
    predicted_price = scaler.inverse_transform(predicted_price_scaled)
    
    final_price = round(float(predicted_price[0][0]), 2)

    print(f"------------------------------------------------")
    print(f"💰 {ticker_symbol} PREDICTION RESULTS")
    print(f"------------------------------------------------")
    print(f"   AI's Predicted Fair Price: ₹ {final_price}")
    print(f"------------------------------------------------")

if __name__ == "__main__":
    predict_stock_price("RELIANCE.NS")