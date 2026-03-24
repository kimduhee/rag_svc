from pydantic import BaseModel

"""
질문 요청 
"""
class Question(BaseModel):
    question: str

"""
채팅 이력
"""
class ChatHistory(BaseModel):
    searchText: str

"""
채팅 삭제
"""
class ChatDelete(BaseModel):
    chatId: str

"""
메시지 이력
"""
class MessageHistory(BaseModel):
    chatId: str