import streamlit as st
import json
import urllib.request

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("AI Assistant")
st.write("আপনার যেকোনো প্রশ্ন বা প্রম্পট এখানে লিখুন, আমি টেস্লিসার মতো সুক্ষ্ম ও পুঙ্খানুপুঙ্খ উত্তর দেবো।")

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a highly intelligent, natural, and helpful AI assistant, similar to Google Gemini."
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("আপনার বার্তা লিখুন..."):
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
                "model": "llama-3.3-70b-versatile",
                "messages": formatted_messages,
                "temperature": 0.7
            }
            
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            
            with urllib.request.urlopen(req) as response_obj:
                res_data = json.loads(response_obj.read().decode("utf-8"))
                response = res_data["choices"][0]["message"]["content"]
                
        except Exception as e:
            response = f"দুঃখিত, একটি সমস্যা হয়েছে: {e}"
    else:
        response = "এপিআই কি (API Key) পাওয়া যায়নি! দয়া করে Streamlit Secrets-এ কি যুক্ত করুন।"
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
