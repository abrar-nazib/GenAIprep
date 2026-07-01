from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
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

chat_history = [
    SystemMessage(
        content="You are a helpful AI assistant. You answer in to-the-point and short but understandable manner instead of bluffing. You focus on conceptual understanding and provide examples where needed."
    )
]


while True:
    user_input = input("You: ")
    chat_history.append(HumanMessage(content=user_input))
    if user_input == "exit":
        print("Thank you!")
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content =result.content))
    print("AI: ", result.content)

print(chat_history)
