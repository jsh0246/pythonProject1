from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'testusers'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True, index=True)
    gender = Column(String)
    age = Column(Integer)