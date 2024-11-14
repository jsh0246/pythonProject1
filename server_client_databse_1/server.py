from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Union
from fastapi import HTTPException

from db_service import DBService

class Message(BaseModel):
    content: str

class Server:
    def __init__(self):
        # FastAPI 인스턴스 생성
        self.app = FastAPI()
        # 데이터베이스 서비스 인스턴스 생성
        self.db_service = DBService()
        # 엔드포인트 설정
        self._setup_routes()

    def _setup_routes(self):
        # /echo 엔드포인트에 대한 POST 요청 핸들러
        @self.app.post("/echo", response_model=Dict[str, str])
        async def echo_message(request: Message) -> Dict[str, str]:
            return {"message": request.content}

        # /read 엔드포인트에 대한 GET 요청 핸들러
        @self.app.get("/read", response_model=List[Dict[str, Union[str, int]]])
        async def read_data():

            try:
                # 데이터베이스에서 데이터 조회
                rows = self.db_service.read()
                #print("Rows debug here : ", rows)

                if rows is None:
                    return []
                # 조회한 데이터를 JSON 형식으로 변환하여 반환
                #return rows

                #print("dffffffffffffffffffff")
                return [{"id": row[0], "name": row[1], "age": row[2]} for row in rows]
            except Exception as e:
                print(f"Server error: {e}")
                raise HTTPException(status_code=500, detail="Internal Server Error")


    def get_app(self):
        # FastAPI 애플리케이션 반환
        return self.app


# EchoServer 인스턴스 생성 및 FastAPI 애플리케이션 반환
echo_server = Server()
app = echo_server.get_app()