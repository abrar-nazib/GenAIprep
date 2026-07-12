from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

@tool
def get_last_user_message(runtime:ToolRuntime) -> str:
    """Get the latest user message."""
    messages = runtime.state["messages"]
    
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return message.content
        
    return "No user message found"