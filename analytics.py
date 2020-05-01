import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta

def get_data(symbols, start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    for symbol in symbols:
        df1 = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
        df1 = df1[['Adj Close']]
        df1 = df1.rename(columns={'Adj Close': symbol})
        df = df.join(df1)
    df.dropna(inplace=True)
    return df


def rolling_bands(df_stocks: pd.DataFrame, **kwargs):
    column_name = kwargs.get('column_name', 'portfolio')
    rolling_mean_portfolio = df_stocks[column_name].rolling(20).mean()
    rolling_std_portfolio = df_stocks[column_name].rolling(20).std()

    rolling_bands_df = pd.DataFrame()
    rolling_bands_df['Upper'] = rolling_mean_portfolio + (rolling_std_portfolio * 2)
    rolling_bands_df['Lower'] = rolling_mean_portfolio - (rolling_std_portfolio * 2)
    rolling_bands_df['Actual'] = df_stocks[column_name]

    return rolling_bands_df


if __name__ == '__main__':
    stock_name = 'AAPL'
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = datetime.today() - timedelta(days=90)
    start_date = start_date.strftime('%Y-%m-%d')
    df = get_data([stock_name], start_date, end_date)
    rolling_bands_df = rolling_bands(df, column_name=stock_name)
