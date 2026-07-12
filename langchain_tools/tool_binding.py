from langchain_openrouter import ChatOpenRouter
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
import requests

from pathlib import Path
from dotenv import load_dotenv

cwd = Path(__file__).parent
load_dotenv(cwd / ".env")

model=ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0
)

# Tool Create
@tool
def multiply(a: int, b: int) -> int:
    """Given 2 numbers a and b, tool returns their product"""
    return a * b

llm_with_tools = model.bind_tools([multiply]) # Bind the tools

# Create a conversation history
messages = []
query = HumanMessage("Multiply 33 with 20")
messages.append(query)
response = llm_with_tools.invoke(messages)
messages.append(response)
tool_response = multiply.invoke(response.tool_calls[0])
messages.append(tool_response)
result = llm_with_tools.invoke(messages)
print(result)