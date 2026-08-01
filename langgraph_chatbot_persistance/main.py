from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

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

class JokeState(TypedDict):
    topic: str
    joke: str
    explanation: str


graph = StateGraph(JokeState)

def generate_joke(state:JokeState):
    prompt = f"Generate a joke on the following topic: {state['topic']}"
    result = llm.invoke(prompt).content
    return {"joke": result}

def generate_explanation(state: JokeState):
    prompt = f"Generate explanation for the following joke: {state["joke"]}"
    result = llm.invoke(prompt).content
    return {"explanation": result}



graph.add_node("generate_joke", generate_joke)
graph.add_node("generate_explanation", generate_explanation)

graph.add_edge(START, "generate_joke")
graph.add_edge("generate_joke", "generate_explanation")
graph.add_edge("generate_explanation", END)

checkpointer = InMemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

png_bytes = workflow.get_graph().draw_mermaid_png(max_retries=5, retry_delay=2.0)
with open(cwd/f"{__file__.split(".")[0]}.png", "wb") as f:
	f.write(png_bytes)

config1 = {"configurable":{"thread_id": "1"}}
config2 = {"configurable":{"thread_id": "2"}}

print(workflow.invoke({"topic": "Pizza"}, config1))

print("-"*30)

print(workflow.invoke({"topic": "Pasta"}, config2))

print("-"*30)

print(workflow.get_state(config1))
print()
print(workflow.get_state_history(config1))

print("-"*30)

print(workflow.get_state(config2))
print()
print(workflow.get_state_history(config2))

print(list(workflow.get_state_history(config2)))