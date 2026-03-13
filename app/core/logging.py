import logging
import os

"""
프로젝트 공통 로깅 설정
"""
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
LEVEL = logging._nameToLevel.get(LOG_LEVEL, logging.DEBUG)

logging.basicConfig(
    level=LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

# 라이브러리 로그 끄기
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("elasticsearch").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("pdfminer").setLevel(logging.WARNING)

def get_logger(name):
    return logging.getLogger(name)
