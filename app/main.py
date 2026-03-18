from fastapi import FastAPI
from app.api import health, embedding, question
from app.common.exception.global_exception import global_exception_handler
from app.core.logging import get_logger
from fastapi.middleware.cors import CORSMiddleware

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


origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 허용할 origin
    allow_credentials=True,     # 쿠키 허용
    allow_methods=["*"],        # GET, POST 등 모든 메서드
    allow_headers=["*"],        # 모든 헤더 허용
)