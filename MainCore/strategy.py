import pandas as pd



def userstrategy(data):

    dates = pd.date_range(start='2023-03-01', end='2023-12-31')

    closing_prices = [100 + i * 5 for i in range(len(dates))]

    data = pd.DataFrame({'Date': dates, 'Close': closing_prices})



    short_ma = data['Close'].rolling(window=20).mean()

    long_ma = data['Close'].rolling(window=50).mean()



    signals = (short_ma > long_ma).astype(int)



    return signals

