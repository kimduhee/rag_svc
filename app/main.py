from fastapi import FastAPI
from app.api import upload, query, docs
from app.core.logging import get_logger

app = FastAPI(
    title="Multimodal RAG System",
    description="PDF/Excel/Doc 기반 멀티모달 RAG",
    version="1.0"
)

app.include_router(upload.router)
app.include_router(query.router)
app.include_router(docs.router)
