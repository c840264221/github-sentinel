# services/llm/base.py

class LLMClient:
    def summarize(self, text: str) -> str:
        raise NotImplementedError
