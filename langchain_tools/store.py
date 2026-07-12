from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id: str


@tool
def save_preference(key: str, value: str, runtime: ToolRuntime[UserContext]) -> str:
    """Save a user preference"""
    user_id = runtime.context.user_id
    runtime.store.put(("preferences", user_id), key, value)
    return f"Saved preference {key} = {value}"
    
    
# ("preferences", "user_1") -> {"language": "Bengali"}
