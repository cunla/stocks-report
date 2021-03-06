from datetime import datetime, date
from typing import Set

import pandas_datareader as pdr
import pandas as pd
from sqlalchemy import func

from db import Session, StockValue, Stock


def db_exists(session: Session, symbol: str, date: str):
    query = session \
        .query(StockValue.date, StockValue.adj_close.label(symbol)) \
        .filter(StockValue.symbol == symbol, StockValue.date == date) \
        .count()
    return query > 0


def update_db(df: pd.DataFrame, **kwargs):
    session = Session()
    columns = kwargs.get('columns', df.columns)
    for index, row in df.iterrows():
        for col in columns:
            if not db_exists(session, col, index):
                stock_value = StockValue(col, index, row[col])
                session.add(stock_value)
    session.commit()
    symbols_min_max = session \
        .query(StockValue.symbol, func.min(StockValue.date), func.max(StockValue.date)) \
        .group_by(StockValue.symbol).all()
    for symbol in symbols_min_max:
        stock = session.query(Stock).filter(Stock.symbol == symbol[0]).first()
        if stock is None:
            stock = Stock(symbol[0])
            session.add(stock)
        stock.min_date = symbol[1]
        stock.max_date = symbol[2]
        stock.last_updated = datetime.today()
    session.commit()
    session.close()


def _get_pdr_data(symbols: Set[str], start_date: date, end_date: date) -> pd.DataFrame:
    """
    gets data from pandas reader
    :param symbols: symbols to get data for
    :param start_date: start date
    :param end_date: end date
    :return: dataframe with data
    """
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    for symbol in symbols:
        df1 = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
        df1 = df1[['Adj Close']]
        df1 = df1.rename(columns={'Adj Close': symbol})
        df = df.join(df1)
    return df


def _get_db_data(symbol: str, start_date: datetime.date, end_date: datetime.date, **kwargs) -> pd.DataFrame:
    session = kwargs.get('session', Session())
    query = session \
        .query(StockValue.date, StockValue.adj_close.label(symbol)) \
        .filter(StockValue.symbol == symbol,
                StockValue.date >= start_date,
                StockValue.date <= end_date)
    df = pd.read_sql(query.statement, session.bind, index_col='date')
    return df


def convert_to_date(x) -> date:
    if isinstance(x, str):
        return datetime.strptime(x, '%Y-%m-%d').date()
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    raise ValueError("Can't convert to date")


def get_data(symbols: Set[str],
             start_date: date,
             end_date: date) -> pd.DataFrame:
    session = Session()
    pdr_needed = False
    start_date = convert_to_date(start_date)
    end_date = convert_to_date(end_date)
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    # try with DB data
    for symbol in symbols:
        df_curr = _get_db_data(symbol, start_date, end_date, session=session)
        if len(df_curr) == 0 or df_curr.index.max() < end_date:
            pdr_needed = True
            break
        df = df.join(df_curr, how='left')

    if pdr_needed:
        df = _get_pdr_data(symbols, start_date, end_date)
        # TODO update DB
        update_db(df, columns=symbols)
        session.commit()
    session.close()
    return df


if __name__ == '__main__':
    # df = generate_report_from_csv('stocks.csv')
    # update_db(df, columns=['AMZN'])
    pass
