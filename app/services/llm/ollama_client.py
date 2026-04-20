import requests
from app.services.llm.base import LLMClient
from app.core.logger import LOG


class OllamaClient(LLMClient):

    def generate_daily_report(self, markdown_content: str) -> str:
        LOG.info(f"Ollama Generating daily report")
        prompt = (f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}\n\n 最后请以中文回答，并且将每个标题"
                  f"用不同的颜色展示，并在标题前加一个对应的小图标")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream":False
            }
        )
        response.raise_for_status()
        LOG.info(f"Ollama summary completed")

        return response.json().get("response","")

