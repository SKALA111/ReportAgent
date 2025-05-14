from langchain_core.runnables import Runnable
from prompts.prompt import REPORT_AGENT_PROMPT
from models.llm_wrapper import ask_with_context

class ReportAgent(Runnable):
    def __init__(self, model):
        self.model = model

    def invoke(self, input_data: dict, config=None) -> dict:
        tech = input_data.get("tech_summary", "")
        market = input_data.get("market_analysis", "")
        finance = input_data.get("finance_summary", "")
        judgement = input_data.get("investment_judgement", "")

        if not all([tech, market, finance, judgement]):
            return {"final_report": "ReportAgent: 입력값 부족"}

        prompt = REPORT_AGENT_PROMPT\
            .replace("{{tech_summary}}", tech)\
            .replace("{{market_analysis}}", market)\
            .replace("{{finance_summary}}", finance)\
            .replace("{{investment_judgement}}", judgement)

        print("최종 보고서 생성 중...")
        result = ask_with_context(prompt, context=[], model=self.model)

        return {"final_report": result}
