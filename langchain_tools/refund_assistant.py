from dataclasses import dataclass
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.types import Command
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.globals import set_debug

set_debug(True)


cwd = Path(__file__).parent
print(cwd)

load_dotenv(Path.joinpath(cwd, ".env"))


@dataclass
class UserContext:
    user_id: str
    
    
class RefundState(AgentState):
    authenticated: bool = False
    current_order_id: str | None = None
    
ORDERS = {
    "user_1":{
        "1234": {"status": "delivered", "amount": 49.99, "refundable": True},
        "9999": {"status": "shipped", "amount": 20.00, "refundable": False}, 
    }
}

@tool
def remember_order_id(
    order_id: str,
    runtime: ToolRuntime[UserContext, RefundState]
) -> Command:
    """Remember the order id currently being discussed"""
    return Command(
        update={
            "current_order_id": order_id,
            "messages":[
                ToolMessage(
                    content=f"Remembered order id {order_id}.",
                    tool_call_id = runtime.tool_call_id,
                )
            ]
        }
    )
    
@tool 
def get_current_order(
    runtime: ToolRuntime[UserContext, RefundState],
) -> str:
    """Get details for the current order"""
    user_id = runtime.context.user_id
    order_id = runtime.state.get("current_order_id")
    
    if not order_id:
        return "No order id is currently selected"
    
    order = ORDERS.get(user_id, {}).get(order_id)
    
    if not order:
        return "Order not found for this user"
    
    return str(order)


@tool
def issue_refund(
    runtime:ToolRuntime[UserContext, RefundState],
)->str:
    """Issue refund for the current order if allowed"""
    user_id = runtime.context.user_id
    order_id = runtime.state.get("current_order_id")
    
    if not order_id:
        return "Cannot refund because no order id is selected"
    
    order = ORDERS.get(user_id, {}).get(order_id)
    
    if not order.get("refundable"):
        return "This order is not refundable"
    
    return f"Refund issued for order {order_id}, amount ${order['amount']}"

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0,
)

agent = create_agent(
    model = model,
    tools=[remember_order_id, get_current_order, issue_refund],
    context_schema=UserContext,
    state_schema=RefundState,
    system_prompt="""You are a customer support refund assistant. Before refunding, identify the order id, check the order, and only refund if policy allows.""", 
)

result = agent.invoke(
    {
        "messages":[
            {
                "role": "user",
                "content": "Find transaction #1234 and refund it to me",
            }
        ]
    },
    context=UserContext(user_id="user_1")
)
