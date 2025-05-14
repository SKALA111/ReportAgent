import os
import pandas as pd
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_core.runnables import Runnable
from models.llm_wrapper import ask_with_context
from prompts.prompt import FINANCE_AGENT_PROMPT

# 환경 변수 로드 및 모델 초기화
load_dotenv()
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma 클라이언트 초기화
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("finance_docs")

# 기업 정보 문서화
def format_company_doc(row):
    return f"""
    [기업명]: {row['스타트업']}
    [분야]: {row['분야']}
    [특징]: {row['특징']}
    [성장 포인트]: {row['성장 포인트']}
    """

# FinanceAgent 정의
class FinanceAgent(Runnable):
    def __init__(self, model):
        self.model = model

    def invoke(self, input_data: dict, config=None) -> dict:
        startup_name = input_data.get("startup_name", "").strip()
        if not startup_name:
            return {"finance_analysis": "FinanceAgent: startup_name이 없습니다."}

        print(f"🔍 {startup_name}의 재무 분석을 시작합니다.")

        # 유사 기업 검색
        query_doc = format_company_doc({"스타트업": startup_name, "분야": "", "특징": "", "성장 포인트": ""})
        query_embedding = embed_model.encode(query_doc).tolist()

        results = collection.query(query_embeddings=[query_embedding], n_results=4)
        context_docs = results["documents"]

        if not context_docs:
            return {"finance_analysis": "유사한 기업 정보를 찾을 수 없습니다."}

        # 프롬프트 생성
        context = "\n\n".join(context_docs)
        prompt = FINANCE_AGENT_PROMPT.replace("{{context}}", context).replace("{{startup_name}}", startup_name)

        # OpenAI API 호출
        print(f"💡 {startup_name}의 재무 분석 생성 중...")
        result = ask_with_context(prompt, context=context_docs, model=self.model)

        return {"finance_analysis": result}

# 데이터 초기화 함수
def initialize_finance_data(file_path):
    data = pd.read_csv(file_path)

    # Chroma에 기업 정보 저장
    for _, row in data.iterrows():
        doc = format_company_doc(row)
        embedding = embed_model.encode(doc).tolist()
        collection.add(
            documents=[doc],
            metadatas=[{"name": row["스타트업"]}],
            ids=[row["스타트업"]],
            embeddings=[embedding]
        )
    print("✅ FinanceAgent 데이터 초기화 완료!")
