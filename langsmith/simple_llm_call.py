from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

prompt = PromptTemplate.from_template("{question}")

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    openrouter_provider={
        "order":["baidu", "streamlake"], 
        "allow_fallbacks": True
        },
    
    temperature=0
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"question": "What is the capital of Bangladesh? Write a 100 word paragraph on the capital. How polluted is it will be the main theme."})
print(result)