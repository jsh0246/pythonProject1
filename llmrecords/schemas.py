from pydantic import BaseModel
from typing import Optional
import datetime

class QALogBase(BaseModel):
    question: str
    answer: str
    date: Optional[datetime.date]

class QALogCreate(QALogBase):
    pass

class QALogResponse(QALogBase):
    id: int

    class Config:
        from_attributes = True