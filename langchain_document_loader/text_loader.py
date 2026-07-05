from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openrouter import ChatOpenRouter
from pathlib import Path
from dotenv import load_dotenv

file_path = Path(__file__).with_name("test.txt")
env_path = Path(__file__).with_name(".env")
load_dotenv(env_path)

model = ChatOpenRouter(
    model="openai/gpt-4.1-nano",
    temperature=0.7
)

docs = [
    Document(
        page_content=file_path.read_text(encoding="utf-8"),
        metadata={"source": str(file_path)},
    )
]

prompt = PromptTemplate(
    template="Summarize the following text in only one sentence\n\n{text}",
    input_variables=["text"]
)

parser = StrOutputParser()

chain = prompt | model | parser

print(chain.invoke({"text": docs[0].page_content})) 