import requests

class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_message(self, message: str) -> str:
        # 서버로 전송할 데이터 정의
        data = {"content": message}
        # 서버에 POST 요청 전송
        response = requests.post(f"{self.base_url}/echo", json=data)
        # 응답을 JSON으로 파싱 후 message 값 반환

        #print(response.json())

        return response.json()

    def get_players(self):
        # 서버에 GET 요청 전송하여 players 데이터 조회

        ##### 여기서 오류  get이 안됨
        response = requests.get(f"{self.base_url}/read")
        # 응답을 JSON으로 파싱 후 반환
        #return response.json()

        #print("Response status code:", response.status_code)
        #print("Response content:", response.text)

        if response.status_code == 200:
            try:
                return response.json()
                #return response
            except requests.exceptions.JSONDecodeError:
                print("JSONDecodeError: The response is not a valid JSON format.")
                return None
        else:
            print(f"Error: Received status code {response.status_code}")
            return None



# EchoClient 인스턴스 생성 및 서버와 통신
client = Client("http://127.0.0.1:8000")

# /echo 엔드포인트 사용 예시
echoed_message = client.send_message("Hello, FastAPI!")
print(echoed_message)

# /read 엔드포인트 사용 예시
players = client.get_players()
#print(players)

for row in players:
    # print(row)
    print(f"ID: {row['id']:<4} Name: {row['name']:<20} Age: {row['age']:<5}")