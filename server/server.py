from pymongo import MongoClient
import yfinance as yf
from datetime import datetime, timezone
import time
import schedule
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mongo_uri = os.getenv('MONGO_CONNECTION_STRING')
client = MongoClient(mongo_uri)
db = client[os.getenv('DATABASE_NAME')]
stock_collection = db[os.getenv('STOCK_COLLECTION')]

def fetch_and_update_stocks(stock_symbols):
    try:
        # Fetch stock data using yfinance
        stock_data = yf.download(stock_symbols, group_by='ticker', threads=True)
        
        updates = []
        for symbol in stock_symbols:
            if symbol in stock_data:
                last_price = stock_data[symbol]['Close'].iloc[-1]
                updates.append({
                    "symbol": symbol,
                    "price": last_price,
                    "timestamp": datetime.now(timezone.utc)
                })
        
        return updates
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return []

def update_database(stock_updates):
    try:
        for update in stock_updates:
            stock_collection.update_one(
                {"symbol": update["symbol"]},
                {"$set": {"price": update["price"], "timestamp": update["timestamp"]}},
                upsert=True
            )
        print(f"Successfully updated {len(stock_updates)} stocks.")
    except Exception as e:
        print(f"Error updating database: {e}")

def job():
    stock_updates = fetch_and_update_stocks(stock_symbols)
    if stock_updates:
        update_database(stock_updates)

# List of stock symbols to monitor
stock_symbols = ["AAPL", "MSFT", "GOOGL"]  # Eventually will pull list from elsewhere (db or .txt file)

# Schedule the job to run every minute
schedule.every(.05).minutes.do(job)

if __name__ == "__main__":
    print("Starting stock update service...")
    while True:
        schedule.run_pending()
        time.sleep(1)
