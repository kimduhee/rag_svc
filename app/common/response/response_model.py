from pydantic import BaseModel
from typing import Any, Optional

class ResponseModel(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

    def success_response(data: Any = None, message: str = "Success", code: int = 200):
        return {
            "code": code,
            "message": message,
            "data": data
        }

    def fail_response(message: str = "Fail", code: int = 400, data: Any = None):
        return {
            "code": code,
            "message": message,
            "data": data
        }