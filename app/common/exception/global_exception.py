from fastapi.responses import JSONResponse
from fastapi import Request
from app.common.response.response_model import ResponseModel
from app.core.logging import get_logger

logger = get_logger(__name__)

async def global_exception_handler(request: Request, exc: Exception):

    logger.exception(
        f"Global Exception | path={request.url.path} | method={request.method} | error={exc}"
    )

    return JSONResponse(
        status_code=500,
        content=ResponseModel.fail_response(message=str(exc), code=500)
    )