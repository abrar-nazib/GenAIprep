from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph.message import add_messages

from typing import TypedDict, Annotated
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

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

graph = StateGraph(ChatState)

def chat_node(state:ChatState):
    messages = state["messages"]
    response = llm.invoke(messages).content
    return{"messages": [AIMessage(response)]} 

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

workflow = graph.compile()

png_bytes = workflow.get_graph().draw_mermaid_png()
with open(cwd/f"{__file__.split(".")[0]}.png", "wb") as f:
	f.write(png_bytes)
 
initial_state = {
    "messages": [HumanMessage("What is the best way out of depression and procastination? I need short to-the-point concise answer")]
}

result = workflow.invoke(initial_state)
print(result)