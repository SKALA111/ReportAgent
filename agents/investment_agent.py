from langchain_core.runnables import Runnable
from prompts.prompt import INVESTMENT_AGENT_PROMPT
from models.llm_wrapper import ask_with_context

class InvestmentAgent(Runnable):
    def __init__(self, model):
        self.model = model

    def invoke(self, input_data: dict, config=None) -> dict:
        tech = input_data.get("tech_summary", "").strip()
        market = input_data.get("market_analysis", "").strip()
        finance = input_data.get("finance_summary", "").strip()

        if not all([tech, market, finance]):
            return {"investment_judgement": "필수 분석 결과가 부족하여 판단을 내릴 수 없습니다."}

        prompt = INVESTMENT_AGENT_PROMPT\
            .replace("{{tech_summary}}", tech)\
            .replace("{{market_analysis}}", market)\
            .replace("{{finance_summary}}", finance)

        print("투자 판단을 생성합니다.")
        result = ask_with_context(prompt, context=[], model=self.model)

        return {"investment_judgement": result}
