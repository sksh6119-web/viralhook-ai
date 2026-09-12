import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Assistant",
    page_icon="✨",
    layout="centered"
)

st.title("✨ AI Assistant")
st.write("Ask your questions below.")

# Initialize Groq client safely
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    client = None
    st.error("Please set your GROQ_API_KEY in Streamlit Secrets.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if client:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                model="llama3-70b-8192",
            )
            response = chat_completion.choices[0].message.content
        except Exception as e:
            response = f"An error occurred: {str(e)}"
    else:
        response = "API Key is not configured properly."

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
