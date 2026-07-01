from langchain_openrouter import ChatOpenRouter
import streamlit as st
from langchain_core.prompts import load_prompt
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)

load_dotenv(os.path.join(cwd, ".env"))

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0,
    max_tokens=1024,
    max_retries=2,
)

st.header("Research Toool")

paper_input = st.selectbox(
    "Select Research Paper Name",
    [
        "Select...",
        "Attention Is All You Need",
        "BERT: pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis",
    ],
)

style_input = st.selectbox(
    "Select Explanation Style",
    ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"],
)

length_input = st.selectbox(
    "Select Explanation Length",
    ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Mathematical"],
)

# Template
template = load_prompt(os.path.join(cwd, "template.json"))

# prompt = template.invoke(
#     {
#         "paper_input": paper_input,
#         "style_input": style_input,
#         "length_input": length_input,
#     }
# )

if st.button("Summarize"):
    chain = template | model

    result = chain.invoke(
        {
            "paper_input": paper_input,
            "style_input": style_input,
            "length_input": length_input,
        }
    )
    content = result.content
    # Replace bracket delimiters with Streamlit-friendly dollar signs
    content = content.replace("\\[", "$$").replace("\\]", "$$")
    content = content.replace("\\(", "$").replace("\\)", "$")

    st.markdown(content)
