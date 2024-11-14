import requests

class EchoClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_message(self, message: str) -> str:
        # 서버로 전송할 데이터 정의
        data = {"message": message}
        # 서버에 POST 요청 전송
        response = requests.post(f"{self.base_url}/echo", json=data)
        # 응답을 JSON으로 파싱 후 message 값 반환
        return response.json().get("message")

    def get_players(self):
        # 서버에 GET 요청 전송하여 players 데이터 조회
        response = requests.get(f"{self.base_url}/read")
        # 응답을 JSON으로 파싱 후 반환
        return response.json()

# EchoClient 인스턴스 생성 및 서버와 통신
client = EchoClient("http://127.0.0.1:8000")

# /echo 엔드포인트 사용 예시
# echoed_message = client.send_message("Hello, FastAPI!")
# print(echoed_message)

# /read 엔드포인트 사용 예시
players = client.get_players()
print(players)