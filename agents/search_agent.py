# agents/search_agent.py

from langchain_core.runnables import Runnable
from prompts.prompt import SEARCH_AGENT_PROMPT
from models.llm_wrapper import ask_with_context

# 1. 웹 검색 (Serper API 기반)
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def web_search(query: str, max_results=5) -> list[str]:
    """
    Serper API를 사용하여 구글 기반 웹 검색을 수행합니다.
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

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
        results.append("관련 검색 결과가 없습니다.")

    return results

# 2. 임베딩 및 벡터 유사도 검색 (Chroma + SentenceTransformers 사용)
import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.get_or_create_collection("search_docs")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

import time

def store_documents(docs: list[str]):
    """
    문서들을 임베딩하여 벡터 저장소에 저장합니다.
    """
    embeddings = embed_model.encode(docs).tolist()
    timestamp = int(time.time())  # 현재 타임스탬프
    for i, doc in enumerate(docs):
        unique_id = f"doc_{timestamp}_{i}"  # 타임스탬프와 인덱스를 결합
        collection.add(
            documents=[doc],
            ids=[unique_id],
            embeddings=[embeddings[i]]
        )

def retrieve_similar(query: str, top_k=3) -> list[str]:
    """
    쿼리와 유사한 문서를 벡터 검색으로 추출합니다.
    """
    embedding = embed_model.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    return results['documents'][0]

# 3. SearchAgent 정의
class SearchAgent(Runnable):
    def __init__(self, model):
        self.model = model

    def invoke(self, input_data: dict, config=None) -> dict:
        name = input_data["startup_name"]

        print(f"검색 중: {name}")
        docs = web_search(name)

        print("문서를 벡터 저장소에 저장합니다.")
        store_documents(docs)

        return {
            "search_docs": docs,        # 사용자가 확인 가능
            "startup_name": name        # TechAgent 전달용
        }