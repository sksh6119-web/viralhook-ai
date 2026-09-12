import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI Assistant",
    page_icon="✨",
    layout="centered"
)

st.title("✨ AI Assistant")
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
            
            # Format messages for Groq API
            formatted_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            
            payload = {
                "model": "llama3-70b-8192",
                "messages": formatted_messages
            }
            
            # Direct HTTP POST request (Bypasses any library encoding bugs)
            response_obj = requests.post(url, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'))
            
            if response_obj.status_code == 200:
                res_json = response_obj.json()
                response = res_json["choices"][0]["message"]["content"]
            else:
                response = f"API Error ({response_obj.status_code}): {response_obj.text}"
                
        except Exception as e:
            response = f"Connection Error: {str(e)}"
    else:
        response = "API Key is missing in Streamlit Secrets."

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
