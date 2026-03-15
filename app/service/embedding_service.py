import os
import shutil
import uuid
import numpy as np
import requests
import httpx

from pathlib import Path
from typing import List, Dict
from fastapi import UploadFile
from app.loaders.pdf_loader import PDFLoader
from app.loaders.excel_loader import ExcelLoader
from app.loaders.docx_loader import DocxLoader
from app.embedding.bge_m3 import get_embedding
from app.core.config import settings
from app.core.logging import get_logger
from app.common.elasticsearch.es_vector_store import doc_deleted, index_vectors
from app.common.elasticsearch.es_client import get_es_client
from app.common.elasticsearch.es_index import create_index

embedding = get_embedding()
logger = get_logger(__name__)

"""
문서 업로드
1. 파일 저장
"""
async def doc_embed(uuid: str, save_path: str) -> Dict:

    # 벡엔드에 전달할 상태값
    status_data = {}
    status_data["uuid"] = uuid

    # ==========================================================================================
    # 1)loader 설정
    # ==========================================================================================
    file_suffix = Path(save_path).suffix
    if file_suffix.lower() == ".pdf":
        loader = PDFLoader()
    elif file_suffix.lower() == ".xlsx" or file_suffix.lower() == ".xlsm":
        # TODO 엑셀의 경우 글로벌 처리가 아닌 엑셀양식에 따라 데이터 추출이 달라짐
        loader = ExcelLoader()
    elif file_suffix.lower() == ".docx":
        loader = DocxLoader()
    else:
        status_data["status"] = "fail"
        await status_response(uuid, status_data)
        raise Exception(f"Unsupported file type: {file_suffix}")

    logger.debug("파일 저장 경로: %s", save_path);

    # ==========================================================================================
    # 2)파일 이미지(이미지추출, 이미지 저장, 이미지 LLM 설명)추출, 텍스트 추출, 메타 데이터 생성)
    # ==========================================================================================
    elements = loader.load(str(save_path), uuid)

    # ==========================================================================================
    # 3)텍스트와 메타데이터 분리
    # ==========================================================================================
    texts = []      # 임베딩을 계산할 실제 텍스트 리스트
    metadatas = []  # Elasticsearch에 함께 저장할 메타데이터 리스트

    for e in elements:
        # 완전히 빈 passage는 제외
        if e["content"].strip():
            # 임베딩 모델에 "passage: " prefix를 붙여주는 형태로 입력
            # - BGE 계열 모델에서 prefix를 붙이는 것이 권장되는 패턴 중 하나임
            texts.append("passage: " + e["content"])
            metadatas.append({
                "uid": e["uid"],
                "type": e["type"],
                "page": e["page"],
                "doc": e["doc"],
                "images": e["images"],
                "content": e["content"]
            })

    # ==========================================================================================
    # 4)임베딩
    # ==========================================================================================
    vectors = embedding.embed(texts)
    vectors = np.array(vectors).astype("float32")

    # ==========================================================================================
    # 5)vectorDB 저장(ES)
    # ==========================================================================================
    client = get_es_client()
    create_index(client)

    if len(vectors) > 0:
        # 같은 문서 id(uid)를 가진 이전 passage들을 soft-delete로 표시
        # 질문시 delete 처리된 chunk는 조회 하지 않음
        doc_deleted(client, uuid)

        # 새로 계산한 벡터 + 메타데이터를 인덱싱
        index_vectors(client, vectors, metadatas)

    # deleted=False 인 document 개수를 조회하여 현재 활성 passage 수를 확인
    #count = client.count(index=settings.es_index, body={"query": {"term": {"deleted": False}}})

    #logger.debug("# 유효한 값: %s", count["count"]);
    status_data["status"] = "complete"
    await status_response(uuid, status_data)


async def status_response(uuid: str, status_data: dict):
    try:
        logger.debug("#전송시작!!")
        logger.debug("#param: %s", status_data)
        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(
                settings.local_domain,
                json=status_data
            )

        logger.debug("#전송끝!!")

    except Exception as e:
        logger.exception("문서 전처리 상태 전송 오류: %s", str(e))


"""
    기능: uuid(문서고유번호)에 대한 소프트 삭제 처리
"""
async def doc_soft_delete(uuid: str):

    logger.debug("문서 임베딩 소프트 삭제처리[%s]", uuid)

    try:
        client = get_es_client()
        create_index(client)

        doc_deleted(client, uuid)
        return "success"
    except:
        return "fail"