from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature=0,
)

# 1st prompt
template1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)

# Second prompt
template2 = PromptTemplate(
    template = "Write a 5 sentence summary of the following text.\nReport on {text}",
    input_variables=["text"]
)

# Old usual way
# prompt1 = template1.invoke({'topic': 'black hole'})
# result = model.invoke(prompt1)
# prompt2 = template2.invoke({'text': result.content})
# result2 = model.invoke(prompt2)
# print(result2)

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model  | parser

result = chain.invoke({'topic': 'black_hole'})

print(result)