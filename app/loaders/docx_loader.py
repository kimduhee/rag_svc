from docx import Document
from pathlib import Path

class DocxLoader:
    """
    Word 문서 텍스트 추출
    """

    def load(self, path: str):
        doc = Document(path)
        doc_name = Path(path).stem

        elements = []
        for idx, para in enumerate(doc.paragraphs):
            if para.text.strip():
                elements.append({
                    "type": "text",
                    "page": idx,
                    "content": para.text,
                    "doc": doc_name
                })
        return elements
