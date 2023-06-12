import os

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


API_KEY = os.getenv("OPENAI_API_KEY")

st.title("gpt")
prompt = st.text_input("enter prompt here", key="1")

llm = OpenAI()

if prompt:
    response = llm(prompt)
    st.write(response)