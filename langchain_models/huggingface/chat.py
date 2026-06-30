from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

# Configure Endpoint
llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Flash",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

result = model.invoke("Where is Rajshahi?")
print(result)
print()
print(result.content)