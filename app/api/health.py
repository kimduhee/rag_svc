import requests
import traceback

from fastapi import APIRouter
from app.common.elasticsearch.es_client import get_es_client
from app.core.config import settings
from app.common.response.response_model import ResponseModel
from app.core.logging import get_logger

router = APIRouter(prefix="/api/chat")
logger = get_logger(__name__)

"""
어플리케이션에서 통신하는 서버의 health를 체크한다.

Args:
    Doesn't exist
Returns:
    es_check: 엘라스틱서치 체크
    llm_check: llm 체크
"""
@router.get("/health", response_model=ResponseModel)
def health_check():

    result = {}

    #======================================================
    # elastic health check
    #======================================================
    try:
        client = get_es_client()

        if client.ping():
            #es_check = True
            result["es_check"] = True
        else:
            #es_check = False
            result["es_check"] = False

        logger.info("es check: %s", result["es_check"])

    except Exception as e:
        result["es_check"] = False

    #======================================================
    # llm health check
    #======================================================
    try:
        res = requests.get(settings.llm_check_url)
        logger.info("llm check: %s", res)
        if res.status_code == 200:
            #llm_check = True
            result["llm_check"] = True
        else:
            #llm_check = False
            result["llm_check"] = False
    except Exception as e:
        traceback.print_exc()
        logger.info("Exception: %s", e)

        #llm_check = False
        result["llm_check"] = False

    return ResponseModel.success_response(data=result)
