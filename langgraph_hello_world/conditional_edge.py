from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    user_input: str
    category:str
    answer:str
    
def classify(state:State):
    text = state["user_input"].lower()
    if "refund" in text:
        return {"category": "refund"}
    return{"category": "general"}

def refund_node(state:State):
    return {"answer": "I can help with your refund. Please share your order id"}

def general_node(state: State):
    return {"answer": "How can I help you?"}

# Router node
def route_after_classify(state: State):
    if state["category"] == "refund":
        return "refund_node"
    return "general_node"


# Initialize the graph with State schema
builder = StateGraph(State)

# Add all nodes
builder.add_node("classify", classify)
builder.add_node("refund_node", refund_node)
builder.add_node("general_node", general_node)

# Define the flow
builder.add_edge(START, "classify")

# Add the conditional branching
builder.add_conditional_edges(
    "classify", # Starting node
    route_after_classify # Routing function that dictates where to go next
)

# Route both end nodes to the finish
builder.add_edge("refund_node", END)
builder.add_edge("general_node", END)

# Compile the graphh into an executable application
graph = builder.compile()

result_1 = graph.invoke({"user_input": "I am angry and I want refund right now!"})
print(result_1)
print()
result_2 = graph.invoke({"user_input": "How can you return my money?"})
print(result_2)
