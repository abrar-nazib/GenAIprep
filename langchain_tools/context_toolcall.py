from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langchain_openrouter import ChatOpenRouter

@dataclass
class UserContext:
    user_id: str
    
USER_DB = {
    "user_1":{
        "name": "Abrar",
        "plan": "premium",
        "balance": 120,
    }
}

@tool
def get_account_info(runtime:ToolRuntime[UserContext]) -> str:
    """Get current user's account info"""
    user_id = runtime.context.user_id
    user=USER_DB[user_id]
    
    return f"Name: {user['name']}, Plan: {user['plan']}, Balance: {user['balance']}"


