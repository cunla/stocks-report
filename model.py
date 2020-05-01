from datetime import datetime

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


if __name__ == '__main__':
    df = generate_report_from_csv('stocks.csv')
    update_db(df, columns=['AMZN'])
