from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))


joke_generator_prompt = PromptTemplate(
    template="Write a joke about {topic}",
    input_variables=["topic"]
)

joke_explainer_prompt = PromptTemplate(
    template="Explain the following joke\n{joke}",
    input_variables=["joke"]
)

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature=0.7
)

parser = StrOutputParser()

joke_creation_chain = RunnableSequence(joke_generator_prompt, model, parser)
joke_explainer_chain = RunnableSequence(joke_explainer_prompt, model, parser)
parallel_chain = RunnableParallel({
    "joke": RunnablePassthrough(),
    "explanation": joke_explainer_chain
})

chain = RunnableSequence(joke_creation_chain, parallel_chain)
print(chain.invoke({"topic": "Football"}))