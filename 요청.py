import requests

# 업로드할 이미지 파일 경로
image_path = "KakaoTalk_20250411_005707888.jpg"

# API 서버 주소
url = "http://localhost:8000/analyze"

# 전송 데이터 준비
with open(image_path, "rb") as img_file:
    files = {
        "image": ("example_face.jpg", img_file, "image/jpeg")
    }
    data = {
        "query": "upper_body"
    }

    # POST 요청 전송
    response = requests.post(url, files=files, data=data)

# 결과 출력
if response.status_code == 200:
    result = response.json()
    print("퍼스널컬러:", result["personal_color"])
    print("추천 옷 목록:", result["recommendations"])
else:
    print("오류 발생:", response.text)
