import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str
    log_level: str
    backend_domain: str
    es_host: str
    es_index: str
    vector_dim: int
    base_upload_doc_dir: str
    llm_base_url: str
    llm_check_url: str
    llm_generate_url: str
    llm_chat_url: str
    llm_model: str
    llm_image_model: str
    embedding_model: str
    device: str

    class Config:
        env_file = f"env/.env.{os.getenv('ENV', 'local')}"

settings = Settings() 