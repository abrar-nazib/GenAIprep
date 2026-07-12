from langchain.agents import AgentState
from langchain.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command

class SupportState(AgentState):
    authenticated: bool = False
    current_order_id: str | None = None
    
@tool
def mark_authenticated(runtime: ToolRuntime[None, SupportState]) -> Command:
    """Mark the current user as authenticated."""
    return Command(
        update={
            "authenticated": True,
            "messages":[
                ToolMessage(
                    content="User is now authenticated.",
                    tool_call_id = runtime.tool_call_id,
                )
            ]
        }
    )