from app.llm.ollama import OllamaClient
from app.embedding.bge_m3 import get_embedding
from app.common.elasticsearch.es_search import search_hybrid
from app.core.logging import get_logger

llm = OllamaClient()
embedding = get_embedding()
logger = get_logger(__name__)

"""
질문에 대한 검색을 처리한다.

Args:
    question(str): 질문 텍스트
Returns:
    답변에 대한 stream
    예)
        data: [TOKEN]XXXXX  => 답변 stream
        data: [ERROR]XXXXX  => 에러시 
        data: [REFERENCE]XXXX => 출처문서 정보
"""
def question_search(question: str):

    try:
        results = search_hybrid(question, top_k=5, bm25_k=30, alpha=0.6)
    except Exception as e:
        yield f"data: [ERROR]llm 요청 처리중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
        return

    return llm.generate(question, results)