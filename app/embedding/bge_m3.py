from sentence_transformers import SentenceTransformer
from app.core.config import settings
import torch

class BGEEmbedding:
    def __init__(self):
        device = settings.device
        self.model = SentenceTransformer(settings.embedding_model, device=device)

    """
    입력 텍스트 리스트를 한 번에 encode하여 (N, VECTOR_DIM) 형태의 벡터 배열 생성
    normalize_embeddings=True: 코사인 유사도 계산을 위해 벡터를 L2 정규화
    """
    def embed(self, texts: list[str]):
        return self.model.encode(texts, normalize_embeddings=True)

embedding_model = None

def get_embedding():
    global embedding_model
    
    if embedding_model is None:
        embedding_model = BGEEmbedding()
    
    return embedding_model
