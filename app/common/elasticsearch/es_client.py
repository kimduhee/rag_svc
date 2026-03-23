from elasticsearch import Elasticsearch
from app.core.config import settings

_client = None

"""
Elasticsearch 클라이언트를 생성.
"""
def get_es_client():
    global _client

    if _client is None:
        _client = Elasticsearch(
            settings.es_host,
            timeout=30,
            max_retries=3,
            retry_on_timeout=True
        )
    
    return _client