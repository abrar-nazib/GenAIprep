from dataclasses import dataclass
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage, HumanMessage
from langgraph.types import Command
from langchain_openrouter import ChatOpenRouter
from langchain_tavily import TavilySearch

from dotenv import load_dotenv
from pathlib import Path
# from langchain_core.globals import set_debug

# set_debug(True)

cwd = Path(__file__).parent
print(cwd)

load_dotenv(Path.joinpath(cwd, ".env"))

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0,
)


tavily_tool = TavilySearch(
    max_results=5,
    topic="general"
)

@tool
def write_to_md_file(response: str) -> str:
    """Writes the response to a .md file. If successful, returns the file path. Otherwise returns failure message"""
    if response:
        try:
            output_path = cwd / "output.md"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(response)
            return str(output_path)
        except Exception as e:
            return str(e)
    return "No response was provided to write."
        
agent = create_agent(
    model=model,
    tools=[tavily_tool, write_to_md_file],
    system_prompt="""You are a helpful web serfer agent. Whenever the user asks for anything to be searched from web, you search from web and present the returned data in a human readable and understandable format into a .md file. You present a short summary of your findings to the user as a response.""",
    debug=True
)

messages = [
    HumanMessage("Hi, can you find the prices of cerave facewash for women in bangladeshi shops?")
]

result = agent.invoke({
    "messages": messages
})

print(result)
