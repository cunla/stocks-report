import json

from sqlalchemy import Column, String, Date, Integer, JSON

from db import Base


class Portfolio(Base):
    __tablename__ = 'portfolios_mix'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(32))
    __mix = Column('mix', JSON)
    last_checked = Column('last_checked', Date)

    def __init__(self, name, mix, **kwargs):
        self.name = name
        self.__mix = mix
        self.last_checked = kwargs.get('last_checked', None)
        self._validate()

    def _validate(self):
        mix = self.mix
        symbols = [k for k in mix]
        percentages = mix.values()
        # if len(percentages) != len(symbols):
        #     raise ValueError(f"Length of percentages list is {len(percentages)}"
        #                      f" while length of symbols is {len(symbols)}")
        # if len(set(symbols)) != len(symbols):
        #     raise ValueError("A portfolio can't contain the same symbol multiple times")
        if sum(percentages) != 1.0:
            raise ValueError(f"Some of percentages should be 1.0 but is {sum(percentages)}")

    @property
    def mix(self):
        return json.loads(self.__mix)

    @property
    def symbols(self):
        return {k for k in self.mix}

    @property
    def percentages(self):
        return list(self.mix.values())
