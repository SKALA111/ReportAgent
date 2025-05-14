import csv
from langgraph.graph import StateGraph
from agents.search_agent import SearchAgent
from agents.tech_agent import TechAgent
from agents.market_agent import MarketAgent

search = SearchAgent(model="gpt-4")
tech = TechAgent(model="gpt-4")
market = MarketAgent(model="gpt-4")

workflow = StateGraph(dict)
workflow.add_node("Search", search)
workflow.add_node("Tech", tech)
workflow.add_node("Market", market)
workflow.set_entry_point("Search")
workflow.add_edge("Search", "Tech")
workflow.add_edge("Tech", "Market")
workflow.set_finish_point("Market")

app = workflow.compile()

def analyze_startups(file_path):
    results = []
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            startup_name = row["스타트업"]
            print(f"Analyzing startup: {startup_name}")
            result = app.invoke({"startup_name": startup_name})
            results.append({"startup_name": startup_name, "result": result})
    return results

if __name__ == "__main__":
    file_path = "data/startups.csv"
    analysis_results = analyze_startups(file_path)
    for res in analysis_results:
        print(f"Startup: {res['startup_name']}, Analysis Result: {res['result']}")
