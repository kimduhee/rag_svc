import time
import uuid

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.embedding.bge_m3 import BGEEmbedding
from app.llm.ollama import OllamaClient
from app.service.search_service import question_search
from app.schemas.test_schema import Question, ChatHistory, MessageHistory
from app.core.logging import get_logger

router = APIRouter(prefix="/api/test")

@router.post("/chat-history")
def query(req: ChatHistory):

    if not req.searchText:

        result = { "chatHistoryList" : 
            [
                {
                    "date": "20260302",
                    "chatId": "1234567890",
                    "title": "오늘 날씨 어때?"
                },
                {
                    "date": "20260302",
                    "chatId": "9876543210",
                    "title": "삼성전자 주식 얼마야?"
                }
            ]
        }
    else:
        result = { "chatHistoryList" : 
            [
                {
                    "date": "20260302",
                    "chatId": "1234567890",
                    "title": "오늘 날씨 어때?"
                },
                {
                    "date": "20260302",
                    "chatId": "9876543210",
                    "title": "삼성전자 주식 얼마야?"
                }
            ]
        }
    return result

@router.post("/message-history")
def query(req: MessageHistory):

    if not req.chatId:

        result = { "messageHistoryList" : 
            [
                {
                    "chatId": "1234",
                    "msgId": "1111",
                    "question": "오늘 날씨 어때?",
                    "answer": "# 오늘 날씨는 매우 좋습니다.",
                    "references" : [
                        {
                            "fileName": "삼성전자 문서",
                            "page": "1",
                            "uid": "99999" 
                        },
                        {
                            "fileName": "삼성전자 문서",
                            "page": "2",
                            "uid": "88888"
                        }
                    ]
                },
                
            ]
        }
    else:
        result = { "messageHistoryList" : 
            [
                {
                    "chatId": "1234",
                    "msgId": "1111",
                    "question": "오늘 날씨 어때?",
                    "answer": "# 오늘 날씨는 매우 좋습니다.",
                    "references" : [
                        {
                            "fileName": "삼성전자 문서",
                            "page": "1",
                            "uid": "99999" 
                        },
                        {
                            "fileName": "삼성전자 문서",
                            "page": "2",
                            "uid": "88888"
                        }
                    ]
                },
                
            ]
        }
    return result

@router.post("/question")
def query(req: Question):

    return StreamingResponse(
        test_stream(),
        media_type="text/event-stream"
    )
    
def test_stream():

    id = uuid.uuid4()

    yield f"data: [TOKEN]# \n\n"
    time.sleep(0.2)
    yield f"data: [TOKEN]삼\n\n"
    time.sleep(0.1)
    yield f"data: [TOKEN]성전\n\n"
    time.sleep(0.1)
    yield f"data: [TOKEN]자의\n\n"
    time.sleep(0.1)
    yield f"data: [TOKEN] AI\n\n"
    time.sleep(0.1)
    yield f"data: [TOKEN] 이름은\n\n"
    time.sleep(0.1)
    yield f"data: [TOKEN] 가우스\n\n"
    time.sleep(0.1)
    yield f"data: [TOKEN]입\n\n"
    time.sleep(0.1)
    yield f"data: [TOKEN]니다\n\n"
    time.sleep(0.2)
    yield f"data: [REFERENCE]{{\"page\": \"1\", \"file_name\": \"삼성전자 엑시노스\", \"uid\": \"c8c3c6df-2e66-445c-bb88-05ef689977fb\", \"content\":\"하하하하하\"}}\n\n"
    time.sleep(0.2)
    yield f"data: [REFERENCE]{{\"page\": \"2\", \"file_name\": \"삼성전자 엑시노스\", \"uid\": \"c8c3c6df-2e66-445c-bb88-05ef689977fb\", \"content\":\"호호호호호호\"}}\n\n"
    time.sleep(0.1)
    yield f"data: [INFO]{{\"msgId\": \"1111111111\", \"chatId\": \"9999999999\"}}\n\n"
    yield f"data: [DONE]\n\n"