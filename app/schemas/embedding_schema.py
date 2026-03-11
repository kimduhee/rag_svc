from pydantic import BaseModel

class EmbeddingCreate(BaseModel):
    uuid: str
    save_path: str

class EmbeddingStatus(BaseModel):
    uuid: str
    status: str

class EmbeddingDelete(BaseModel):
    uuid: str