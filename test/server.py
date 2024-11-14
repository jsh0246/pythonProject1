from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# 요청 본문을 위한 Pydantic 모델 정의
class Message(BaseModel):
    content: str

# POST 엔드포인트 정의
@app.post("/echo", response_model=Dict[str, str])
async def echo_message(request: Message) -> Dict[str, str]:
    # 클라이언트로부터 받은 메시지를 그대로 반환
    return {"message": request.content}

# uvicorn 명령어로 실행하세요:
# uvicorn server:app --reload