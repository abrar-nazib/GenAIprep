from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)

load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0,
    max_tokens=1024,
    max_retries=2,
)

result = model.invoke("Hi, what's up?")
# print(result)
print(result.content)
print(result.additional_kwargs.get('reasoning_content', 'Didn\'t find anything'))