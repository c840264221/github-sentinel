from app.services.llm.openai_client import OpenAIClient
from app.services.llm.ollama_client import OllamaClient


def get_llm_client(use_openai=True):
    if use_openai:
        return OpenAIClient(api_key="YOUR_API_KEY")
    else:
        return OllamaClient()