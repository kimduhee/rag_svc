import base64
import requests
import pytesseract

from PIL import Image
from app.core.config import settings
from app.llm.prompt import get_image_content
from app.core.logging import get_logger

logger = get_logger(__name__)

"""
LLaVA(멀티모달 LLM)를 사용해 이미지 설명 텍스트를 생성한다.

desc:
    - 현재는 로컬 `http://localhost:11434/api/generate` 엔드포인트(예: Ollama)를 호출한다.
    - 이미지 파일을 base64로 인코딩해 LLaVA 모델에 전달하고, 그 응답을 설명 텍스트로 사용한다.
    - 네트워크 오류나 모델 문제로 실패할 경우 빈 문자열을 반환한다.
Args:
    image_path(str): 이미지 경로로
Returns:
    이미지 설명명
"""

def extract_image_caption(image_path):
    try:
        url = settings.image_llm_url
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")
        
        prompt = get_image_content()

        payload = {
            "model": settings.llm_image_model,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False
        }

        response = requests.post(
            url, 
            json=payload,
            stream=False,
            timeout=(5, 80)
        )

        logger.debug("이미지 설명 내용: %s", response.json()["response"])

        if response.status_code == 200:
            return response.json()["response"].strip()
        return ""

    except Exception as e:
        logger.exception("이미지 설명 오류: %s", e)

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
    except Exception as e:
        logger.exception("OCR 오류: %s", e)

        return ""