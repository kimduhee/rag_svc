import openpyxl
from pathlib import Path

class ExcelLoader:
    """
    Excel → 시트별 텍스트 테이블화
    """

    def load(self, path: str):
        wb = openpyxl.load_workbook(path)
        doc_name = Path(path).stem

        elements = []
        for sheet in wb:
            rows = []
            for row in sheet.iter_rows(values_only=True):
                rows.append("\t".join([str(c) for c in row if c]))

            elements.append({
                "type": "text",
                "page": sheet.title,
                "content": "\n".join(rows),
                "doc": doc_name
            })
        return elements
