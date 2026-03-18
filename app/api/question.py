import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.embedding.bge_m3 import BGEEmbedding
from app.llm.ollama import OllamaClient
from app.service.search_service import question_search
from app.schemas.question_schema import Question
from app.core.logging import get_logger

router = APIRouter(prefix="/api/chat")

"""
질문에 대한 LLM 요청을 한다.

desc:
    질문 임베딩(BAAI/bge-m3) => 엘라스틱서치(bm25, KNN) 검색 => LLM질의(ollama or vLLM)
Args:
    question(str): 질문 문자열
Returns:
    답변 TOKEN(text/event-stream)
"""
@router.post("/question")
def query(req: Question):

    return StreamingResponse(
        question_search(req.question),
        media_type="text/event-stream"
    )

@router.post("/test-question")
def query(req: Question):

    return StreamingResponse(
        test_stream(),
        media_type="text/event-stream"
    )

def test_stream():
    yield f"data: [TOKEN]삼\n\n"
    time.sleep(0.5)
    yield f"data: [TOKEN]성전\n\n"
    time.sleep(0.5)
    yield f"data: [TOKEN]자의\n\n"
    time.sleep(0.5)
    yield f"data: [TOKEN] AI\n\n"
    time.sleep(0.5)
    yield f"data: [TOKEN] 이름은\n\n"
    time.sleep(0.5)
    yield f"data: [TOKEN] 가우스\n\n"
    time.sleep(0.5)
    yield f"data: [TOKEN]입\n\n"
    time.sleep(0.5)
    yield f"data: [TOKEN]니다\n\n"
    time.sleep(0.5)
    yield f"data: [REFERENCE]{{'page': '1', 'file_name': '삼성전자 엑시노스', 'uid': 'c8c3c6df-2e66-445c-bb88-05ef689977fb', 'content':'하하하하하'}}\n\n"
    time.sleep(0.5)
    yield f"data: [REFERENCE]{{'page': '2', 'file_name': '삼성전자 엑시노스', 'uid': 'c8c3c6df-2e66-445c-bb88-05ef689977fb', 'content':'호호호호호호'}}\n\n"
    time.sleep(0.5)
    yield f"data: [DONE]\n\n"