import os
import torch
from pathlib import Path
from elasticsearch import Elasticsearch

# ==============================
# Elasticsearch 설정
# ==============================
# Elasticsearch 접속 URL
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
# RAG용 벡터 인덱스 이름
ES_INDEX = os.getenv("ES_INDEX", "rag-vectors-test")
# BGE-M3 임베딩 차원 수
VECTOR_DIM = 1024

# ==============================
# 문서 설정
# ==============================
# 업로드 기본 경로
BASE_UPLOAD_DOC_DIR = Path("C:/ai/upload/file")

# ==============================
# LLM
# ==============================
# LLM URL(이미지 분석용)
IMAGE_LLM_URL = "http://localhost:11434/api/generate"
# LLM URL(질문용)
LLM_URL = "http://localhost:11434/api/generate"
# 임베딩 모델
EMBEDDING_BODEL = "BAAI/bge-m3"
# 임베딩 디바이스(cpu, cuda)
# cpu(모든 환경), cuda(NVIDIA GPU), mps(Apple Silicon)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"