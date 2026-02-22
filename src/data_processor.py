import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import yfinance as yf

def load_and_process_data(ticker_symbol):
    print(f"⚙️ PROCESSING DATA FOR: {ticker_symbol}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Check the new 'stocks' mega-dataset folder first
    new_file_path = os.path.join(script_dir, f"../data/stocks/{ticker_symbol}_5Y_Data.csv")
    
    # 2. Check the old 'data' folder
    old_file_path = os.path.join(script_dir, f"../data/{ticker_symbol}_data.csv")
    
    # Determine which file to use
    if os.path.exists(new_file_path):
        file_path = new_file_path
        df = pd.read_csv(file_path)
    elif os.path.exists(old_file_path):
        file_path = old_file_path
        df = pd.read_csv(file_path)
    else:
        # 3. FAILSAFE: Auto-download if missing
        print(f"⚠️ Local data not found. Auto-downloading live data...")
        try:
            stock = yf.Ticker(ticker_symbol)
            df = stock.history(period="5y")
            if df.empty:
                print(f"❌ CRITICAL FAILURE: Could not fetch {ticker_symbol}.")
                return None, None, None
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            print(f"❌ CRITICAL FAILURE: Internet error - {e}")
            return None, None, None

    # Make sure we use the 'Close' price for prediction
    data = df.filter(['Close']).values
    
    # Scale the data between 0 and 1 for the AI
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Create the 60-day sequences
    sequence_length = 60
    X, y = [], []
    
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i, 0])
        y.append(scaled_data[i, 0])
        
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    print(f"   ✅ Data Loaded. Total Rows: {len(df)}")
    print(f"   ✅ Sequences Created. AI Training Samples: {len(X)}")
    print(f"   Shape of X (Inputs): {X.shape}")
    
    return X, y, scaler