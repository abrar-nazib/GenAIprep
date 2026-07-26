"""Prompt Chaining Example"""

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
        }
    ,
    temperature=0
)


# Create a state
class BlogState(TypedDict):
    title: str
    outline: str
    content: str    

# Create graph
graph = StateGraph(BlogState)

# nodes
def create_outline(state: BlogState) -> BlogState:
    title = state["title"]
    
    prompt = f"Write outline for a blog on the title - {title}."
    
    result = llm.invoke(prompt).content
    state["outline"] = result
    print("outline invoked")
    return state

def create_content(state: BlogState) -> BlogState:
    title = state["title"]
    outline = state["outline"]
    
    prompt = f"Write a detailed blog on the title - {title} using the following outline \n {outline}"
    
    result = llm.invoke(prompt).content
    state["content"] = result
    print("content invoked")
    return state
    


graph.add_node("create_outline", create_outline)
graph.add_node("create_content", create_content)

# Add edges
graph.add_edge(START, "create_outline")
graph.add_edge("create_outline", "create_content")
graph.add_edge("create_content", END)


# Compile Graph
workflow = graph.compile()

# Invoke
initial_state = {"title": "Acceptance of Failure is required for Growth."}
result:BlogState = workflow.invoke(initial_state)
print(result["title"])
print(result["outline"])
print(result["content"])