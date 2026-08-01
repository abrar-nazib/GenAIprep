from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

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

checkpointer = MemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

png_bytes = workflow.get_graph().draw_mermaid_png()
with open(cwd/f"{__file__.split(".")[0]}.png", "wb") as f:
	f.write(png_bytes)

thread_id = "demo_thread"
config = {
    "configurable": {"thread_id": thread_id}
}

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit", "bye"]:
        print("Goodbye")
        break
        
    result = workflow.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )
    
    ai_message = result["messages"][-1]
    print(f"AI: {ai_message.content}\n")
    
# Get the full persisted state for this thread after chatting
print(workflow.get_state(config))