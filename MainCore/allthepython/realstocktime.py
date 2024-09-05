import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time


client = MongoClient("<monogodb><password>")
db = client["stock_prices"]
collection = db["prices"]

def update_stock_price_data(tickers, exchanges, update_interval=10):
    previous_prices = {}  # Store previous prices to detect changes

    while True:
        try:
            stock_prices = {}
            for ticker, exchange in zip(tickers, exchanges):
                url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                soup = BeautifulSoup(response.text, 'html.parser')
                price_element = soup.find(class_='YMlKec fxKbKc')
                if price_element:
                    price = price_element.text.strip()[1:]  # Remove currency symbol
                    stock_prices[f'{exchange}: {ticker}'] = price
                    print(f"Real-time stock price for {exchange}: {ticker}: {price}")
                else:
                    print(f"Price not found for {exchange}: {ticker}")

            # Update the prices in MongoDB
            if stock_prices:
                # Extract only the prices and stock names without the exchange prefix
                prices_data = {}
                for stock, price in stock_prices.items():
                    stock_name = stock.split(': ')[1]  # Extract stock name without exchange prefix
                    prices_data[stock_name] = price
                collection.update_one({}, {"$set": {"prices": prices_data}}, upsert=True)

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")

        time.sleep(update_interval)  # Update the data every specified interval

# Example usage:
tickers = ['IRFC', 'ONGC', 'NBCC', 'ITC']
exchanges = ['NSE', 'NSE', 'NSE', 'NSE']
update_stock_price_data(tickers, exchanges)
