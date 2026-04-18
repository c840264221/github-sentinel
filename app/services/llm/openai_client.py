# services/llm/openai_client.py
import os

from openai import OpenAI
from app.services.llm.base import LLMClient

openai_api_key = os.getenv("OPENAI_API_KEY")
class OpenAIClient(LLMClient):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def summarize(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # ⭐ 推荐用这个（便宜很多）
            messages=[
                {"role": "system", "content": "Summarize the following GitHub updates:"},
                {"role": "user", "content": text}
            ]
        )

        return response.choices[0].message.content
