from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnablePassthrough,
)
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Literal
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature=0,
)


str_parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the feedback.")

pydantic_parser = PydanticOutputParser(pydantic_object=Feedback)

classifier_prompt = PromptTemplate(
    template = "Classify the sentiment of the following feedback text into positive or negative\n\n{feedback}\n{format_instruction}",
    input_variables=["feedback"],
    partial_variables={ "format_instruction": pydantic_parser.get_format_instructions()}
)


positive_response_prompt = PromptTemplate(
    template = "Write an appropriate response to the positive feedback \n {feedback}",
    input_variables=["feedback"]
)
negative_response_prompt = PromptTemplate(
    template = "Write an appropriate response to the negative feedback \n {feedback}",
    input_variables=["feedback"]
)

branch_chain = RunnableBranch(
    (
        lambda x: x["classification"].sentiment == "positive",
        positive_response_prompt | model | str_parser,
    ),
    (
        lambda x: x["classification"].sentiment == "negative",
        negative_response_prompt | model | str_parser,
    ),
    RunnableLambda(lambda x: "Could not find sentiment")
    # Usually chain is executed. Conversion to runnable is needed here.
    # RunnableLambda converts a lambda function into a runnable
)

classifier_chain = classifier_prompt | model | pydantic_parser
chain = (
    RunnablePassthrough.assign(classification=classifier_chain)
    | branch_chain
)

result = chain.invoke({"feedback": "This is a horrible product. You overcharged for the quality"})
print(result)

print("---------------------------------------")

result = chain.invoke({"feedback": "This is a really great product. I kinda feel that you overcharged, but premium comes at a cost."})
print(result)


chain.get_graph().print_ascii()
