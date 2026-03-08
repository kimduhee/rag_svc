from fastapi.responses import JSONResponse
from fastapi import Request
from app.common.response.response_model import ResponseModel

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseModel.error_response(message=str(exc), code=500)
    )