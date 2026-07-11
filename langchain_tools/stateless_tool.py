from langchain.tools import tool

@tool
def get_order_status(order_id: str) -> str:
    """Get order status by order id"""
    return f"Order {order_id} is currently shipped."