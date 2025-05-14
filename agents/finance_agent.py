from langchain_core.runnables import Runnable
from prompts.prompt import FINANCE_AGENT_PROMPT
from models.llm_wrapper import ask_with_context

# 웹 검색 (Serper API)
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def web_search(query: str, max_results=5) -> list[str]:
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY가 .env에 정의되어 있지 않습니다.")

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key}
    payload = {"q": query}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Serper API 호출 실패: {response.status_code} {response.text}")

    data = response.json()
    results = []

    if "organic" in data:
        for item in data["organic"][:max_results]:
            if "snippet" in item:
                results.append(item["snippet"])
            elif "title" in item:
                results.append(item["title"])

    if not results:
        results.append("재무 관련 검색 결과가 없습니다.")

    return results

# FinanceAgent 정의
class FinanceAgent(Runnable):
    def __init__(self, model):
        self.model = model

    def invoke(self, input_data: dict, config=None) -> dict:
        name = input_data.get("startup_name", "").strip()
        if not name:
            return {"finance_summary": "FinanceAgent: startup_name이 없습니다."}

        print("재무 관련 정보를 웹에서 검색합니다.")
        docs = web_search(f"{name} 투자 유치 수익 매출 성장률")

        prompt = FINANCE_AGENT_PROMPT.replace("{{search_result}}", "\n".join(docs))

        print("재무 상태 분석을 생성합니다.")
        result = ask_with_context(prompt, context=[], model=self.model)

        return {"finance_summary": result}
