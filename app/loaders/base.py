class BaseLoader:
    """
    모든 문서 로더의 공통 인터페이스
    """

    def load(self, path: str):
        raise NotImplementedError
