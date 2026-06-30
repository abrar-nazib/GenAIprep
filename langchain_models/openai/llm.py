from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)

load_dotenv(os.path.join(cwd, ".env"))

llm = OpenAI(model='gpt-3.5-turbo-instruct')


result = llm.invoke("What is the capital of India")

print(result)