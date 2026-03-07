from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_BODEL, DEVICE
import torch

class BGEEmbedding:
    def __init__(self):
        device = DEVICE
        self.model = SentenceTransformer(EMBEDDING_BODEL, device=device)

    """
    입력 텍스트 리스트를 한 번에 encode하여 (N, VECTOR_DIM) 형태의 벡터 배열 생성
    normalize_embeddings=True: 코사인 유사도 계산을 위해 벡터를 L2 정규화
    """
    def embed(self, texts: list[str]):
        return self.model.encode(texts, normalize_embeddings=True)
