import yfinance as yf
import os
import pandas as pd

# ==========================================
# 🎯 INDIAN MARKET MEGA-DATASET
# ==========================================
target_tickers = [
    # --- PART 1: THE "CLEAN" DATA (NIFTY 50 STABLE STOCKS) ---
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS",
    "SBIN.NS", "INFY.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS",
    "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "TATAMOTORS.NS",
    "TATASTEEL.NS", "KOTAKBANK.NS", "TITAN.NS", "ADANIENT.NS", "NTPC.NS",
    "AXISBANK.NS", "ASIANPAINT.NS", "POWERGRID.NS", "BAJAJFINSV.NS", 
    
    # --- PART 2: THE "VOLATILE / PENNY" DATA (HIGH SCAM RISK) ---
    # These are highly traded, low-priced, or historically volatile Indian stocks 
    # perfect for training your anomaly detection engine.
    "SUZLON.NS",       # Classic high-retail, highly volatile stock
    "YESBANK.NS",      # Historic crash and restructuring 
    "IDEA.NS",         # Vodafone Idea - huge debt, massive volume 
    "GTLINFRA.NS",     # Telecom Infrastructure - classic penny stock 
    "RPOWER.NS",       # Reliance Power - high volume penny stock 
    "SOUTHBANK.NS",    # South Indian Bank 
    "JPPOWER.NS",      # Jaiprakash Power 
    "VAKRANGEE.NS",    # Historically high volatility 
    "PCJEWELLER.NS",   # Massive historic crashes and swings 
    "RTNPOWER.NS",     # RattanIndia Power 
    "UNITECH.NS"       # Real Estate penny stock 
]

def collect_datasets():
    print("📈 STOCKGUARD: BULK DATASET COLLECTOR")
    print("="*60)
    
    # Create a dedicated folder for stock CSVs inside your data folder
    folder_path = "../data/stocks"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_folder_path = os.path.join(script_dir, folder_path)
    
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)
        print(f"📁 Created new directory: {full_folder_path}")

    total_records = 0

    # Loop through each company and download 5 years of data
    for ticker in target_tickers:
        print(f"\n📥 Fetching 5-year history for: {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5y") 
            
            if not hist.empty:
                hist = hist[['Open', 'High', 'Low', 'Close', 'Volume']]
                
                file_name = f"{ticker}_5Y_Data.csv"
                file_path = os.path.join(full_folder_path, file_name)
                hist.to_csv(file_path)
                
                records = len(hist)
                total_records += records
                print(f"   ✅ Saved {records} days of trading data -> {file_name}")
            else:
                print(f"   ❌ No data found for {ticker}. Check the symbol.")
                
        except Exception as e:
            print(f"   ❌ Error downloading {ticker}: {e}")
            
    print("\n" + "="*60)
    print("🎉 MASS DATA COLLECTION COMPLETE")
    print(f"📊 Total Trading Days Collected: {total_records}")
    print(f"💾 All datasets saved in: {full_folder_path}")
    print("="*60)

if __name__ == "__main__":
    collect_datasets()