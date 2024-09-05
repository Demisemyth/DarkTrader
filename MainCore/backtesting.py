from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import threading
import logging
import plotly.graph_objs as go
import numpy as np

app = Flask(__name__)
CORS(app)

# Lock for synchronizing file writes
file_lock = threading.Lock()

def fetch_stock_data(stock_name):
    try:
        # Define the file path based on the stock name
        file_path = f'dataset/backdata/{stock_name}.csv'
        print(stock_name)
        print(file_path)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file for stock '{stock_name}' not found.")

def generate_chart(df, strategy_result):
    try:
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Create candlestick trace with increased size
        candlestick = go.Candlestick(x=df['Date'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     name='Candlestick',
                                     increasing=dict(line=dict(color='green', width=1.5)),
                                     decreasing=dict(line=dict(color='red', width=1.5)))

        # Initialize lists to store buy and sell signals
        buy_signals = []
        sell_signals = []

        # Iterate over strategy results
        for i, signal in enumerate(strategy_result):
            if i < len(df):  # Check if index is within the bounds of the DataFrame
                if signal == 1:
                    buy_signals.append(df['High'].iloc[i])  # Buy signal at high price
                    sell_signals.append(None)  # No sell signal
                else:
                    buy_signals.append(None)  # No buy signal
                    sell_signals.append(df['Low'].iloc[i])  # Sell signal at low price

        # Create traces for buy and sell signals
        trace_buy = go.Scatter(x=df['Date'], y=buy_signals, mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up', size=7))
        trace_sell = go.Scatter(x=df['Date'], y=sell_signals, mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down', size=7))

        # Create the figure
        fig = go.Figure(data=[candlestick, trace_buy, trace_sell])

        # Define frames for animation
        frames = []
        for i in range(len(df)):
            # Candlestick frame with increased size
            frame_data = go.Candlestick(x=df['Date'].iloc[:i+1],
                                        open=df['Open'].iloc[:i+1],
                                        high=df['High'].iloc[:i+1],
                                        low=df['Low'].iloc[:i+1],
                                        close=df['Close'].iloc[:i+1],
                                        increasing=dict(line=dict(color='green', width=1.5)),
                                        decreasing=dict(line=dict(color='red', width=1.5)))
            frames.append(go.Frame(data=[frame_data]))

        # Add frames to the figure for animation
        fig.frames = frames

        # Update layout
        fig.update_layout(title='Candlestick Chart with Buy/Sell Signals',
                          xaxis_title='Date',
                          yaxis_title='Price',
                          template='plotly_dark',
                          updatemenus=[dict(type='buttons',
                                            buttons=[dict(label='Play',
                                                          method='animate',
                                                          args=[None, dict(frame=dict(duration=100, redraw=True),
                                                                           fromcurrent=True)])],
                                            direction='left',
                                            x=1.1,
                                            y=-0.6,
                                            xanchor='right',
                                            yanchor='bottom'
                                           )
                                      ])

        # Serialize the figure to JSON
        chart_json = fig.to_json()

        return chart_json
    except Exception as e:
        return str(e)

# Function to calculate buy and sell signal counts
def calculate_buy_sell_counts(strategy_result):
    buy_count = strategy_result.count(1)
    sell_count = strategy_result.count(-1)
    return buy_count, sell_count

@app.route('/upload', methods=['POST'])
def upload_strategy():
    try:
        # Get strategy code and stock name from the request
        strategy_code = request.json.get('strategyCode')
        stock_name = request.json.get('stockName')

        # Sanitize stock name
        stock_name = stock_name.strip()

        # Validate stock name
        if not stock_name:
            return jsonify({'error': 'Stock name cannot be empty'}), 400

        # Clear the contents of the strategy.py file before writing the new code
        with file_lock:
            with open('strategy.py', 'w') as f:
                f.write('')  # This effectively clears the file

            # Write the new strategy code to strategy.py file
            with open('strategy.py', 'w') as f:
                f.write(strategy_code)

        # Fetch stock data based on the provided stock name
        df = fetch_stock_data(stock_name)

        # Execute user's strategy
        from strategy import userstrategy
        strategy_result = userstrategy(df)
        strategy_result_list = strategy_result.tolist()

        # Calculate buy and sell signal counts
        buy_count, sell_count = calculate_buy_sell_counts(strategy_result)

        # Print the buy and sell signal counts
        print("Buy Count:", buy_count)
        print("Sell Count:", sell_count)

        # Return the strategy result, buy and sell counts as JSON
        return jsonify({'strategyResult': strategy_result_list, 'buyCount': buy_count, 'sellCount': sell_count}), 200
    except FileNotFoundError:
        return jsonify({'error': f"CSV file for stock '{stock_name}' not found."}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/chart', methods=['GET'])
def display_chart():
    try:
        # Get stock name from the request
        stock_name = request.args.get('stockName')

        # Sanitize stock name
        stock_name = stock_name.strip()

        # Fetch stock data based on the provided stock name
        df = fetch_stock_data(stock_name)

        # Execute user's strategy
        from strategy import userstrategy
        strategy_result = userstrategy(df)

        # Calculate buy and sell signal counts
        buy_count, sell_count = calculate_buy_sell_counts(strategy_result)

        # Generate chart
        chart_json = generate_chart(df, strategy_result.tolist())

        # Return the chart JSON and buy/sell counts to the client
        return jsonify({'chart': chart_json, 'buyCount': buy_count, 'sellCount': sell_count}), 200
    except FileNotFoundError:
        return jsonify({'error': f"CSV file for stock '{stock_name}' not found."}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5002, debug=True)
