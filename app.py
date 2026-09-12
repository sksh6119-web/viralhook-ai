import streamlit as st
import urllib.request
import json

st.set_page_config(
    page_title="Gemini-like AI Assistant",
    page_icon="✨",
    layout="centered"
)

# জেমিনির মতো পরিষ্কার লুক দেওয়ার জন্য কিছু কাস্টম CSS স্টাইল
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ AI Assistant")
st.write("আপনার যেকোনো প্রশ্ন বা স্ক্রিপ্ট এখানে দিন, আমি জেমিনির মতো সুন্দর ও সাবলীলভাবে উত্তর দেব।")

# Get API key safely from Streamlit Secrets
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = None

if "messages" not in st.session_state:
    # এখানে সিস্টেম প্রম্পট সেট করা হলো যাতে এআই একদম মানুষের মতো, সাবলীল এবং জেমিনির স্টাইলে কথা বলে
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are a highly intelligent, natural, and helpful AI assistant, similar to Google Gemini. Speak politely, clearly, and engagingly in Bengali (or the user's requested language) so that it feels like a real human conversation, not robotic. Never break character."
        }
    ]

# ডিসপ্লে করার সময় শুধু ইউজার এবং অ্যাসিস্ট্যান্টের চ্যাট দেখানোর জন্য (সিস্টেম প্রম্পট লুকিয়ে রাখা ভালো)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("এখানে আপনার বার্তা লিখুন..."):
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

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")

            with urllib.request.urlopen(req) as response_obj:
                res_data = json.loads(response_obj.read().decode("utf-8"))
                response = res_data["choices"][0]["message"]["content"]

        except Exception as e:
            response = f"দুঃখিত, একটি সমস্যা হয়েছে: {e}"
    else:
        response = "এপিআই কি (API Key) পাওয়া যায়নি। দয়া করে Streamlit Secrets-এ কি যুক্ত করুন।"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
