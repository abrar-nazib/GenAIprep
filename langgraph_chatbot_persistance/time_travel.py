from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

# 1. Define State Schema
class State(TypedDict):
    topic: str
    joke: NotRequired[str]
    explanation: NotRequired[str]

# 2. Define Nodes
def generate_joke(state: State):
    # In a real app, an LLM generates this dynamically based on state["topic"]
    return {"joke": f"Why did the {state['topic']} break up with the ravioli? It couldn't handle the emotional baggage!"}

def generate_explanation(state: State):
    # In a real app, an LLM explains the pun based on state["joke"]
    return {"explanation": f"Explaining the joke: '{state['joke']}' - It is a pun on physical vs emotional baggage."}

# 3. Build and Compile the Graph with Persistence
checkpointer = InMemorySaver()
builder = StateGraph(State)

builder.add_node("generate_joke", generate_joke)
builder.add_node("generate_explanation", generate_explanation)

builder.add_edge(START, "generate_joke")
builder.add_edge("generate_joke", "generate_explanation")
builder.add_edge("generate_explanation", END)

# Passing the checkpointer enables persistence and time travel
graph = builder.compile(checkpointer=checkpointer)

# ==========================================
# TUTORIAL EXECUTION
# ==========================================

# Step 1: Initial Standard Run
print("--- FIRST RUN ---")
config = {"configurable": {"thread_id": "thread-1"}}
initial_state = graph.invoke({"topic": "Pasta"}, config)

print(f"Final Joke: {initial_state.get('joke')}")
print(f"Final Explanation: {initial_state.get('explanation')}\n")


# Step 2: View State History
print("--- STATE HISTORY ---")
# get_state_history returns checkpoints in reverse chronological order
history = list(graph.get_state_history(config))
for idx, checkpoint in enumerate(history):
    print(f"Checkpoint {idx}: next={checkpoint.next}, checkpoint_id={checkpoint.config['configurable']['checkpoint_id']}")
print("\n")


# Step 3: Time Travel (Forking)
print("--- TIME TRAVEL (FORKING) ---")
# Find the specific checkpoint after the joke was generated, but BEFORE the explanation.
# We look for the state where the 'next' node queued up is 'generate_explanation'.
joke_checkpoint = [s for s in history if s.next == ("generate_explanation",)][0]

# Time Travel: We update the state at that specific past checkpoint with a completely different joke.
# This creates a new config pointing to a forked timeline.
fork_config = graph.update_state(
    joke_checkpoint.config, 
    {"joke": "Why did the pasta refuse to fight? It was an impasta!"}
)

# Resume execution from the fork. 
# We pass `None` as the input because the state is already loaded from the fork_config.
forked_state = graph.invoke(None, fork_config)

print(f"Forked Joke: {forked_state.get('joke')}")
print(f"Forked Explanation: {forked_state.get('explanation')}")