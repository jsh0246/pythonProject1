from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User

app = FastAPI()

# 데이터베이스와 연결을 설정
models.Base.metadata.create_all(bind=database.engine)

# 의존성 주입: 요청마다 데이터베이스 세션을 생성
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user