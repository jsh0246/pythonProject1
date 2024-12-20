from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(nickname=user.nickname, gender=user.gender, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user