import streamlit as st
import urllib.request
import json

st.title("AI Assistant")

api_key = st.secrets.get("GROQ_API_KEY")

prompt = st.chat_input("আপনার বার্তা লিখুন...")
if prompt:
    st.write(prompt)
