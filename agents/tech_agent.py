from langchain_core.runnables import Runnable
from prompts.prompt import TECH_AGENT_PROMPT
from models.llm_wrapper import ask_with_context

# 1. Chroma + SentenceTransformer 기반 벡터 검색
import chromadb
from sentence_transformers import SentenceTransformer

# 벡터 저장소 초기화
client = chromadb.Client()
collection = client.get_or_create_collection("search_docs")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_similar(query: str, top_k=3) -> list[str]:
    """
    쿼리를 임베딩하고, 벡터 저장소에서 유사 문서 top_k개를 반환합니다.
    """
    embedding = embed_model.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    return results["documents"][0] if results["documents"] else []

# 2. TechAgent 정의
class TechAgent(Runnable):
    def __init__(self, model):
        self.model = model

    def invoke(self, input_data: dict, config=None) -> dict:
        name = input_data.get("startup_name", "").strip()
        if not name:
            return {"tech_summary": "TechAgent: startup_name이 없습니다."}

        print("기술 요약을 위해 유사 문서 검색 중입니다.")
        context = retrieve_similar(f"{name} 기술 요약")

        if not context:
            return {"tech_summary": "유사한 기술 문서를 찾을 수 없습니다."}

        prompt = TECH_AGENT_PROMPT.replace("{{search_result}}", "\n".join(context))

        print("기술 요약을 생성 중입니다.")
        result = ask_with_context(prompt, context=[], model=self.model)

        return {"tech_summary": result}
