
from sqlalchemy import Column, Integer, String, Numeric, Date
from db.base import Base, engine


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

