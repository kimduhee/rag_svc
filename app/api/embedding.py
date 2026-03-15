import asyncio
import os

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.service.embedding_service import doc_embed, doc_soft_delete
from app.common.response.response_model import ResponseModel
from app.core.config import settings
from app.schemas.embedding_schema import EmbeddingStatus, EmbeddingCreate, EmbeddingDelete
from app.core.logging import get_logger

router = APIRouter(prefix="/api/chat")
logger = get_logger(__name__)

"""
(삭제대상)문서를 업로드 한다.
=> 백엔드에서 업로드 하고 업로드 경로 받는 부분 부터 시작
"""
@router.post("/embedding-upload", response_model=ResponseModel)
async def embedding_create(uuid: str, file: UploadFile = File(...)):
    result = {}

    if not file.filename:
        #raise HTTPException(status_code=400, detail="No file uploaded")
        return ResponseModel.fail_response("No file uploaded")

    logger.info(f"[UPLOAD] filename={file.filename}")

    try:
        upload_path = Path(settings.base_upload_doc_dir) / uuid
        os.makedirs(upload_path, exist_ok=True)

        file_name = Path(file.filename).name
        file_suffix = Path(file.filename).suffix
        save_path = upload_path / f"{file_name}"

        with open(save_path, "wb") as f:
            f.write(await file.read())

        result["file_path"] = save_path.as_posix()
        return ResponseModel.success_response(data=result)
    except Exception as e:
        logger.exception("[UPLOAD ERROR]%s", str(e))
        #raise HTTPException(status_code=500, detail=str(e))
        return ResponseModel.fail_response()

"""
문서에 대한 임베딩 처리한다.

desc:
    문서 업로드(추후 백엔드에서 처리) => Load => Split(RecursiveCharacterTextSplitter) => Embed(BAAI/bge-m3) => Store(ElasticSearch)
    호출한 백엔드에서 타임아웃 발생 소지가 있기 때문에 스레드로 전처리하고 처리완료 후 백엔드에 전처리 작업 상태값 전달한다.
    TODO: Spring boot에서 파일 업로드 후 업로드경로 전달하면 llm시스템에서는 해당 경로의 파일을 읽고 처리
Args:
    uuid(str): 문서고유번호(백엔드 서버에서 파일 업로드 후 고유 uuid 할당하여 전달)
    file: TODO 파일경로
Returns:
    
"""
@router.post("/embedding-create", response_model=ResponseModel)
async def embedding_create(req: EmbeddingCreate):

    result = {}

    logger.info(f"filename={req.save_path}")

    try:
        # 전처리는 스레드에서 처리
        task = asyncio.create_task(doc_embed(req.uuid, req.save_path))
        def task_done(t):
            if t.exception():
                logger.exception(t.exception())

        task.add_done_callback(task_done)

        # 문서 전처리 시작됨을 전달
        result["uuid"] = req.uuid
        result["status"] = "start"

        return ResponseModel.success_response(data=result)
    except Exception as e:
        logger.exception("[UPLOAD ERROR]%s", str(e))
        #raise HTTPException(status_code=500, detail=str(e))
        return ResponseModel.fail_response()

"""
(전처리상태 호출 확인용용)문서 전처리 작업 진행상태 처리한다.
TODO 백엔드에서 처리해야 하는 부분이며 추후 삭제

Args:
    uuid(str): 문서고유번호
    status(str): 처리상태
Returns:
    
"""
@router.post("/embedding-status")
def embedding_status(req: EmbeddingStatus):
    logger.debug("전처리 uuid: %s", req.uuid)
    logger.debug("전처리 상태: %s", req.status)

"""
동일 문서에 대한 엘라스틱서치 soft-delete 처리한다.

Args:
    uuid(str): 문서고유번호
Returns:
    
"""
@router.post("/embedding-delete", response_model=ResponseModel)
async def embedding_delete(req: EmbeddingDelete):

    result = {}

    try:
        result = await doc_soft_delete(req.uuid)

        if result == "fail":
            return ResponseModel.fail_response()
        
        # TODO 이전버전 업로드 파일 삭제 처리 구현 필요

        return ResponseModel.success_response(data=result)
    except Exception as e:
        logger.exception("[UPLOAD ERROR]%s", str(e))
        return ResponseModel.fail_response()