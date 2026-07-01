from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))

# Chat template
chat_template = ChatPromptTemplate(
    [
        ('system', 'You are a helpful customer support agent. You handle angry customers with patience.'),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{query}')
    ]
)

chat_history = []

# Load Chat history
with open(os.path.join(cwd, "chat_history.txt")) as f:
    for line in f:
        role, content = line.strip().split(":", 1)

        if role.lower() == "human":
            chat_history.append(HumanMessage(content=content.strip()))
        elif role.lower() == "ai":
            chat_history.append(AIMessage(content=content.strip()))
    
prompt = chat_template.invoke({
    'chat_history':chat_history,
    'query': "Where is my refund?"
})

print(prompt)
    
    
