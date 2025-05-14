import os
import csv
from fpdf import FPDF
from langgraph.graph import StateGraph
from agents.search_agent import SearchAgent
from agents.tech_agent import TechAgent
from agents.market_agent import MarketAgent
from agents.finance_agent import FinanceAgent
from agents.investment_agent import InvestmentAgent
from agents.report_agent import ReportAgent
from typing import TypedDict

# 상태 정의
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

# 분석 함수
def analyze_startups(file_path):
    results = []
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            startup_name = row["스타트업"]
            print(f"Analyzing startup: {startup_name}")
            workflow_result = app.invoke({"startup_name": startup_name})
            print(f"Workflow result for {startup_name}: {workflow_result}")
            results.append({
                "startup_name": startup_name,
                "result": workflow_result
            })
    return results

# 실행부
if __name__ == "__main__":
    file_path = "data/startups.csv"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    analysis_results = analyze_startups(file_path)

    # PDF 생성
    pdf = FPDF()
    pdf.add_page()
    pdf.set_title("투자 분석 최종 보고서")
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "투자 분석 최종 보고서", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(5)

    for entry in analysis_results:
        name = entry["startup_name"]
        report = entry["result"].get("final_report", "").strip()

        pdf.set_font("Arial", "B", 14)
        pdf.multi_cell(0, 10, f"{name}", align="L")

        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, report)
        pdf.ln(8)

    pdf_path = os.path.join(output_dir, "final_report.pdf")
    pdf.output(pdf_path)
    print(f"\n✅ PDF 저장 완료: {pdf_path}")
    print("모든 스타트업 분석 완료.")