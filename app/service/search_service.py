from app.llm.ollama import OllamaClient
from app.embedding.bge_m3 import get_embedding
from app.common.elasticsearch.es_search import search_hybrid
from app.core.logging import get_logger

llm = OllamaClient()
embedding = get_embedding()

logger = get_logger(__name__)

def question_search(question: str):

    results = search_hybrid(question, top_k=5, bm25_k=30, alpha=0.6, max_chars=3000)

    logger.debug("\n################### LLM에 전달할 Context ###################")
    logger.debug(results)

    return llm.generate(question, results)