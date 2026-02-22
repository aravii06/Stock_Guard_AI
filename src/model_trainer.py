import os
import data_processor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def train_model(ticker_symbol):
    print(f"🚀 INITIALIZING TRAINING FOR: {ticker_symbol}")
    print("-" * 48)
    
    # 1. Get the data from your processor
    X, y, scaler = data_processor.load_and_process_data(ticker_symbol)
    
    if X is None:
        print("❌ Training Aborted: No data available.")
        return
        
    # 2. Build the Deep Learning Brain
    print("🧠 Building the Neural Network...")
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # 3. Train the Brain
    print(f"🏋️ Training the AI on {ticker_symbol} history...")
    model.fit(X, y, batch_size=32, epochs=5) # 5 epochs for a quick test run
    
    # 4. Save the Brain (THE FIX FOR YOUR ERROR)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "../models")
    
    # Force create the folder if it doesn't exist!
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"📁 Created missing directory: {models_dir}")
        
    model_path = os.path.join(models_dir, f"{ticker_symbol}_model.h5")
    model.save(model_path)
    print(f"✅ MODEL SAVED SUCCESSFULLY: {model_path}")
    print("-" * 48)

if __name__ == "__main__":
    # We are explicitly telling it to train Suzlon!
    train_model("SUZLON.NS")