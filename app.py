import streamlit as st
from groq import Groq

# পেজ সেটআপ (মোবাইল ফ্রেন্ডলি লুক)
st.set_page_config(page_title="Gemini AI", page_icon="🤖", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

# বন্ধুসুলভ, মার্জিত এবং সবজান্তা হিসেবে আচরণ করার সিস্টেম প্রম্পট
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a supremely knowledgeable, wise, and incredibly friendly AI companion. You have access to all information in the universe and can answer any question accurately and instantly. Always use extremely polite, decent, respectful, and sweet language. Never use any harsh, inappropriate, or bad words. When greeted like 'Hi' or 'Hello', warmly and affectionately ask how the user is doing, what's up, and offer a friendly chat just like a caring best friend."}
    ]

# সিএসএস দিয়ে ইনপুট বক্স এবং ইন্টারফেস ক্লিন রাখা
st.markdown("""
    <style>
    .stChatInput {
        position: fixed !important;
        bottom: 10px !important;
        background: white !important;
    }
    .block-container {
        padding-bottom: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# ভয়েস জেন্ডার নির্বাচন করার ছোট অপশন
col1, col2 = st.columns([4, 1])
with col2:
    voice_gender = st.selectbox("ভয়েস:", ["Female", "Male"])

# চ্যাট হিস্ট্রি ডিসপ্লে করা
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ইউজারের মেসেজ ইনপুট
if prompt := st.chat_input("আপনার যেকোনো প্রশ্ন এখানে লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("উত্তর তৈরি হচ্ছে..."):
            try:
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.5
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                # ব্রাউজারের ভয়েস আউটপুট
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                js_code = f"""
                <script>
                var msg = new SpeechSynthesisUtterance();
                msg.text = `{reply.replace('`', '')}`;
                msg.lang = 'en-US';
                var voices = window.speechSynthesis.getVoices();
                for(var i = 0; i < voices.length; i++) {{
                    if(voices[i].name.toLowerCase().includes('{selected_voice_filter}')) {{
                        msg.voice = voices[i];
                        break;
                    }}
                }}
                window.speechSynthesis.speak(msg);
                </script>
                """
                st.markdown(js_code, unsafe_allow_html=True)

            except Exception as err:
                st.error(f"Error: {err}")
