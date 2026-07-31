from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langchain.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

from typing import TypedDict, Literal, Annotated
from pathlib import Path
from dotenv import load_dotenv
from operator import add

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

OLLAMA_CLOUD_URL = "https://ollama.com"

generator_llm = ChatOllama(
    model="deepseek-v4-flash:cloud",
    base_url=OLLAMA_CLOUD_URL,
    temperature=0
)

evaluator_llm = ChatOllama(
    model="minimax-m3:cloud",
    base_url=OLLAMA_CLOUD_URL,
    temperature=0
)

optimizer_llm = ChatOllama(
    model="glm-5.2:cloud",
    base_url=OLLAMA_CLOUD_URL,
    temperature=0
)

class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvement"] = Field(description="Final verdict on whether the tweet is good enough to post.")
    feedback: str = Field(description="One paragraph explaining the strengths and weaknesses of the tweet.")

structured_evaluator_llm = evaluator_llm.with_structured_output(TweetEvaluation, method="function_calling")

# State
class TweetState(TypedDict):
    topic: str
    tweet: str
    evaluation: Literal["approved", "needs_improvement"]
    feedback: str
    iteration: int
    max_iteration: int
    tweet_history: Annotated[list[str], add]
    
graph = StateGraph(TweetState)

def generate_tweet(state:TweetState):
    # Prompt
    messages = [
        SystemMessage(content="You are a funny and clever Twitter/X influencer."),
        HumanMessage(content=f"""
    Write a short, original and hillarious tweet on the topic "{state['topic']}".
    Rules:
    - Do not use question-answer format.
    - Max 280 characters
    - Use observational humor, irony, sarcasm or cultural references.
    - Think in meme logic, punchlines or relatable takes.
    - Use simple day-to-day englies.
    """)
    ]
    
    # Send generator llm
    response = generator_llm.invoke(messages).content
    return {'tweet': response, "tweet_history":[response]}
    
def evaluate_tweet(state:TweetState):
    # prompt
    messages = [
        SystemMessage(content="You are a ruthless, no-laugh-given Twitter critic. You evaluate tweets for humor, originality, and virality with zero patience for mediocrity."),
        HumanMessage(content=f"""
    Evaluate the following tweet:

    Tweet: "{state['tweet']}"

    Use the criteria below to evaluate the tweet:

    1. Originality - Is this fresh, or have you seen it a hundred times before?
    2. Humor - Did it genuinely make you smile, laugh, or chuckle?
    3. Punchiness - Is it short, sharp, and scroll-stopping?
    4. Virality Potential - Would people retweet or share it?
    5. Format - Is it a well-formed tweet (not a setup-punchline joke, not a Q&A joke, and under 280 characters)

    Auto-reject if:
    - It's written in question-answer format (e.g., "Why did..." or "What happens when...")
    - It exceeds 280 characters
    - It reads like a traditional setup-punchline joke
    - Dont end with generic, throwaway, or deflating lines that weaken the humor
    - It's just nonsense
    - It's not funny enough

    """)
    ]

    response = structured_evaluator_llm.invoke(messages)
    print(response)
    return {"evaluation": response.evaluation, "feedback": response.feedback}

def optimize_tweet(state:TweetState):
    messages = [
        SystemMessage(content="You punch up tweets for virality and humor based on given feedback."),
        HumanMessage(content=f"""
    Improve the tweet based on this feedback:
    "{state['feedback']}"

    Topic: "{state['topic']}"
    Original Tweet:
    {state['tweet']}

    Re-write it as a short, viral-worthy tweet. Avoid Q&A style and stay under 280 characters.
    """)
    ]

    response = optimizer_llm.invoke(messages).content
    return {'tweet': response, 'iteration': state['iteration'] + 1, "tweet_history": [response]}

def route_evaluation(state: TweetState):
    if state['evaluation'] == 'approved' or state['iteration'] >= state['max_iteration']:
        return "approved"
    else:
        return "needs_improvement"

graph.add_node("generate", generate_tweet)
graph.add_node("evaluate", evaluate_tweet)
graph.add_node("optimize", optimize_tweet)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")
graph.add_conditional_edges("evaluate", route_evaluation, {'approved':END, 'needs_improvement': "optimize"})
graph.add_edge("optimize", "evaluate")

workflow = graph.compile()

png_bytes = workflow.get_graph().draw_mermaid_png()
with open(cwd/f"{__file__.split(".")[0]}.png", "wb") as f:
	f.write(png_bytes)
 
initial_state = {
    "topic": "Is there a Black Person here and Is there a Black Purse in here",
    "max_iteration": 5,
    "iteration": 1
}

result = workflow.invoke(initial_state)
print(result)
print(result["iteration"])