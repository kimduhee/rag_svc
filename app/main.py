from fastapi import FastAPI
from app.api import health, preprocessing, question
from app.core.logging import get_logger

app = FastAPI(
    title="RAG System",
    description="PDF/Excel/Doc 기반 멀티모달 RAG",
    version="1.0"
)

app.include_router(health.router)
app.include_router(preprocessing.router)
app.include_router(question.router)
