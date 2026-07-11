from pydantic import BaseModel, Field
from typing import Literal
from langchain.tools import tool

class WeatherInput(BaseModel):
    """Input for weather queries"""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    
    include_forecast: bool = Field(
        default = False,
        description="Include 5-day forecast"
    )
    
@tool(args_schema=WeatherInput)
def get_weather(location:str, units:str="celsius", include_forcast:bool=False) -> str:
    """Get current weather and optional forecast"""
    temp=22 if units == "celsius" else 72
    result = f"Current weather in {location} is {temp} degrees {units}"
    if include_forcast:
        result +="\n Next 5 days: Sunny"
    return result