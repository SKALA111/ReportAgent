import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def ask_with_context(prompt: str, context: list[str], model: str = "gpt-4") -> str:
    """
    컨텍스트와 함께 OpenAI 모델에 프롬프트를 전달하여 응답을 생성합니다.

    Args:
        prompt (str): 프롬프트 (프롬프트 템플릿 + 치환된 변수)
        context (List[str]): RAG 또는 검색에서 추출된 문서들
        model (str): GPT 모델명 (예: gpt-4)

    Returns:
        str: GPT의 응답 텍스트
    """
    context_text = "\n\n".join(context)

    full_prompt = f"""
    [Context]
    {context_text}

    [Instruction]
    {prompt}
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful and professional AI analyst assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[LLM 호출 오류] {e}")
        return "Error: LLM call failed."