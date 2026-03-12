import numpy as np
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

"""
동일 문서 uid를 가진 기존 passage들을 soft-delete 처리한다.

desc:
    - 같은 PDF를 다시 색인할 때, 기존 벡터들을 실제로 삭제하지 않고 deleted=True로만 표시
    - 검색 시 deleted=False 조건으로 필터링하여, 가장 최신 버전의 문서만 보이도록 함
    - update_by_query를 사용하기 때문에 전체 인덱스를 다시 만드는 비용을 줄일 수 있음
Args:
    client(Elasticsearch): Elasticsearch client
    doc_id(str): 문서 uuid
Returns:

"""
def doc_deleted(client: Elasticsearch, doc_id: str):
    client.update_by_query(
        index=settings.es_index,
        body={
            "script": {"source": "ctx._source.deleted = true", "lang": "painless"},
            "query": {"term": {"uid": doc_id}}
        },
        refresh=True
    )

"""
임베딩 벡터와 메타데이터를 Elasticsearch에 bulk 인덱싱한다.

desc:
    - vectors: (N, VECTOR_DIM) 형태의 numpy 배열
    - metadatas: 각 passage에 대한 부가 정보(uid, type, page, doc, images, content)
    - 하나의 passage(텍스트 조각 또는 이미지 설명)가 Elasticsearch의 한 document가 된다.
Args:
    client(Elasticsearch): Elasticsearch client
    vectors(np.ndarray): chunk 임베딩 값값
    metadatas(list): 메타데이터
Returns:

"""
def index_vectors(client: Elasticsearch, vectors: np.ndarray, metadatas: list):
    def gen():
        for i, (vec, m) in enumerate(zip(vectors, metadatas)):
            yield {
                "_index": settings.es_index,
                # 하나의 문서(uid) 안에서도 페이지/조각마다 여러 passage가 생기므로
                # ES의 _id는 (문서 uid, 페이지 번호, 로컬 인덱스)를 조합해서 유일하게 만든다.
                "_id": f"{m['uid']}_{m['page']}_{i}",
                "_source": {
                    # numpy 배열은 바로 직렬화할 수 없기 때문에 list로 변환해서 저장
                    "passage_embedding": vec.tolist(),
                    "uid": m["uid"],
                    "type": m["type"],
                    "page": m["page"],
                    "doc": m["doc"],
                    "images": m["images"],
                    "content": m["content"],
                    # 새로 저장되는 passage는 항상 deleted=False 상태로 시작
                    "deleted": False
                }
            }
    try:
        bulk(client, gen(), refresh=True)
    except BulkIndexError as e:
        logger.exception(json.dumps(e.errors, indent=2))