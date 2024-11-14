import requests

class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_message(self, message: str) -> str:
        # 서버로 전송할 데이터 정의
        data = {"content": message}
        # 서버에 POST 요청 전송
        response = requests.post(f"{self.base_url}/echo", json=data)

        # 응답 확인 및 반환
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

# EchoClient 인스턴스 생성 및 서버와 통신
client = Client("http://127.0.0.1:8000")

# /echo 엔드포인트 사용 예시
echoed_message = client.send_message("Hello, FastAPI!")
print("Server Response:", echoed_message)
