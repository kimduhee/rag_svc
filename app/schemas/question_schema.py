from pydantic import BaseModel

"""
질문 요청 
"""
class Question(BaseModel):
    question: str