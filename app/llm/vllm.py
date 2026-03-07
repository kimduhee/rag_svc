import requests
from app.core.config import VLLM_URL

class VLLMClient:
    def __init__(self, model):
        self.model = model

    def generate(self, prompt, images):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": images
        }
        r = requests.post(f"{VLLM_URL}/generate", json=payload)
        return r.json()["text"]
