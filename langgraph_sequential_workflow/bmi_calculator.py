from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from pathlib import Path
from dotenv import load_dotenv

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

llm = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0
)

# Define the state
class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    
# Define the graph
graph = StateGraph(BMIState) # Pass the state while defining the graph

# Create Nodes
def calculate_bmi(state: BMIState) -> BMIState:
    height= state["height_m"]
    weight = state["weight_kg"]
    bmi = weight/(height**2)
    state["bmi"] = round(bmi, 2)
    return state # Returning state is important    

# Add Nodes
graph.add_node("calculate_bmi", calculate_bmi)

# Add Edges
graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", END)

# Compile Graph
workflow = graph.compile()

# Execute the Graph
initial_state = {"weight_kg": 80, "height_m": 1.73}
output_state = workflow.invoke(initial_state)
print(output_state)
png_bytes = workflow.get_graph().draw_mermaid_png()
with open(cwd/"graph.png", "wb") as f:
    f.write(png_bytes)