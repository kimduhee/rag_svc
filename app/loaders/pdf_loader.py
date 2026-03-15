import pdfplumber
import os

from pathlib import Path
from app.core.config import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.common.utils.image_util import extract_ocr_text
from app.core.logging import get_logger

logger = get_logger(__name__)

class PDFLoader:

    def __init__(self, chunk_size=500, chunk_overlap=50, splitter="recursive"):

        if splitter == "recursive":
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        self.splitter = splitter
        self.text_splitter = text_splitter

    def load(self, pdf_path: str, uuid: str):

        DATA_DIR = Path(settings.base_upload_doc_dir) / uuid / "data"
        IMAGE_DIR = DATA_DIR / "images"

        elements = []
        doc_name = Path(pdf_path).stem

        with pdfplumber.open(pdf_path) as pdf:
            for page_idx, page in enumerate(pdf.pages):

                # 페이지 내에서 추출한 이미지 경로들을 저장해두었다가,
                # 해당 페이지의 텍스트 passage에도 연결해 줄 수 있다.
                page_images = []

                # 1) 페이지에 포함된 모든 이미지를 추출
                for img_idx, img in enumerate(page.images):
                    try:
                        # pdfplumber가 제공하는 이미지 스트림(raw bytes)을 얻어 파일로 저장
                        stream = img["stream"]
                        image_bytes = stream.get_data()
                        image_filename = f"{doc_name}_p{page_idx+1}_img{img_idx+1}.png"
                        image_path = IMAGE_DIR / image_filename

                        os.makedirs(IMAGE_DIR, exist_ok=True)

                        with open(image_path, "wb") as f:
                            f.write(image_bytes)

                        image_path_str = str(image_path)
                        page_images.append(image_path_str)

                        # OCR로 이미지 내 텍스트 추출
                        ocr_text = extract_ocr_text(image_path_str)

                        # 이미지 내용에 대한 자연어 설명(LLaVA)
                        # 실제로 사용하려면 아래 주석을 해제
                        #image_caption = image_caption(image_path_str)
                        image_caption = "이 부분에 이미지에 대한 llm 설명이 들어갑니다."

                        # 이미지 하나를 하나의 passage로 저장
                        elements.append({
                            "uid": uuid,
                            "type": "image",
                            "page": str(page_idx + 1),
                            "content": f"""
        [Image]
        text: {ocr_text}
        description: {image_caption}
        [/Image]
        """,
                            "doc": doc_name,
                            "images": [image_path_str]
                        })
                    except Exception as e:
                        # 개별 이미지 처리에 실패해도 전체 파이프라인은 계속 진행
                        logger.debug("이미지 처리 실패: %s", e)

                # 2) 페이지의 텍스트 추출
                text = page.extract_text()
                if text and text.strip():
                    # LangChain Document 리스트로 분할 후 content만 꺼내서 사용
                    docs = self.text_splitter.create_documents([text])
                    chunks = [d.page_content for d in docs]

                    for chunk in chunks:
                        # 각 텍스트 조각도 하나의 passage로 elements에 추가
                        elements.append({
                            "uid": uuid,
                            "type": "text",
                            "page": str(page_idx + 1),
                            "content": chunk,
                            "doc": doc_name,
                            # 같은 페이지에서 추출한 이미지들을 연결해 두면,
                            # 검색 후 결과를 보여줄 때 관련 이미지를 함께 노출할 수 있다.
                            "images": page_images
                        })

        return elements
