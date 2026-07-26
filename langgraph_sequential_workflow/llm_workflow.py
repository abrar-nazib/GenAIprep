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


# Create a state
class LLMState(TypedDict):
    question: str
    answer: str
    
# Create graph
graph = StateGraph(LLMState)

# Add node
def llm_qa(state:LLMState) -> LLMState:
    question = state["question"]
    
    prompt = f"Answer the following question {question}"
    
    answer = llm.invoke(prompt).content
    
    state['answer'] = answer
    
    return state
    
graph.add_node("llm_qa", llm_qa)


# Add edge
graph.add_edge(START, "llm_qa")
graph.add_edge("llm_qa", END)

workflow = graph.compile()

initial_state = {"question": "How far is moon from earth?"}
result = workflow.invoke(initial_state)
print(result)