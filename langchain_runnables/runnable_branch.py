from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableBranch, RunnablePassthrough
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))


joke_generator_prompt = PromptTemplate(
    template="Write a joke about {topic}",
    input_variables=["topic"]
)

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature=0.7
)


prompt1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="Summarize the following text with a heading.\n{text}",
    input_variables=["text"]
)

parser = StrOutputParser()

report_generation_chain = RunnableSequence(prompt1, model, parser)
summarization_chain = RunnableSequence(prompt2, model, parser)

branch_chain = RunnableBranch(
    (lambda x:len(x.split())>100, summarization_chain),
    RunnablePassthrough()
)

final_chain = RunnableSequence(report_generation_chain, branch_chain)
print(final_chain.invoke({"topic": "Russia vs Ukraine"}))