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
chat_history = []


while True:
    user_input = input('You: ')
    chat_history.append(user_input)
    if user_input == 'exit':
        print("Thank you!")
        break
    result = model.invoke(chat_history)
    chat_history.append(result.content)
    print("AI: ", result.content)
    
print(chat_history)
    
    