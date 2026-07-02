from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature=0,
)

class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age:int = Field(gt=18, description="Age of the person")
    city: str = Field(description="Name of the city the person belongs to")
    
parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template="Generate the name, age and city of the most famous {place} footballer \n{format_instruction}",
    input_variables=['place'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

# Oldschool invokation
# prompt = template.invoke({'place': 'Bangladesh'})
# print(prompt)
# result = model.invoke(prompt)
# final_result = parser.parse(result.content)
# print(final_result)

# Chain Invokation
chain = template | model | parser
final_result = chain.invoke({'place': 'Norwaygian'})
print(final_result)
