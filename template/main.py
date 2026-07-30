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

class DummyState(TypedDict):
    key: str
    
graph = StateGraph(DummyState)
workflow = graph.compile()

png_bytes = workflow.get_graph().draw_mermaid_png()
with open(cwd/f"{__file__.split(".")[0]}.png", "wb") as f:
	f.write(png_bytes)