from langchain.tools import tool
from langchain_openrouter import ChatOpenRouter
from langchain.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage, AIMessage
from typing_extensions import TypedDict, Annotated
from langgraph.graph import END, START, StateGraph
from typing import Literal
import operator

from dotenv import load_dotenv
from pathlib import Path
  
cwd = Path(__file__).parent
load_dotenv(cwd/".env")

@tool
def multiply(a:int, b:int)->int:
    """Multiply two integers"""
    return a*b

@tool
def add(a:int, b:int)->int:
    """Add two integers"""
    return a + b

@tool
def divide(a:int, b:int)->float:
    """Divide a by b""" 
    if b == 0:
        raise ValueError("Can't divide by zero")
    return a/b

class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
    # Graph state:
    # { 
    #     "messages" : [...],
    #     "llm_calls": 0
    # }



model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0
)

tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}

model_with_tools = model.bind_tools(tools)

def llm_call(state:MessageState):
    """LLM decides whether to call or answer directly."""
    response = model_with_tools.invoke(
        [
            SystemMessage(
                content=(
                    "You are a helpful assistant. "
                    "Use the calculator tools for arithmetic. "
                    "Do not calculate manually when a tool is available."
                )
            )
        ]
        + state["messages"]
    )
    
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
    
def tool_node(state: MessageState):
    """Execute tool calls requested by the LLM"""
    
    results = []
    last_message = state["messages"][-1]
    
    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        
        results.append(
            ToolMessage(
                content=str(observation),
                tool_call_id = tool_call["id"],
            )
        )

    return {"messages": results}
    
    
def should_continue(state: MessageState) -> Literal["tool_node", "__end__"]:
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        return "tool_node"
    
    return END

graph_builder = StateGraph(MessageState)
graph_builder.add_node("llm_call", llm_call)
graph_builder.add_node("tool_node", tool_node)
graph_builder.add_edge(START, "llm_call")
graph_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
graph_builder.add_edge("tool_node", "llm_call")
agent= graph_builder.compile()


# Non Streaming Background LLM Invokation
# result = agent.invoke({
#     "messages": [
#         HumanMessage(
#             content="Multiply 12 by 7, then add 5, then divide by 3"
#         )
#     ],
#     "llm_calls":0
# })

# for message in result["messages"]:
#     message.pretty_print()
    
# print("LLM Calls:", result["llm_calls"])

# Streaming Invokation
for step in agent.stream(
    {
        "messages":[
            HumanMessage(content="What is 10 plus 5 multiplied by 3?")
        ],
        "llm_calls":0
    },
    stream_mode="updates"
):
    print(step)
    print("-"*80)
