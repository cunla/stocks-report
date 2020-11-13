import json
from typing import Dict

from sqlalchemy import Column, String, Date, Integer, JSON

from db import Base, Session


class Portfolio(Base):
    """
    Contains a portfolio in json format:
    {
            "FB": 0.2,
            "AMZN": 0.2,
            "GOOG": 0.2,
            "AAPL": 0.3,
            "TSLA": 0.2,
    }
    """
    __tablename__ = 'portfolios_mix'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(32), unique=True)
    __mix = Column('mix', JSON)
    last_checked = Column('last_checked', Date)

    def __init__(self, name, mix_str, **kwargs):
        self._validate(mix_str)
        self.name = name
        self.__mix = mix_str
        self.last_checked = kwargs.get('last_checked', None)

    def _validate(self, mix_str: str):
        mix = json.loads(mix_str)
        values = mix.values()
        if any(val != int(val) for val in values) and sum(values) != 1.0:
            raise ValueError(f"Some of percentages should be 1.0 but is {sum(values)}")

    @property
    def mix(self):
        return json.loads(self.__mix)

    @property
    def symbols(self):
        return {k for k in self.mix}

    @property
    def percentages(self):
        return list(self.mix.values())

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'mix': self.mix}

    @staticmethod
    def create(name: str, mix):
        session = Session()
        portfolio = Portfolio(name, json.dumps(mix) if isinstance(mix, dict) else mix)
        session.add(portfolio)
        session.commit()
        return portfolio

    @staticmethod
    def delete(name: str):
        session = Session()
        session.query(Portfolio).filter(Portfolio.name == name).delete()
        session.commit()

    @staticmethod
    def get(p_id: int):
        session = Session()
        portfolio = session.query(Portfolio).get(p_id)
        return portfolio

    @staticmethod
    def list(query: str):
        session = Session()
        query = f"%{query}%"
        portfolios = session.query(Portfolio).filter(Portfolio.name.like(query)).all()
        return portfolios

    @staticmethod
    def update(old_name: str, name: str, mix: Dict):
        session = Session()
        portfolio = session.query(Portfolio).filter(Portfolio.name == old_name)
        portfolio.update({'name': name, 'mix': mix})
        session.commit()
        return portfolio
