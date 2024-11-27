from sqlalchemy import Column, Integer, String, Text, Date
from database import Base

class QALog(Base):
    __tablename__ = "qa_log"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=False)
    date = Column(Date, nullable=False)