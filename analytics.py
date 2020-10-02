import pandas as pd
from datetime import datetime, timedelta

from db_model import get_data


def rolling_bands(df_stocks: pd.DataFrame, **kwargs):
    column_name = kwargs.get('column_name', 'portfolio')
    rolling_mean_portfolio = df_stocks[column_name].rolling(20).mean()
    rolling_std_portfolio = df_stocks[column_name].rolling(20).std()

    rolling_bands_df = df_stocks
    rolling_bands_df['Upper'] = rolling_mean_portfolio + (rolling_std_portfolio * 2)
    rolling_bands_df['Lower'] = rolling_mean_portfolio - (rolling_std_portfolio * 2)
    rolling_bands_df[column_name] = df_stocks[column_name]

    return rolling_bands_df


if __name__ == '__main__':
    stock_name = 'AMZN'
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=90)
    start_date = start_date
    df = get_data({stock_name}, start_date, end_date)
    rolling_bands_df = rolling_bands(df, column_name=stock_name)
    rolling_bands_df.to_csv('stocks.csv')
