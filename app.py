from langgraph.graph import StateGraph
from agents.search_agent import SearchAgent
from agents.tech_agent import TechAgent

search = SearchAgent(model="gpt-4")
tech = TechAgent(model="gpt-4")

workflow = StateGraph(dict)
workflow.add_node("Search", search)
workflow.add_node("Tech", tech)
workflow.set_entry_point("Search")
workflow.add_edge("Search", "Tech")
workflow.set_finish_point("Tech")

app = workflow.compile()

if __name__ == "__main__":
    result = app.invoke({"startup_name": "퓨리오사AI"})
    print(result)
