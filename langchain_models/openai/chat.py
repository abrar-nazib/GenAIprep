from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)

load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenAI(model="gpt-4")

result = model.invoke("What is the capital of Bangladesh")
print(result)