import streamlit as st
from groq import Groq
from gTTS import gTTS
import os

# পেজ কনফিগারেশন - ফুল উইডথ এবং ক্লিন লুক
st.set_page_config(page_title="Gemini Style AI", page_icon="✨", layout="centered")

# কাস্টম সিএসএস (CSS) দিয়ে ইন্টারফেসকে জেমিনির মতো আকর্ষণীয় করা
st.markdown("""
    <style>
    .stChatInput {
        position: fixed;
        bottom: 20px;
        background: white;
    }
    .main {
        background-color: #f9f9fb;
    }
    h1 {
        color: #1f1f1f;
        font-family: sans-serif;
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>✨ Gemini Style AI Assistant</h1>", unsafe_allow_html=True)

# এপিআই কি চেক
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

# চ্যাট হিস্ট্রি সেটআপ
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a smart, precise, and polite AI assistant like Google Gemini. Give accurate and crisp answers."}
    ]

# আগের মেসেজগুলো স্ক্রিনে দেখানো
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ইউজারের ইনপুট নেওয়ার বক্স
if prompt := st.chat_input("জেমিনির মতো কিছু জিজ্ঞাসা করুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("উত্তর তৈরি হচ্ছে..."):
            try:
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.3
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                # মিষ্টি ও স্পষ্ট স্বরে ভয়েস আউটপুট
                tts = gTTS(text=reply, lang='en', slow=False)
                audio_file = "response.mp3"
                tts.save(audio_file)
                st.audio(audio_file, format='audio/mp3', autoplay=True)

            except Exception as err:
                st.error(f"Error: {err}")
