from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MongoDB cluster
client = MongoClient("mongodb+srv://petwhiz8:VNs3DXlFys93zAzE@cluster1.tdxh1k7.mongodb.net/?retryWrites=true&w=majority")
db = client["stock_prices"]  # Connect to the 'stock_prices' database
collection = db["prices"]  # Connect to the 'prices' collection in the 'stock_prices' database

# Route to serve the latest stock prices
@app.route('/api/stock-prices', methods=['GET'])
def get_stock_prices():
    try:
        # Retrieve the latest stock prices from MongoDB
        stock_prices_document = collection.find_one({}, {'_id': 0, 'prices': 1})  # Exclude _id field from response
        if stock_prices_document:
            return jsonify(stock_prices_document), 200
        else:
            return jsonify({'error': 'No stock prices found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
