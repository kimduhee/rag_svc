import requests


class OllamaClient:
    def __init__(self, model: str):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def generate(self, prompt: str, images: list[str] | None = None):
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        # 멀티모달일 경우
        if images:
            payload["messages"][0]["images"] = images

        r = requests.post(self.url, json=payload)
        r.raise_for_status()

        data = r.json()

        # ✅ Ollama chat API 정석 파싱
        return data["message"]["content"]
