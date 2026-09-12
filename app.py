import streamlit as st
import urllib.request
import json

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Assistant")
st.write("Ask your questions below.")

# Get API key safely from Streamlit Secrets
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = None

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if groq_api_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }

            formatted_messages = [
                {"role": x["role"], "content": x["content"]}
                for x in st.session_state.messages
            ]

            payload = {
                "model": "llama3-70b-8192",
                "messages": formatted_messages
            }

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")

            with urllib.request.urlopen(req) as response_obj:
                res_data = json.loads(response_obj.read().decode("utf-8"))
                response = res_data["choices"][0]["message"]["content"]

        except Exception as e:
            response = f"Error: {e}"
    else:
        response = "API Key is missing in Streamlit Secrets."

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
