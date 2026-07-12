from langchain.agents import create_agent
from langchain.agents.middleware import ShellToolMiddleware
from langchain_openrouter import ChatOpenRouter

from pathlib import Path
from dotenv import load_dotenv

cwd = Path(__file__).parent
load_dotenv(cwd / ".env")

model=ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        ShellToolMiddleware(
            workspace_root=cwd,
            startup_commands="pwd",
            tool_name="terminal",
            tool_description=(
                "Run safe shell commands inside the project workspace"
                "Use this to inspect files, list directories and read non-secret files"
            )
        )
    ],
    system_prompt="""You are a coding assistant. You may use the terminal tool to inspect the local project. Do not read .env files, do not modify files. Do not run destructive commands"""
)

result = agent.invoke(
    {
        "messages":[
            {
                "role": "user",
                "content": "List the folders in the current directory and tell me what python files exist."
            }
        ]
    }
)

import json

with open(cwd / "out.json", "w", encoding="utf-8") as f:
    json.dump(
        [message.model_dump() for message in result["messages"]],
        f,
        indent=2,
        ensure_ascii=False,
    )