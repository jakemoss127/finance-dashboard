from pymongo import MongoClient
import yfinance as yf
from datetime import datetime, timezone
import time
import schedule
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request

# Load environment variables from .env file
load_dotenv()

# Set up Flask
app = Flask(__name__)

# Set up MongoDB connection
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

@app.route('/api/stocks/<symbol>', methods=['GET'])
def get_stock(symbol):
    try:
        stock = stock_collection.find_one({"symbol": symbol.upper()})
        if stock:
            return jsonify({
                "symbol": stock["symbol"],
                "price": stock["price"],
                "timestamp": stock["timestamp"]
            })
        else:
            return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

def job():
    stock_updates = fetch_and_update_stocks(stock_symbols)
    if stock_updates:
        update_database(stock_updates)

# List of stock symbols to monitor
stock_symbols = ["AAPL", "MSFT", "GOOGL"]  # Eventually will pull list from elsewhere (db or .txt file)

# Schedule the job to run every minute
schedule.every(.5).minutes.do(job)

if __name__ == "__main__":
    print("Starting stock update service...")

    # Start the scheduled job in a separate thread or process
    import threading
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Start Flask application
    app.run(port=5000, debug=True)
