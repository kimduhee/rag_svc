from app.core.config import ENV
from .ollama import OllamaClient
from .vllm import VLLMClient

def get_llm():
    if ENV == "local":
        return OllamaClient("llava-llama3")
    return VLLMClient("Qwen-VL")
