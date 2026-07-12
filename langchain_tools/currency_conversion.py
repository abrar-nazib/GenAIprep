from langchain_openrouter import ChatOpenRouter
from langchain_core.tools import tool, InjectedToolArg
from langchain_core.messages import HumanMessage, ToolMessage
import requests
from typing import Annotated

from pathlib import Path
from dotenv import load_dotenv
import os

cwd = Path(__file__).parent
load_dotenv(cwd / ".env")

model=ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0
)

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
API_ENDPOINT="https://v6.exchangerate-api.com/v6"

@tool
def get_conversion_factor(base_currency: str, target_currency:str) -> float:
    """Fetches the currency conversion factor between a given base currency and a target currency"""
    if not API_KEY:
        raise ValueError("EXCHANGE_RATE_API_KEY is not set")
    
    url = f"{API_ENDPOINT}/{API_KEY}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    conversion_rate = None
    try:
        data =  response.json()
        conversion_rate = data.get("conversion_rate")
    except Exception as e:
        print(e)
        print(response)
    return conversion_rate
    
@tool
def convert(base_currrency_value: float, conversion_rate: Annotated[float, InjectedToolArg]) -> float:
    """Given a currency conversation, this function calculates the target currency valur from a given base currency value."""
    return base_currrency_value, conversion_rate

# bind tools
llm_with_tools = model.bind_tools([get_conversion_factor, convert])

messages = [HumanMessage("Convert 100 USD to BDT according to today's market conversion rate.")]

ai_message = llm_with_tools.invoke(messages)
print(ai_message.tool_calls)
