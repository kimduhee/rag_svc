from fastapi import APIRouter

router = APIRouter(prefix="/health")

@router.get("")
def health_check():
    """
    서버 헬스 체크
    """
    return {"status": "ok"}
