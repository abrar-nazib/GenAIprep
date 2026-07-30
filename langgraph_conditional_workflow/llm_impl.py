from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from pydantic import BaseModel, Field

from pathlib import Path
from dotenv import load_dotenv

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

llm = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    openrouter_provider={
        "order":["baidu", "streamlake"], 
        "allow_fallbacks": True
        },
    
    temperature=0
)

class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the review")

class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX", "Performance", "Support", "Other"] = Field(description="The category of issue mentioned in the review.")
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description="The emotional condition of the reviewer.")
    urgency: Literal["low", "medium", "high", "critical"] = Field(description="How urgent or critical the issue is.")

structured_model = llm.with_structured_output(SentimentSchema)
structured_diagnosis_model = llm.with_structured_output(DiagnosisSchema)

class ReviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: dict
    response: str
    
graph = StateGraph(ReviewState)

def find_sentiment(state:ReviewState):
    review = state["review"]
    prompt = f"For the following review find out the sentiment\n{review}"
    result = structured_model.invoke(prompt)
    sentiment = result.sentiment
    return {"sentiment": sentiment}

def check_sentiment(state:ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    if state["sentiment"] == "positive":
        return "positive_response"
    else:
        return "run_diagnosis"
    
def positive_response(state:ReviewState):
    prompt = f"Write a warm thank-you message in response to this review and ask the user to leave a feedback on our website.\n{state['review']}"
    response = llm.invoke(prompt).content
    return {"response": response}

def run_diagnosis(state:ReviewState):
    prompt = f"""Diagnose this negative review:\n\n{state['review']}\n"""
    response = structured_diagnosis_model.invoke(prompt)
    return {'diagnosis': response.model_dump()} # model.dump() converts pydantic model to dictioniary

def negative_response(state:ReviewState):
    diagnosis = state['diagnosis']
    prompt = f"""You are a support assistant\nThe user had a {diagnosis['issue_type']}, sounded {diagnosis['tone']} and marked urgency as {diagnosis['urgency']}."""
    response = llm.invoke(prompt).content
    return {'response': response}

graph.add_node("find_sentiment", find_sentiment)
graph.add_node("positive_response", positive_response)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("negative_response", negative_response)


graph.add_edge(START, "find_sentiment")
graph.add_conditional_edges("find_sentiment", check_sentiment)
graph.add_edge("run_diagnosis", "negative_response")
graph.add_edge("positive_response", END)
graph.add_edge("negative_response", END)

workflow = graph.compile()

png_bytes = workflow.get_graph().draw_mermaid_png()
with open(cwd/f"{__file__.split(".")[0]}.png", "wb") as f:
	f.write(png_bytes)

initial_state:ReviewState = {
    "review": "the product was really bad! I fucking need a refund! Send it asap! The Whole payment gateway integration is fucked up! One click in the pay button cut my balance twice! Fix your moronic website!"
}

 
result = workflow.invoke(initial_state)

print(result)