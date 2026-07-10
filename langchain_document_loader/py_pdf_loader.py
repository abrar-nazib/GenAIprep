from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openrouter import ChatOpenRouter
from pathlib import Path
from dotenv import load_dotenv

file_path = Path(__file__).with_name("test.pdf")
env_path = Path(__file__).with_name(".env")
load_dotenv(env_path)

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature = 0.8   
)

loader = PyMuPDF4LLMLoader(
    file_path = file_path,
    mode = "page" # One document per page
    # mode = "single" # For combined document
)

docs = loader.load()
print(len(docs))
print()
print(docs)

