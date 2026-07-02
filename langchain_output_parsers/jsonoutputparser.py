from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature=0,
)

parser = JsonOutputParser()

# 1st prompt
template = PromptTemplate(
    template="I want you to prepare 10 titles for LG monitors with different screen sizes and models. Use \" instead of Inch\n{format_instruction}",
    input_variables=[],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

# Old school implementation
# prompt = template.format()

# result = model.invoke(prompt)
# final_result = parser.parse(result.content)
# print(final_result)

# Chain Implementation

chain = template | model | parser

result = chain.invoke({}) # Blank dictionary needed as no input is there

print(result)
