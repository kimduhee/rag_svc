import openpyxl
from app.core.config import settings
from pathlib import Path
from app.core.logging import get_logger

logger = get_logger(__name__)

class ExcelLoader:
    """
    Excel → 시트별 텍스트 테이블화
    """
    def load(self, excel_path: str, uuid:str):
        wb = openpyxl.load_workbook(excel_path)

        #DATA_DIR = Path(settings.base_upload_doc_dir) / uuid / "data"
        #IMAGE_DIR = DATA_DIR / "images"

        elements = []
        doc_name = Path(excel_path).stem

        for sheet in wb:
            rows = []
            for row in sheet.iter_rows(values_only=True):
                rows.append("\t".join([str(c) for c in row if c]))

            elements.append({
                "uid": uuid,
                "type": "text",
                "page": sheet.title,
                "content": "\n".join(rows),
                "doc": doc_name,
                "images": ""
            })
        
        print(elements)
        return elements