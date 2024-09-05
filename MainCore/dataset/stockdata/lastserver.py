import pandas as pd
from flask import Flask, request, jsonify
import plotly.graph_objs as go
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)


model = load_model('thebiggmachine.h5')
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])  # Compile the model with metrics
scaler = MinMaxScaler(feature_range=(0, 1))

# Function to load and describe dataset
def load_and_describe_dataset(stock_name):
    try:
        df = pd.read_csv(f"{stock_name}.csv")
        description = df.describe()
        # Convert description to dictionary of numerical values
        description_dict = description.to_dict()
        for key in description_dict:
            for sub_key in description_dict[key]:
                # Convert each value to float
                description_dict[key][sub_key] = float(description_dict[key][sub_key])
        return {'success': True, 'description': description_dict}
    except FileNotFoundError:
        return {'success': False, 'message': 'Dataset not found for the given stock name.'}

# Function to generate candlestick plot with Plotly
def generate_candlestick_plot(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                          open=df['Open'],
                                          high=df['High'],
                                          low=df['Low'],
                                          close=df['Close'])])
    fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price', template='plotly_dark')
    return fig.to_json()

# Function to generate Moving Average plot with Plotly
def generate_ma_plot(df):
    df['MA_100'] = df['Close'].rolling(window=100).mean()
    df['MA_200'] = df['Close'].rolling(window=200).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_100'], mode='lines', name='100-day Moving Average'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_200'], mode='lines', name='200-day Moving Average'))
    fig.add_trace(go.Candlestick(x=df['Date'],
                                  open=df['Open'],
                                  high=df['High'],
                                  low=df['Low'],
                                  close=df['Close'],
                                  name='Candlestick'))
    fig.update_layout(title='Moving Averages', xaxis_title='Date', yaxis_title='Price',template='plotly_dark')
    return fig.to_json()

# Function to generate Prediction vs Real Price plot
def generate_prediction_vs_real_plot(y_test, y_predicted, dates):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=y_test.flatten(), mode='lines', name='Real Price'))
    fig.add_trace(go.Scatter(x=dates, y=y_predicted.flatten(), mode='lines', name='Predicted Price'))
    fig.add_trace(go.Candlestick(x=dates,
                                  open=y_test.flatten(),
                                  high=y_test.flatten(),
                                  low=y_test.flatten(),
                                  close=y_test.flatten(),
                                  name='Candlestick'))
    fig.update_layout(title='Prediction vs Real Price', xaxis_title='Time', yaxis_title='Price',template='plotly_dark')
    return fig.to_json()

# Endpoint to receive stock name input and perform describe()
@app.route('/get_stock_description', methods=['POST'])
def get_stock_description():
    stock_name = request.json['stock_name']
    result = load_and_describe_dataset(stock_name)
    return jsonify(result)

# Endpoint to generate and return plots
@app.route('/get_plots', methods=['POST'])
def get_plots():
    stock_name = request.json['stock_name']
    df = pd.read_csv(f"{stock_name}.csv")
    candlestick_plot = generate_candlestick_plot(df)
    ma_plot = generate_ma_plot(df)

    # Prepare data for prediction
    data_training = pd.DataFrame(df['Close'][0:int(len(df) * 0.70)])
    data_testing = pd.DataFrame(df['Close'][int(len(df) * 0.70): int(len(df))])
    past_100_days = data_training.tail(100)
    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
    input_data = scaler.fit_transform(final_df)

    x_test = []
    y_test = []

    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i - 100: i])
        y_test.append(input_data[i, 0])

    x_test, y_test = np.array(x_test), np.array(y_test)

    # Perform prediction
    y_predicted = model.predict(x_test)

    # Rescale predictions and actual values
    y_predicted_rescaled = scaler.inverse_transform(y_predicted)
    y_test_rescaled = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Generate Prediction vs Real Price plot
    dates = df['Date'][-len(y_test_rescaled):]  # Ensure dates match the length of the test data
    prediction_vs_real_plot = generate_prediction_vs_real_plot(y_test_rescaled, y_predicted_rescaled, dates)

    return jsonify({
        'success': True,
        'candlestick_plot': candlestick_plot,
        'ma_plot': ma_plot,
        'prediction_vs_real_plot': prediction_vs_real_plot
    })

if __name__ == '__main__':
    app.run(port=5004, debug=True)
