from langchain_openrouter import ChatOpenRouter
from langchain.messages import HumanMessage, ToolMessage, AIMessage
from langgraph.types import Command, interrupt, RetryPolicy
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


from typing import TypedDict, Literal
from pathlib import Path
from dotenv import load_dotenv

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

llm = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0
)

class EmailClassification(TypedDict):
    intent: Literal["question", "bug", "billing", "feature", "complex"]
    urgency: Literal["low", "medium", "high", "critical"]
    topic: str
    summary: str
    
class EmailAgentState(TypedDict):
    email_content:str # Pushed content to agent state
    sender_email: str
    email_id: str
    
    classification: EmailClassification
    search_results: list[str] | None
    custoemr_history: dict | None
    
    draft_response: str | None
    messages: list[str] | None
    

# Read Email Node: Starts the workflow
def read_email(state: EmailAgentState) -> dict:
    """Extract and parse email content."""
    return {
        "messages":[
            HumanMessage(
                content=f"Processing email: {state['email_content']}"
            )
        ]
    }
    
# Classify Intent Node: Decision Making
def classify_intent(state: EmailAgentState)->Command[Literal[
    "search_documentation", "human_review", "draft_response", "bug_tracking"
]]:
    # Updates state with classification
    # Decides the next node
    
    structured_llm = llm.with_structured_output(EmailClassification)
    classification_prompt = f"""Analyze this customer support email.
    Email:
    {state['email_content']}
    
    From:
    {state['sender_email']}
    """
    classification:EmailClassification = structured_llm.invoke(classification_prompt)
    
    if classification["intent"] == "billing" or classification["urgency"] == "critical":
        goto="human_review"
    elif classification["intent"] in ["question", "features"]:
        goto = "search_documentation"
    elif classification["intent"] == "bug":
        goto = "bug_tracking"
    else:
        goto = "draft_response"
    
    # Update the internal state
    return Command(
        update={"classification": classification},
        goto=goto
    )
    
# Search Documentation Node. Retrieves Information
def search_documentation(
    state:EmailAgentState
) -> Command[Literal["draft_response"]]:
    classification: EmailClassification = state.get("classification") or {}
    query = f"{classification.get('intent', '')} {classification.get('topic', '')}"
    
    # Fake document search result
    search_results = [
        "Reset password via settings > security > change password.",
        "Password must be at least 12 characters.",
        "Use uppercase, lowercase, numbers and symbols."
    ]
    
    return Command(
        update={"search_results": search_results},
        goto="draft_response"
    )
    
def bug_tracking(
    state: EmailAgentState,
) -> Command[Literal["draft_response"]]:
    # Take the state and do something and create a ticket.
    ticket_id = "BUG_12345"
    
    return Command(
        update={"search_results": [f"Bug ticket {ticket_id} created"]},
        goto="draft_response"
    )
    
def draft_response(
    state: EmailAgentState
) -> Command[Literal["human_review", "send_reply"]]:
    classification = state.get("classification") or {}
    
    # Enrich The Context
    context_sections = []
    
    if state.get("search_results"):
        formatted_docs = "\n".join(
            f" - {doc}" for doc in state["search_results"]
        )
        context_sections.append("Relevant Documentation:\n{formatted_docs}")    
        
    
    if state.get("custoemr_history"):
        customer_tier = state["custoemr_history"].get("tier", "standard")
        context_sections.append(f"Customer tier: {customer_tier}")
        
    draft_prompt = f"""Draft a professional customer support response.
    Original Email:
    {state["email_content"]}
    
    Intent:
    {classification.get("intent", "unknown")}
    
    Urgency:
    {classification.get("urgency", "medium")}
    
    Context:
    {chr(10).join(context_sections)}
    
    Guidelines:
    - Be professional and helpful.
    - Address the customer's specific concern.
    - Use documentation when relevant.
    - Do not invent facts
    """
    response = llm.invoke(draft_prompt)
    needs_review = (
        classification.get("urgency") in ["high", "critical"]
        or classification.get("intent") == "complex"
    )
    
    goto="human_review" if needs_review else "send_reply"
    
    return Command(
        update={"draft_response": response.content},
        goto=goto,
    )
    
def  human_review(state: EmailAgentState) -> Command[Literal["send_reply", "__end__"]]:
    classification = state.get("classification") or {}
    
    human_decision = interrupt(
        {
            "email_id": state["email_id"],
            "original_email": state["email_content"],
            "draft_response": state.get("draft_response", ""),
            "urgency": classification.get("urgency"),
            "intent": classification.get("intent"),
            "action": "Please approve or edit this response",
        }
    )
    
    if human_decision.get("approved"):
        return Command(
            update={
                "draft_response": human_decision.get(
                    "edited_response",
                    state.get("draft_response", ""),
                )
            },
            goto="send_reply"
        )
    return Command(update={}, goto="__end__")


def send_reply(state:EmailAgentState) -> dict:
    """Send the email response"""
    
    # Real version would call email api
    print(f"Sending reply to {state["sender_email"]}:")
    print(state["draft_response"])
    
    return {}

workflow = StateGraph(EmailAgentState)
workflow.add_node("read_email", read_email)
workflow.add_node("classify_intent", classify_intent)
workflow.add_node("search_documentation", search_documentation, retry_policy=RetryPolicy(max_attempts=2))

workflow.add_node("bug_tracking", bug_tracking)
workflow.add_node("draft_response", draft_response)
workflow.add_node("human_review", human_review)
workflow.add_node("send_reply", send_reply)


workflow.add_edge(START, "read_email")
workflow.add_edge("read_email", "classify_intent")
workflow.add_edge("send_reply", END)

checkpointer = InMemorySaver()

app = workflow.compile(checkpointer=checkpointer)


initial_state:EmailAgentState = {
    "email_content": "How do I reset my password?",
    "sender_email": "abrar@example.com",
    "email_id": "email_001",
    "classification": None,
    "search_results": None,
    "custoemr_history": None,
    "draft_response" : None,
    "messages": None
}

config = {"configurable": {"thread_id": "email_001"}}

# result = app.invoke(initial_state, config=config)

# print("\nFinal State:")
# print(result)
for event in app.stream(
    initial_state,
    config=config, # Needed for 
    stream_mode="updates",
):
    print("-"*80)
    print(event)