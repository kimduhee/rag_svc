import os
import torch
from pathlib import Path
from elasticsearch import Elasticsearch
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "local"
    es_host: str
    es_index: str
    vector_dim: int
    base_upload_doc_dir: str
    llm_check_url: str
    image_llm_url: str
    llm_url: str
    llm_model: str
    embedding_model: str
    device: str

    class Config:
        env_file = f"env/.env.{os.getenv('ENV', 'local')}"

settings = Settings()
"""
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "rag-vectors-test")
VECTOR_DIM = 1024
BASE_UPLOAD_DOC_DIR = Path("C:/ai/upload/file")
IMAGE_LLM_URL = "http://localhost:11434/api/generate"
LLM_URL = "http://localhost:11434/api/chat"
LLM_MODEL = "llama3"
EMBEDDING_MODEL = "BAAI/bge-m3"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
"""