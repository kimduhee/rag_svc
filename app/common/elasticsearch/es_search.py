import numpy as np

from app.core.config import settings
from elasticsearch import Elasticsearch
from app.embedding.bge_m3 import get_embedding
from app.common.elasticsearch.es_client import get_es_client
from app.common.elasticsearch.es_index import create_index
from app.core.logging import get_logger

embedding = get_embedding()
logger = get_logger(__name__)

"""
코사인 유사도 기반 kNN 검색을 수행해 상위 top_k passage를 반환한다.

desc:
    - knn 필드:
        - field: 어떤 dense_vector 필드를 기준으로 검색할지 지정 (passage_embedding)
        - query_vector: 질의 문장을 임베딩한 벡터
        - k: 실제로 반환할 후보 개수
        - num_candidates: 내부적으로 더 많은 후보를 계산한 뒤 상위 k개를 반환하기 위한 값
    - filter:
        - deleted=False 조건을 사용하여 soft-delete된 passage는 검색 결과에서 제외
Args:
    client(Elasticsearch): 엘라스틱서치 client
    query_vector(list): 질문 벡터
    top_k(int): 뽑아낼 chunk 수
Returns:
    results: 조회 결과 메타데이터
"""
def search_es_knn(client: Elasticsearch, query_vector: list, top_k: int = 5):
    resp = client.search(
        index=settings.es_index,
        body={
            "size": top_k,
            "knn": {
                "field": "passage_embedding",
                "query_vector": query_vector,
                "k": top_k,
                "num_candidates": max(100, top_k * 20),
                "filter": {"term": {"deleted": False}}
            },
            "_source": ["uid", "type", "page", "doc", "images", "content", "deleted"]
        }
    )
    results = []
    for hit in resp["hits"]["hits"]:
        s = hit["_source"]
        results.append({
            "score": float(hit["_score"]),
            "uid": s["uid"],
            "type": s["type"],
            "page": s["page"],
            "doc": s["doc"],
            "images": s["images"],
            "content": s["content"],
            "deleted": s.get("deleted", False)
        })
    return results

"""
BM25 기반 키워드 검색을 수행해 상위 top_k passage를 반환한다.

desc:
    - content 필드를 대상으로 full-text 검색을 수행 (operator="and")
    - deleted=False 필터를 사용해 soft-delete 문서는 제외
Args:
    client(Elasticsearch): 엘라스틱서치 client
    query_text(str): 질문 텍스트
    top_k(int): 뽑아낼 chunk 수
Returns:
    results: 조회 결과 메타데이터
"""
def search_es_bm25(client: Elasticsearch, query_text: str, top_k: int = 30):
    resp = client.search(
        index=settings.es_index,
        body={
            "size": top_k,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "content": {
                                    "query": query_text,
                                    "operator": "and"
                                }
                            }
                        }
                    ],
                    "filter": [
                        {"term": {"deleted": False}}
                    ]
                }
            },
            "_source": ["uid", "type", "page", "doc", "images", "content", "deleted"]
        }
    )

    results = []
    for hit in resp["hits"]["hits"]:
        s = hit["_source"]
        results.append({
            "score": float(hit["_score"]),  # BM25 점수
            "uid": s["uid"],
            "type": s["type"],
            "page": s["page"],
            "doc": s["doc"],
            "images": s["images"],
            "content": s["content"],
            "deleted": s.get("deleted", False),
        })
    return results

"""
벡터 검색 결과와 BM25 검색 결과를 합쳐 hybrid rerank를 수행한다.

desc:
    - alpha: 벡터 점수 가중치 (0~1), 나머지(1-alpha)는 BM25 가중치
    - 두 점수 모두 [0,1] 범위로 정규화 후 가중합
Args:
    vector_results(list): kNN 검색 결과 리스트
    keyword_results(list): BM25 기반 키워드 검색 결과 리스트
    top_k(int): 뽑아낼 chunk 수
Returns:
    reranked:  re-rank 결과목록
"""
def rerank_hybrid_results(
    vector_results: list,
    keyword_results: list,
    top_k: int = 5,
    alpha: float = 0.6,
):
    merged = {}

    # 정규화를 위한 최대 점수 계산
    max_vec = max((r["score"] for r in vector_results), default=0.0)
    max_kw = max((r["score"] for r in keyword_results), default=0.0)

    # 벡터 결과 반영
    for r in vector_results:
        key = _make_passage_key(r)
        if key not in merged:
            merged[key] = {
                **r,
                "vector_score": 0.0,
                "bm25_score": 0.0,
            }
        merged[key]["vector_score"] = r["score"]

    # BM25 결과 반영
    for r in keyword_results:
        key = _make_passage_key(r)
        if key not in merged:
            merged[key] = {
                **r,
                "vector_score": 0.0,
                "bm25_score": 0.0,
            }
        merged[key]["bm25_score"] = r["score"]

    # 정규화 + 최종 score 계산
    for item in merged.values():
        vec_norm = item["vector_score"] / max_vec if max_vec > 0 else 0.0
        kw_norm = item["bm25_score"] / max_kw if max_kw > 0 else 0.0
        hybrid = alpha * vec_norm + (1.0 - alpha) * kw_norm
        item["score"] = float(hybrid)  # 최종 rerank 점수

    # 점수 기준 내림차순 정렬 후 top_k 반환
    reranked = sorted(merged.values(), key=lambda x: x["score"], reverse=True)

    return reranked[:top_k]

"""
벡터 kNN + BM25 키워드 검색을 결합한 하이브리드 검색.

Args:
    query(str): 사용자 자연어 질의
    top_k(int): 최종 반환할 passage 개수
    bm25_k(int): BM25에서 가져올 후보 개수 (벡터보다 넉넉히)
    alpha(float): 벡터 점수 비중 (0~1)
Returns:
    reranked:  re-rank 결과목록
"""
def search_hybrid(query: str, top_k: int = 5,
                  bm25_k: int = 30,
                  alpha: float = 0.6):

    # elasticsearch client
    client = get_es_client()
    create_index(client)

    # 1) 벡터 검색
    query_text = "query: " + query
    q_vec = embedding.embed([query_text])
    q_vec = np.array(q_vec).astype("float32")
    vector_results = search_es_knn(client, q_vec[0].tolist(), top_k=top_k)

    # 2) BM25 키워드 검색
    keyword_results = search_es_bm25(client, query_text=query, top_k=bm25_k)

    # 3) 결과 병합 및 rerank
    hybrid_results = rerank_hybrid_results(
        vector_results=vector_results,
        keyword_results=keyword_results,
        top_k=top_k,
        alpha=alpha,
    )

    for idx, r in enumerate(hybrid_results):
        logger.debug("# %s%s", idx + 1, "번째###############################################")
        logger.debug("# 점수: %s", str(r["score"]))
        logger.debug("# 페이지: %s", r["page"])
        logger.debug("# uid: %s", r["uid"])
        if r["type"] == "image":
            logger.debug("# 이미지경로: %s %s", r["images"], "\n")
        elif r["type"] == "text":
            logger.debug("# 텍스트: %s %s", r["content"], "\n")
        logger.debug("######################################################################")

    return hybrid_results

"""
하나의 passage를 유일하게 식별하기 위한 키를 생성.

desc:
    - uid + page + type 조합을 기본으로 사용 (필요시 조정 가능)
Args:
    result(dict): 메타데이터
Returns:
    생성한 키 값값
"""
def _make_passage_key(result: dict) -> tuple:
    return (result["uid"], result["page"], result["type"])