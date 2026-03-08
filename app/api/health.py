import requests

from fastapi import APIRouter
from app.common.elasticsearch.es_client import get_es_client
from app.core.config import Settings
from app.common.response.response_model import ResponseModel

router = APIRouter(prefix="/api/chat")

@router.get("/health", response_model=ResponseModel)
def health_check():

    result = {}

    # elastic health check
    try:
        client = get_es_client()
        if client.ping():
            #es_check = True
            result["es_check"] = True
        else:
            #es_check = False
            result["es_check"] = False
    except Exception as e:
        result["es_check"] = False

    # llm health check
    try:
        res = requests.get(Settings.llm_check_url)
        if res.status_code == 200:
            #llm_check = True
            result["llm_check"] = True
        else:
            #llm_check = False
            result["llm_check"] = False
    except:
        #llm_check = False
        result["llm_check"] = False

    return ResponseModel.success_response(data=result)
