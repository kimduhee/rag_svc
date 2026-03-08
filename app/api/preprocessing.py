import logging

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.service.embedding_service import doc_embed, doc_soft_delete
from app.common.response.response_model import ResponseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat")

"""
    문서에 대한 임베딩
    문서 업로드(추후 백엔드에서 처리) => Load => Split(RecursiveCharacterTextSplitter) => Embed(BAAI/bge-m3) => Store(ElasticSearch)
    TODO: Spring boot에서 파일 업로드 후 업로드경로 전달하면 llm시스템에서는 해당 경로의 파일을 읽고 처리
"""
@router.post("/embedding-create", response_model=ResponseModel)
async def embedding_create(uuid: str, file: UploadFile = File(...)):

    result = {}

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    logger.info(f"[UPLOAD] filename={file.filename}")

    try:
        await doc_embed(uuid, file)
        """
        return {
            "status": "ok",
            "filename": file.filename,
            "chunks": result.get("chunks", 0),
            "vectors": result.get("vectors", 0),
            "images": result.get("images", 0),
        }
        """

        return ResponseModel.success_response(data=result)
    except Exception as e:
        logger.exception("[UPLOAD ERROR]%s", str(e))
        #raise HTTPException(status_code=500, detail=str(e))
        return ResponseModel.fail_response()

"""
    문서 삭제 처리
"""
@router.post("/embedding-delete", response_model=ResponseModel)
async def embedding_delete(uuid: str):

    result = {}

    try:
        await doc_soft_delete(uuid)
        return ResponseModel.success_response(data=result)
    except Exception as e:
        logger.exception("[UPLOAD ERROR]%s", str(e))
        return ResponseModel.fail_response()