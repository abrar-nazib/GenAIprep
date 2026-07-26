from langchain_openrouter import ChatOpenRouter

from pathlib import Path
from dotenv import load_dotenv

cwd = Path(__file__).parent
load_dotenv(cwd/".env")

llm = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    openrouter_provider={
        "order":["baidu", "streamlake"], 
        "allow_fallbacks": True
        }
    
    temperature=0
)

