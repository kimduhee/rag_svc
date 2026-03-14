import base64
import requests
import pytesseract

from PIL import Image
from app.core.config import settings

def image_caption(image_path):
    """
    LLaVA(멀티모달 LLM)를 사용해 이미지 설명 텍스트를 생성한다.

    - 현재는 로컬 `http://localhost:11434/api/generate` 엔드포인트(예: Ollama)를 호출한다.
    - 이미지 파일을 base64로 인코딩해 LLaVA 모델에 전달하고, 그 응답을 설명 텍스트로 사용한다.
    - 네트워크 오류나 모델 문제로 실패할 경우 빈 문자열을 반환한다.
    """
    url = settings.image_llm_url
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
    prompt = """
    이 이미지를 자세히 설명하세요.
    표라면 표의 내용도 요약하세요.
    그래프라면 축과 수치 의미를 설명하세요.
    """
    payload = {
        "model": settings.llm_image_model,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["response"].strip()
    return ""

def extract_ocr_text(image_path):
    """
    Tesseract OCR을 이용해 이미지 안의 텍스트를 추출한다.

    - 언어는 한국어+영어(`kor+eng`) 조합으로 설정
    - OCR 중 예외가 발생하면 전체 파이프라인이 중단되지 않도록 빈 문자열을 반환
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="kor+eng")
        return text.strip()
    except Exception:
        return ""