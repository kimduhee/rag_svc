from fastapi import FastAPI
from app.api import health, embedding, question
from app.common.exception.global_exception import global_exception_handler
from app.core.logging import get_logger

app = FastAPI(
    title="RAG System",
    description="PDF/Excel/Doc 기반 RAG",
    version="1.0"
)

app.include_router(health.router)
app.include_router(embedding.router)
app.include_router(question.router)

# 글로벌 예외 처리 설정
app.add_exception_handler(Exception, global_exception_handler)