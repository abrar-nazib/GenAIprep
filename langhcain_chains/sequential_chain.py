from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    # openrouter_provider={
    #     "order": ["wandb", "cloudflare", "morph"],
    #     "allow_fallbacks": False,
    # },
    temperature=0,
)

prompt1 = PromptTemplate(
    template = "Generate a detailed report (10 sentences) on {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template = "Generate a 2 sentence summary on the following text\n{text}",
    input_variables=['text']
)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic': 'Erling Haaland'})

print(result)

chain.get_graph().print_ascii()
