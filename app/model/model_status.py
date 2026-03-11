from pydantic import BaseModel

class EmbeddingStatus(BaseModel):
    uuid: str
    status: str