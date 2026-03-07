from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.service.embedding_service import doc_embed
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload")
async def upload(uuid: str, file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    logger.info(f"[UPLOAD] filename={file.filename}")

    try:
        # 🔹 실제 ingest 실행 (저장 → 파싱 → 청킹 → 임베딩 → faiss)
        result = await doc_embed(uuid, file)
        """
        return {
            "status": "ok",
            "filename": file.filename,
            "chunks": result.get("chunks", 0),
            "vectors": result.get("vectors", 0),
            "images": result.get("images", 0),
        }
        """
        return {}
    except Exception as e:
        logger.exception("[UPLOAD ERROR]")
        raise HTTPException(status_code=500, detail=str(e))
