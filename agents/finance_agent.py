import os
import pandas as pd
import openai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# 환경 변수 로드 및 모델 초기화
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_dim = 384

# 파일 경로
CSV_FILE_PATH = "/workspaces/ReportAgent/data/startups.csv"

# 벡터 저장소
company_texts = []
company_names = []
company_embeddings = []

# 기업 정보 문서화
def format_company_doc(row):
    return f"""
    [기업명]: {row['스타트업']}
    [분야]: {row['분야']}
    [특징]: {row['특징']}
    [성장 포인트]: {row['성장 포인트']}
    """

# RAG 기반 분석
def rag_analysis_for_company(company_idx, data, index):
    target_doc = company_texts[company_idx]
    target_emb = company_embeddings[company_idx]

    # 유사 기업 탐색
    D, I = index.search(np.array([target_emb]), 4)
    context_docs = [company_texts[i] for i in I[0] if i != company_idx]
    context = "\n\n".join(context_docs)

    prompt = f"""
    주요 스타트업들 정보:\n\n{context}\n\n
    대상 기업:\n{target_doc}\n\n
    이 기업의 재무 상태, 실적, 향후 성장 가능성을 다른 기업들과 비교하며 전문가처럼 분석해줘.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a startup investment analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=700
    )
    return response.choices[0].message["content"].strip()

# 전체 분석 파이프라인
def main():
    data = pd.read_csv(CSV_FILE_PATH)

    # Step 1: 기업 정보 임베딩
    for _, row in data.iterrows():
        doc = format_company_doc(row)
        emb = model.encode(doc)
        company_texts.append(doc)
        company_names.append(row["스타트업"])
        company_embeddings.append(emb)

    # Step 2: FAISS 인덱스 구축
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np.array(company_embeddings))

    # Step 3: 각 기업에 대해 RAG 분석
    analysis_results = []
    for i, name in enumerate(company_names):
        print(f"🔍 [{i+1}/{len(company_names)}] {name} 분석 중...")
        analysis = rag_analysis_for_company(i, data, index)
        analysis_results.append((name, analysis))

    # Step 4: 결과 저장
    analysis_texts = [f"{name}: {analysis}" for name, analysis in analysis_results]
    analysis_embeddings = model.encode(analysis_texts)
    analysis_index = faiss.IndexFlatL2(embedding_dim)
    analysis_index.add(np.array(analysis_embeddings))

    faiss.write_index(analysis_index, "company_analysis.faiss")
    with open("company_analysis.pkl", "wb") as f:
        pickle.dump((analysis_texts, [name for name, _ in analysis_results]), f)

    print("✅ 전체 기업 분석 및 벡터 DB 저장 완료!")

if __name__ == "__main__":
    main()
