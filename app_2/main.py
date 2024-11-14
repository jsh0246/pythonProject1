from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud
from database import engine, Base, get_db

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/{_type}", response_model=schemas.User)
def read_user_by_type(_type: str, col: Union[str, int], db: Session = Depends(get_db)):

    if _type == "id":
        db_user = crud.get_user_by_type(db=db, _id=col)
        print(1)
    if _type == "nickname":
        db_user = crud.get_user_by_type(db=db, nickname=col)
        print(2)
    if _type == "gender":
        db_user = crud.get_user_by_type(db=db, gender=col)
        print(3)
    if _type == "age":
        db_user = crud.get_user_by_type(db=db, age=col)
        print(4)

    print(5)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user