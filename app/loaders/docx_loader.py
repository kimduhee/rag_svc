from docx import Document
from pathlib import Path
from app.core.logging import get_logger

logger = get_logger(__name__)

class DocxLoader:
    
    """
    Word 문서 텍스트 추출
    """
    def load(self, docx_path: str, uuid:str):
        doc = Document(docx_path)

        elements = []
        doc_name = Path(docx_path).stem

        for idx, para in enumerate(doc.paragraphs):

            if para.text.strip():
                elements.append({
                    "uid": uuid,
                    "type": "text",
                    "page": idx,
                    "content": para.text,
                    "doc": doc_name,
                    "images": ""
                })
        
        logger.debug(elements)

        return elements
