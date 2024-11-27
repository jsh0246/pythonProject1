from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import QALog
from schemas import QALogCreate, QALogResponse
from typing import List

import datetime

# FastAPI 인스턴스 생성
app = FastAPI()

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# CREATE: 새로운 QA 로그 추가
@app.post("/qa_logs/", response_model=QALogResponse)
def create_qa_log(qa_log: QALogCreate, db: Session = Depends(get_db)):
    db_qa_log = QALog(
        question=qa_log.question,
        answer=qa_log.answer,
        date=qa_log.date if qa_log.date else datetime.date.today()
    )
    db.add(db_qa_log)
    db.commit()
    db.refresh(db_qa_log)
    return db_qa_log

# READ: 모든 QA 로그 조회
@app.get("/qa_logs/", response_model=List[QALogResponse])
def read_qa_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(QALog).offset(skip).limit(limit).all()
    return logs

# READ: 특정 ID의 QA 로그 조회
@app.get("/qa_logs/{qa_log_id}", response_model=QALogResponse)
def read_qa_log(qa_log_id: int, db: Session = Depends(get_db)):
    log = db.query(QALog).filter(QALog.id == qa_log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log


# UPDATE: 특정 QA 로그 수정
@app.put("/qa_logs/{qa_log_id}", response_model=QALogResponse)
def update_qa_log(qa_log_id: int, qa_log: QALogCreate, db: Session = Depends(get_db)):
    db_log = db.query(QALog).filter(QALog.id == qa_log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")

    # 업데이트할 필드를 설정
    db_log.question = qa_log.question
    db_log.answer = qa_log.answer
    db_log.date = qa_log.date if qa_log.date else db_log.date

    db.commit()
    db.refresh(db_log)
    return db_log


# DELETE: 특정 QA 로그 삭제
@app.delete("/qa_logs/{qa_log_id}")
def delete_qa_log(qa_log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(QALog).filter(QALog.id == qa_log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(db_log)
    db.commit()
    return {"detail": "Log deleted successfully"}