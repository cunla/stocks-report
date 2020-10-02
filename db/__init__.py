from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
engine = create_engine("sqlite:///db.sqlite")
Session = sessionmaker(bind=engine)

Base = declarative_base()

from .portfolio_model import *
from .stock_model import *

Base.metadata.create_all(engine, checkfirst=True)
