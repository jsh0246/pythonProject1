from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# PostgreSQL 연결 설정
DATABASE_URL = "postgressql://postgres:password@localhost:5432/players"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터 모델 정의 (SQLAlchemy 모델)
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# 데이터베이스 초기화 (테이블 생성)
Base.metadata.create_all(bind=engine)

# Pydantic 모델 정의 (데이터 유효성 검사용)
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

# FastAPI 애플리케이션 생성
app = FastAPI()

# 데이터베이스 세션 종속성
class Database:
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_db(self):
        try:
            yield self.db
        finally:
            self.db.close()

# 서비스 클래스 정의 (비즈니스 로직 처리)
class ItemService:
    def __init__(self, db: Session):
        self.db = db

    def create_item(self, item_data: ItemCreate) -> Item:
        db_item = Item(name=item_data.name, description=item_data.description)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get_items(self) -> List[Item]:
        return self.db.query(Item).all()

    def get_item(self, item_id: int) -> Optional[Item]:
        return self.db.query(Item).filter(Item.id == item_id).first()

    def update_item(self, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        db_item = self.get_item(item_id)
        if db_item is None:
            return None
        if item_data.name is not None:
            db_item.name = item_data.name
        if item_data.description is not None:
            db_item.description = item_data.description
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete_item(self, item_id: int) -> bool:
        db_item = self.get_item(item_id)
        if db_item is None:
            return False
        self.db.delete(db_item)
        self.db.commit()
        return True

# FastAPI 라우터 정의
db_instance = Database()

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    db = next(db_instance.get_db())
    item_service = ItemService(db)
    return item_service.create_item(item)

@app.get("/items/", response_model=List[ItemResponse])
def read_items():
    db = next(db_instance.get_db())
    item_service = ItemService(db)
    return item_service.get_items()

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    db = next(db_instance.get_db())
    item_service = ItemService(db)
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate):
    db = next(db_instance.get_db())
    item_service = ItemService(db)
    updated_item = item_service.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    db = next(db_instance.get_db())
    item_service = ItemService(db)
    success = item_service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# 간단한 클라이언트에서 요청을 통해 데이터를 저장하고, 저장된 데이터를 조회, 수정, 삭제할 수 있는 API입니다.
