from fastapi import APIRouter
#from app.rag.pipeline import RAGPipeline
from app.embedding.bge_m3 import BGEEmbedding
from app.llm.ollama import OllamaClient
#from app.core.config import FAISS_DIR
#from app.core.config import OLLAMA_MODEL

router = APIRouter()

#store = FaissStore(dim=1024, path=FAISS_DIR)
embedder = BGEEmbedding()
#llm = OllamaClient(model=OLLAMA_MODEL)

#pipeline = RAGPipeline(
    #store=store,
#    embedder=embedder
    #llm=llm
#)


#@router.post("/query")
#def query(q: str):
#    return pipeline.query(q)
