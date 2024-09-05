from flask import Flask, request, jsonify
import pandas as pd
import os
from analysis import calculate_indicator, generate_plot
from  flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load historical stock data from CSV files
data_dir = "dataset/stockdata"
stocks = ['TCS','ZEEL', 'WIPRO', 'VEDL', 'UPL', 'ULTRACEMCO', 'TITAN', 'TECHM', 'TCS', 'TATAMOTORS', 'SUNPHARMA', 'ONGC', 'NTPC', 'NIFTY50_all', 'IOC','NBCC','ITC']
stock_data = {}
for stock in stocks:
    file_path = os.path.join(data_dir, f"{stock}.csv")
    stock_data[stock] = pd.read_csv(file_path)

@app.route('/plot', methods=['POST'])
def plot_technical_analysis():
    stock_symbol = request.form.get('symbol')
    indicator = request.form.get('indicator')
    num_candlesticks = int(request.form.get('candlesticks', 20))

    if stock_symbol not in stocks:
        return jsonify({'error': f'Stock symbol {stock_symbol} not found'}), 404
    if indicator not in ['SMA', 'EMA', 'RSI', 'MACD', 'BollingerBands']:
        return jsonify({'error': f'Indicator {indicator} not supported'}), 400


    df = stock_data[stock_symbol]


    df = df[-num_candlesticks:]


    close_prices = df['Close'].values
    indicator_values = calculate_indicator(close_prices, indicator)

    plot_json = generate_plot(df, indicator_values, indicator, stock_symbol)

    return jsonify({'plot': plot_json})


if __name__ == '__main__':
    app.run(port=5001, debug=True)
