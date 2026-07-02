from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    openrouter_provider={
        "order": ["wandb", "cloudflare", "morph"],
        "allow_fallbacks": False,
    },
    temperature=0,
    max_tokens=1024,
)

# Define schema
class Review(TypedDict):
    name: Annotated[Optional[str], "Write the name of the reviewer"]
    key_themes: Annotated[list[str], "Write down all the key themes discussed in the review in a list"]
    summary: Annotated[str, "A brief summary of the review in one sentence."]
    sentiment: Annotated[Literal["positive", "negative", "neutral"], "Return sentiment of the review either negative, positive or neutral."]
    pros: Annotated[Optional[list[str]], "Write down all the pros inside a list"]
    cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]

# Create a model that understands the structure
structured_model = model.with_structured_output(Review)

# Invoke the structured model
result = structured_model.invoke("""I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.
The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.
However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

- Nazib Abrar

""")

print(result.keys())
