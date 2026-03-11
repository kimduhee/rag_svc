from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.embedding.bge_m3 import BGEEmbedding
from app.llm.ollama import OllamaClient
from app.service.search_service import question_search
from app.schemas.question_schema import Question

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

