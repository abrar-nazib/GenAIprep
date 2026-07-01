from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    openrouter_provider={
        "order": ["wandb", "cloudflare", "morph"],
        "allow_fallbacks": False,
    },
    temperature=0,
    max_tokens=1024,
)

messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="Tell me about Langchain in just 2 sentences")
]

result = model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages) 