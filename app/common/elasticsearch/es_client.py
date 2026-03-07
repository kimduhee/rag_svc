from elasticsearch import Elasticsearch
from app.core.config import ES_HOST

_client = None

"""
Elasticsearch 클라이언트를 생성.
"""
def get_es_client():
    global _client

    if _client is None
        _client = Elasticsearch(ES_HOST)
    
    return _client