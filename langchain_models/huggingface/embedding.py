from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

# Set Downlaod Location for Huggingface
os.environ['HF_HOME'] = "/tmp"

embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

text = "This is a product of brand lenovo"

vector = embedding.embed_query(text)
print(vector)