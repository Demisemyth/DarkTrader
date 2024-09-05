from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import threading
import logging
import plotly.graph_objs as go
app = Flask(__name__)
CORS(app)
file_lock = threading.Lock()
def fetch_stock_data(stock_name):
    try:
        file_path = f'dataset/backdata/{stock_name}.csv'
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file for stock '{stock_name}' not found.")
def generate_chart(df, strategy_result):
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        candlestick = go.Candlestick(x=df['Date'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     name='Candlestick',
                                     increasing=dict(line=dict(color='green', width=1.5)),
                                     decreasing=dict(line=dict(color='red', width=1.5)))
        buy_signals = []
        sell_signals = []
        for i, signal in enumerate(strategy_result):
            if i < len(df):
                if signal == 1:
                    buy_signals.append(df['High'].iloc[i])
                    sell_signals.append(None)
                else:
                    buy_signals.append(None)
                    sell_signals.append(df['Low'].iloc[i])
        trace_buy = go.Scatter(x=df['Date'], y=buy_signals, mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up', size=7))
        trace_sell = go.Scatter(x=df['Date'], y=sell_signals, mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down', size=7))
        fig = go.Figure(data=[candlestick, trace_buy, trace_sell])


        frames = []
        for i in range(len(df)):

            frame_data = go.Candlestick(x=df['Date'].iloc[:i+1],
                                        open=df['Open'].iloc[:i+1],
                                        high=df['High'].iloc[:i+1],
                                        low=df['Low'].iloc[:i+1],
                                        close=df['Close'].iloc[:i+1],
                                        increasing=dict(line=dict(color='green', width=1.5)),
                                        decreasing=dict(line=dict(color='red', width=1.5)))
            frames.append(go.Frame(data=[frame_data]))


        fig.frames = frames


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

        # Return the strategy result as JSON
        return jsonify({'strategyResult': strategy_result_list}), 200
    except FileNotFoundError:
        return jsonify({'error': f"CSV file for stock '{stock_name}' not found."}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['GET'])
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

        # Generate chart
        chart_json = generate_chart(df, strategy_result.tolist())

        # Return the chart JSON to the client
        return jsonify({'chart': chart_json}), 200
    except FileNotFoundError:
        return jsonify({'error': f"CSV file for stock '{stock_name}' not found."}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)
