from sqlalchemy import Column, Integer, String, Numeric
#from sqlalchemy.orm import relationship
from database import Base

class CurPairs(Base):
	"""
	Stores list of all cur pair table names that
	should be displayed in real time
	"""
	
	__tablename__ = "CurPairs"
	
	id        = Column(Integer, primary_key=True, index=True)
	cur_pair  = Column(String, unique=True, index=True)
	

class EURUSD(Base):
	__tablename__ = "EURUSD"
	
	id   = Column(Integer, primary_key=True, index=True)
	date = Column(String)
	Time = Column(String, unique=True, index=True)
	high = Column(Numeric(1,4)) # 10 digits before and 2 after dec point
	low  = Column(Numeric(1,4)) # be wary of floating calc errors
	ma50 = Column(Numeric(10,2))
	

class Stocks(Base):
	"""
	Stores list of all stocks tables that should be
	displayed in realtime.
	"""
	
	__tablename__ = "Stocks"
	
	id    = Column(Integer, primary_key=True, index=True)
	symbol = Column(String, unique=True, index=True)
	
	
class GOOGL(Base):
	__tablename__ = "GOOGL"
	
	id        = Column(Integer, primary_key=True, index=True)
	date      = Column(String, unique=True, index=True)
	high      = Column(Numeric(4,6))
	low       = Column(Numeric(4,6))
	close     = Column(Numeric(4,6))
	adj_close = Column(Numeric(4,6))
	volume    = Column(Integer)
	
	
# better way to do it - create tables for GOOGL and EURUSD
# in relatime through api?