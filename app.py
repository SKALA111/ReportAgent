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

if __name__ == "__main__":
    result = app.invoke({"startup_name": "퓨리오사AI"})
    print(result)
