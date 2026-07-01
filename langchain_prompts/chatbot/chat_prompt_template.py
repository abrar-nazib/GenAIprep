from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# chat_template = ChatPromptTemplate([
#     SystemMessage(content="You are a helpful {domain} expert. You only answer questions related to {domain}. If you think the question topic doesn't have relation to {domain}, you skip it by apologizing that you are a {domain} expert. You can't answer questions related any other domains reliably."),
#     HumanMessage(content="Explain in simple terms, what is {topic}?")
# ])

chat_template = ChatPromptTemplate([
    ('system', "You are a helpful {domain} expert. You only answer questions related to {domain}. If you think the question topic doesn't have relation to {domain}, you skip it by apologizing that you are a {domain} expert. You can't answer questions related any other domains reliably."),
    ('human',"Explain in simple terms, what is {topic}?" )
])

prompt = chat_template.invoke({
    "domain": "Cricket", "topic": "Stero Vision Models"
}) # Weird Behavior

print(prompt)