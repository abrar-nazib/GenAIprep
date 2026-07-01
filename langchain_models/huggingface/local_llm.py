from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

# Set Downlaod Location for Huggingface
os.environ['HF_HOME'] = "/tmp"

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen3-0.6B",
    task="text-generation",
    pipeline_kwargs=dict(
        temperature=0.5,
        max_new_tokens=1000
    )
)

model = ChatHuggingFace(llm=llm)

result = model.invoke("Name a few Bangladeshi cosmetics brands.")
print(result)
print()
print(result.content)