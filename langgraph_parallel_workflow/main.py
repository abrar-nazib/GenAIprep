from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from pathlib import Path
from dotenv import load_dotenv

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

llm = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    openrouter_provider={
        "order":["baidu", "streamlake"], 
        "allow_fallbacks": True
        },
    
    temperature=0
)

class BatsManState(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int
    
    sr: float
    bpb: float
    boundary_percent: float
    
    summary: str

# Graph
graph = StateGraph(BatsManState)

def calculate_sr(state: BatsManState):
    sr = (state["runs"]/state["balls"]) * 100
    # return state
    return {"sr": sr}

def calculate_bpb(state: BatsManState):
    bpb = state['balls']/(state['fours'] + state['sixes'])
    # return state
    return {"bpb": bpb}

def calculate_boundary_percent(state: BatsManState):
    boundary_percent = (state['fours'] * 4 + state['sixes'] * 6) / state['runs']
    state['boundary_percent'] = boundary_percent * 100
    # return state
    return {"boundary_percent": boundary_percent}

def summary(state: BatsManState):
    summary = f"""
    Strike rate - {state['sr']} \n
    Balls per boundary - {state['bpb']}\n
    Boundary Percent - {state['boundary_percent']}
    """
    state["summary"] = summary
    
    return state

graph.add_node("calculate_sr", calculate_sr)
graph.add_node("calculate_bpb", calculate_bpb)
graph.add_node("calculate_boundary_percent", calculate_boundary_percent)
graph.add_node("summary", summary)

# Declare the edges
graph.add_edge(START, "calculate_sr")
graph.add_edge(START, "calculate_bpb")
graph.add_edge(START, "calculate_boundary_percent")

graph.add_edge("calculate_sr", "summary")
graph.add_edge("calculate_bpb", "summary")
graph.add_edge("calculate_boundary_percent", "summary")

graph.add_edge("summary", END)

workflow = graph.compile()

initial_state:BatsManState = {
    "runs": 130,
    "balls" : 85,
    "fours" : 7,
    "sixes": 4
}

print(workflow.invoke(initial_state))