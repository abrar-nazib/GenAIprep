from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

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

class QuadState(TypedDict):
    a: float
    b: float
    c: float
    
    equation: str
    discriminant: float
    result: str
    
graph = StateGraph(QuadState)

def show_equation(state:QuadState):
    equation = f"{state['a']}x + {state['b']}x + {state['c']}"
    
    return {'equation': equation}

def calculate_discriminant(state: QuadState):
    discriminant = state["b"]**2 - (4 * state["a"]*state["c"])
    return {"discriminant": discriminant}

def real_roots(state:QuadState):
    a, b, c = state['a'], state['b'], state['c']
    d = state['discriminant']
    root1 = -b + d**0.5/2*a
    root2 = -b - d**0.5/2*a
    
    result = f"The roots are {root1} and {root2}"
    
    return {"result": result}

def repeated_roots(state:QuadState):
    a, b, c = state['a'], state['b'], state['c']
    d = state['discriminant']
    root = -b / 2*a
    
    result = f"Only Repeating root is {root}."
    
    return {"result": result}

def no_real_roots(state:QuadState):
    return {"result": "No real roots"}

def check_condition(state: QuadState) -> Literal["real_roots", "repeated_roots", "no_real_roots"]:
    if state["discriminant"] > 0:
        return "real_roots"
    elif state["discriminant"] == 0:
        return "repeated_roots"
    else:
        return "no_real_roots"

graph.add_node("show_equation", show_equation)
graph.add_node("calculate_discriminant", calculate_discriminant)
graph.add_node("real_roots", real_roots)
graph.add_node("repeated_roots", repeated_roots)
graph.add_node("no_real_roots", no_real_roots)

graph.add_edge(START, "show_equation")
graph.add_edge("show_equation", "calculate_discriminant")

graph.add_conditional_edges("calculate_discriminant", check_condition)

graph.add_edge("real_roots", END)
graph.add_edge("repeated_roots", END)
graph.add_edge("no_real_roots", END)

workflow = graph.compile()

png_bytes = workflow.get_graph().draw_mermaid_png()
with open(cwd/"graph.png", "wb") as f:
	f.write(png_bytes)

initial_state:QuadState = {
    "a" : 2,
    "b": 4,
    "c" : 2
}

 
result = workflow.invoke(initial_state)

print(result)