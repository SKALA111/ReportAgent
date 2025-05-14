from langchain_core.runnables import Runnable
from prompts.prompt import MARKET_AGENT_PROMPT
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
        results.append("검색 결과가 없습니다.")

    return results

# 벡터 검색 (Chroma + SentenceTransformers)
import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.get_or_create_collection("market_docs")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

import time

def store_documents(docs: list[str]):
    """
    문서들을 임베딩하여 벡터 저장소에 저장합니다.
    """    
    embeddings = embed_model.encode(docs).tolist()
    timestamp = int(time.time())  # 현재 타임스탬프
    for i, doc in enumerate(docs):
        unique_id = f"market_{timestamp}_{i}"  # 타임스탬프와 인덱스를 결합
        collection.add(
            documents=[doc],
            ids=[unique_id],
            embeddings=[embeddings[i]]
        )

def retrieve_similar(query: str, top_k=3) -> list[str]:
    embedding = embed_model.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    if not results["documents"]:
        return []
    return results["documents"][0]

# MarketAgent 클래스 정의
class MarketAgent(Runnable):
    def __init__(self, model):
        self.model = model

    def invoke(self, input_data: dict, config=None) -> dict:
        tech = input_data.get("tech_summary", "").strip()
        startup_name = input_data.get("startup_name", "").strip()
        if not tech:
            return {"market_analysis": "MarketAgent: tech_summary가 없습니다."}

        print("시장 관련 정보 검색을 시작합니다.")
        docs = web_search(f"{tech} 시장 규모 경쟁사 기술 전망")
        store_documents(docs)

        print("유사한 시장 정보를 벡터 DB에서 검색합니다.")
        context = retrieve_similar(f"{tech} 시장성 분석")

        if not context:
            return {"market_analysis": "시장 정보를 찾을 수 없습니다."}

        prompt = MARKET_AGENT_PROMPT.replace("{{core_tech}}", tech)

        print("시장성 분석을 생성 중입니다.")
        result = ask_with_context(prompt, context, model=self.model)

        return {"market_analysis": result, "startup_name": startup_name}