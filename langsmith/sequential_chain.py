from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    openrouter_provider={
        "order":["baidu", "streamlake"], 
        "allow_fallbacks": True
        },
    
    temperature=0
)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic': 'Unemployment in Bangladesh'})
print(result)
