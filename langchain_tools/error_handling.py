from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langchain_openrouter import ChatOpenRouter

@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
)->ToolMessage:
    """Convert tool exceptions into ToolMessage the model can handle"""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again({e})",
            tool_call_id=request.tool_call["id"]
        )

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0,
)
 
agent = create_agent(
    model=model,
    tools=[],
    middleware=[handle_tool_errors]
)
