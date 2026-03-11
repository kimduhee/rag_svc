from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from app.core.config import settings

def create_index(client: Elasticsearch):
    """
    벡터 검색용 인덱스 매핑을 생성한다. (이미 존재하면 아무 작업도 하지 않음)

    - passage_embedding:
        - dense_vector: 벡터 저장용 필드
        - dims: 벡터 차원 수
        - index: 벡터 검색 가능하게 설정
        - similarity: 코사인 유사도로 검색
    - uid: 하나의 원본 문서를 나타내는 논리적 UID (여러 passage가 같은 uid를 가질 수 있음)
    - type: "text" / "image" 등 passage의 유형
    - page: 원본 PDF의 페이지 번호
    - doc: 원본 PDF 파일명(확장자 제거)
    - images: passage에 연결된 실제 이미지 파일 경로 리스트
    - content: LLM에 넘길 실제 텍스트 (색인은 하지 않고 저장만 함)
    - deleted: soft-delete 플래그. True면 검색에서 제외
    """
    if client.indices.exists(index=settings.es_index):
        return

    client.indices.create(
        index=settings.es_index,
        body={
            "mappings": {
                "properties": {
                    "passage_embedding": {
                        "type": "dense_vector",
                        "dims": settings.vector_dim,
                        "index": True,
                        "similarity": "cosine"
                    },
                    "uid": { "type": "keyword" },
                    "type": { "type": "text" },
                    "page": { "type": "text" },
                    "doc": { "type": "keyword" },
                    "images": { "type": "keyword" },
                    "content": { "type": "text"},
                    "deleted": { "type": "boolean" }
                }
            }
        }
    )