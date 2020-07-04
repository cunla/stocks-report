from datetime import datetime
from operator import and_
from typing import List

import pandas_datareader as pdr
from sqlalchemy import Column, Integer, String, Numeric, Date, func
import pandas as pd
from db.base import Base, engine, Session
from generate_graph import generate_report_from_csv


class Stock(Base):
    __tablename__ = 'symbols_tracked'
    symbol = Column('symbol', String(32), primary_key=True)
    min_date = Column('min_date', Date)
    max_date = Column('max_date', Date)
    last_updated = Column('last_updated', Date)

    def __init__(self, symbol, **kwargs):
        self.symbol = symbol
        self.min_date = kwargs.get('min_date', None)
        self.max_date = kwargs.get('max_date', None)


class StockValue(Base):
    __tablename__ = 'symbol_values'
    id = Column(Integer, primary_key=True)
    symbol = Column('symbol', String(32))
    date = Column('date', Date)
    adj_close = Column('adj_close', Numeric)

    def __init__(self, symbol, date, val):
        self.symbol = symbol
        self.date = date
        self.adj_close = val

    def __str__(self):
        return f'{self.date} - {self.symbol} - {self.adj_close}'


Base.metadata.create_all(engine)


def update_db(df: pd.DataFrame, **kwargs):
    session = Session()
    columns = kwargs.get('columns', df.columns)
    for index, row in df.iterrows():
        for col in columns:
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


def _get_pdr_data(symbols: List[str], start_date: str, end_date: str) -> pd.DataFrame:
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


def get_data(symbols: List[str], start_date_str: str, end_date_str: str) -> pd.DataFrame:
    session = Session()
    pdr_needed = False
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    # try with DB data
    for symbol in symbols:
        df_curr = _get_db_data(symbol, start_date, end_date, session=session)
        if df_curr.index.max() < end_date:
            pdr_needed = True
            break
        df.join(df_curr)

    if pdr_needed:
        df = _get_pdr_data(symbols, start_date_str, end_date_str)
        # TODO update DB
        update_db(df, columns=symbols)
        session.commit()
    session.close()
    return df


if __name__ == '__main__':
    # df = generate_report_from_csv('stocks.csv')
    # update_db(df, columns=['AMZN'])
    pass
