import csv
import os
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# ==========================================
# 🔐 YOUR CONFIGURATION
# ==========================================
api_id = '36509846'          # Your ID
api_hash = 'f9c22709ccdf7ac867ee53de6411da19'   # Your Hash
phone = '+919042996204'      # Your Phone

# LIST OF CHANNELS TO SCRAPE
# (Add the usernames of the groups you joined here)
target_channels = [
   'https://t.me/Equity_Swing_Positional_Calls',
   'https://t.me/Intraday_Trading_Calls_Stock',
   'https://t.me/Stocks_Markets'
]

session_name = 'stockguard_collector_session'

async def main():
    print("🔵 Connecting to Telegram...")
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start(phone)
    print("✅ Connected!")

    # Prepare the CSV file
    output_file = 'data/telegram_dataset.csv'
    
    # Create 'data' folder if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Open file to write data
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Channel', 'Sender', 'Message']) # Header

        print(f"🚀 Starting Data Collection from {len(target_channels)} channels...")
        
        total_count = 0

        for channel in target_channels:
            try:
                print(f"   📥 Scraping: @{channel}...")
                entity = await client.get_entity(channel)
                
                # Download last 500 messages per channel
                async for msg in client.iter_messages(entity, limit=500):
                    if msg.text:
                        # Clean the text (remove newlines for CSV)
                        clean_text = msg.text.replace('\n', ' ').replace('\r', '')
                        
                        writer.writerow([
                            msg.date, 
                            channel, 
                            msg.sender_id, 
                            clean_text
                        ])
                        total_count += 1
                        
            except Exception as e:
                print(f"   ❌ Error scraping {channel}: {e}")

    print("="*50)
    print(f"✅ MISSION COMPLETE")
    print(f"📊 Total Messages Collected: {total_count}")
    print(f"💾 Saved to: {output_file}")
    print("="*50)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())