from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)

load_dotenv(os.path.join(cwd, ".env"))

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=1024) # Custom dimensions not recommended

# documents = [
#     "Sentence 1",
#     "Sentence 2",
#     "Sentence 3"
# ]
# result = embedding.embed_documents(documents)


result  = embedding.embed_query("A quick red fox jumped over a lazy brown dog.")
print(result)