from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableLambda
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


parser = StrOutputParser()

joke_creation_chain = RunnableSequence(joke_generator_prompt, model, parser)

def word_counter(text:str):
    return len(text.split())

parallel_chain = RunnableParallel({
    "joke": RunnablePassthrough(),
    "word_count": RunnableLambda(word_counter)
    # "word_count": RunnableLambda(lambda x: len(x.split()) )
})

chain = RunnableSequence(joke_creation_chain, parallel_chain)
print(chain.invoke({"topic": "AI"}))