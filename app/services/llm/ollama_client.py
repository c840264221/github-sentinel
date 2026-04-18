import requests
from app.services.llm.base import LLMClient


class OllamaClient(LLMClient):
    def summarize(self, text: str) -> str:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"Summarize:\n{text}"
            }
        )

        return response.json()["response"]