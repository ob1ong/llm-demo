import os

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


API_KEY = os.getenv("OPENAI_API_KEY")

st.title("gpt")
prompt = st.text_input("enter prompt here", key="prompt")

llm = OpenAI(temperature=0.9)

if prompt:
    response = llm(prompt)