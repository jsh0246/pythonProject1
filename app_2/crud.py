from sqlalchemy.orm import Session
import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(nickname=user.nickname, gender=user.gender, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_type(db: Session, _id:int = None, nickname: str = None, gender:str=None, age:int=None):
    query = db.query(models.User)

    if _id is not None:
        query = query.filter(models.User.id == _id)
    if nickname is not None:
        query = query.filter(models.User.nickname == nickname)
    if gender is not None:
        query = query.filter(models.User.gender == gender)
    if age is not None:
        query = query.filter(models.User.age == age)

    return query.first()
