import json
import os
import csv
from langgraph.graph import StateGraph
from agents.search_agent import SearchAgent
from agents.tech_agent import TechAgent
from agents.market_agent import MarketAgent
from agents.finance_agent import FinanceAgent
from agents.investment_agent import InvestmentAgent
from agents.report_agent import ReportAgent
from typing import TypedDict

class WorkflowState(TypedDict):
    startup_name: str
    search_docs: list[str]
    tech_summary: str
    market_analysis: str
    finance_summary: str
    investment_judgement: str


# 에이전트 초기화
search = SearchAgent(model="gpt-4")
tech = TechAgent(model="gpt-4")
market = MarketAgent(model="gpt-4")
finance = FinanceAgent(model="gpt-4")
investment = InvestmentAgent(model="gpt-4")
report = ReportAgent(model="gpt-4")

# 워크플로우 정의
workflow = StateGraph(WorkflowState)

workflow.add_node("Search", search)
workflow.add_node("Tech", tech)
workflow.add_node("Finance", finance)
workflow.add_node("Market", market)
workflow.add_node("Investment", investment)
workflow.add_node("Report", report)

workflow.set_entry_point("Search")
workflow.add_edge("Search", "Tech")
workflow.add_edge("Search", "Finance")
workflow.add_edge("Tech", "Market")
workflow.add_edge("Market", "Investment")
workflow.add_edge("Finance", "Investment")
workflow.add_edge("Investment", "Report")
workflow.set_finish_point("Report")

app = workflow.compile()

def analyze_startups(file_path):
    results = []
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            startup_name = row["스타트업"]
            print(f"Analyzing startup: {startup_name}")

            # 워크플로우를 한 번만 실행
            workflow_result = app.invoke({"startup_name": startup_name})

            # 디버깅: 각 노드의 출력 확인
            print(f"Workflow result for {startup_name}: {workflow_result}")

            # 결과 저장
            results.append({
                "startup_name": startup_name,
                "result": workflow_result
            })
    return results

if __name__ == "__main__":
    file_path = "data/startups.csv"
    analysis_results = analyze_startups(file_path)
    for res in analysis_results:
        print(f"Startup: {res['startup_name']}, Analysis Result: {res['result']}")

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
