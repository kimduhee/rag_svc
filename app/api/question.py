from fastapi import APIRouter
from fastapi.responses import StreamingResponse
#from app.rag.pipeline import RAGPipeline
from app.embedding.bge_m3 import BGEEmbedding
from app.llm.ollama import OllamaClient
from app.service.search_service import question_search
#from app.core.config import FAISS_DIR
#from app.core.config import OLLAMA_MODEL

router = APIRouter(prefix="/api/chat")

#store = FaissStore(dim=1024, path=FAISS_DIR)
#embedder = BGEEmbedding()
#llm = OllamaClient()

#pipeline = RAGPipeline(
    #store=store,
#    embedder=embedder
    #llm=llm
#)


@router.post("/question")
def query(question: str):

    #return question_search(question)
    
    return StreamingResponse(
        question_search(question),
        media_type="text/event-stream"
    )
    
    #return pipeline.query(q)
