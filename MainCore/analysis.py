import talib
import plotly.graph_objs as go


def calculate_indicator(data, indicator):
    if indicator == 'SMA':
        return talib.SMA(data)
    elif indicator == 'EMA':
        return talib.EMA(data)
    elif indicator == 'RSI':
        return talib.RSI(data)
    elif indicator == 'MACD':
        macd, signal, _ = talib.MACD(data)
        return macd, signal  # Return MACD and its signal line

    elif indicator == 'BollingerBands':
        upper_band, middle_band, lower_band = talib.BBANDS(data)
        return upper_band, middle_band, lower_band  # Return upper, middle, and lower bands
    else:
        raise ValueError(f"Indicator '{indicator}' is not supported.")




def generate_plot(df, indicator_values, indicator_name, stock_symbol):
    trace1 = go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price')
    trace2 = go.Scatter(x=df['Date'], y=indicator_values, mode='lines', name=indicator_name)

    # Candlestick trace
    candlestick = go.Candlestick(x=df['Date'],
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='Candlestick')

    layout = go.Layout(title=f'Technical Analysis for {stock_symbol}',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Value'),
                        template='plotly_dark')

    fig = go.Figure(data=[candlestick, trace1, trace2], layout=layout)
    return fig.to_json()

