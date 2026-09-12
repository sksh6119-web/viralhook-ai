import streamlit as st
from groq import Groq

# পেজ কনফিগারেশন ও জেমিনির মতো আধুনিক লুকের জন্য ফুল কাস্টম CSS ও HTML
st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a supremely knowledgeable, wise, and incredibly friendly AI companion. You have access to all information in the universe and can answer any question accurately and instantly. Always use extremely polite, decent, respectful, and sweet language in Bengali. Never use any harsh, inappropriate, or bad words. When greeted like 'Hi' or 'Hello', warmly and affectionately ask how the user is doing, what's up, and offer a friendly chat just like a caring best friend."}
    ]

# জেমিনির মতো চওড়া, ভাসমান ইনপুট বক্স এবং স্টাইলিশ চ্যাট ডিজাইন সিএসএস
st.markdown("""
    <style>
    /* ডিফল্ট হেডার ও ফুটার হাইড করা */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* মূল ব্যাকগ্রাউন্ড ও ফন্ট */
    .stApp {
        background-color: #ffffff;
    }
    
    /* চ্যাট মেসেজ বক্সগুলোকে জেমিনির মতো রাউন্ড ও সুন্দর করা */
    .stChatMessage {
        background-color: #f0f4f9 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
        border: none !important;
    }
    
    /* ইনপুট বক্সকে জেমিনির মতো একদম নিচে চওড়া ও ভাসমান করা */
    .stChatInput {
        position: fixed !important;
        bottom: 20px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 85% !important;
        max-width: 750px !important;
        background: #f0f4f9 !important;
        border-radius: 30px !important;
        padding: 5px 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        z-index: 99999 !important;
    }
    
    /* লেখার পেজ যাতে ইনপুট বক্সের নিচে ঢাকা না পড়ে */
    .block-container {
        padding-bottom: 120px !important;
        max-width: 800px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ওপরের হেডার ও ভয়েস সিলেক্টর
st.markdown("<h2 style='text-align: center; color: #1f1f1f; font-family: sans-serif;'>✨ Gemini AI</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    voice_gender = st.selectbox("", ["Female", "Male"], label_visibility="collapsed")

# চ্যাট হিস্ট্রি ডিসপ্লে
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ইনপুট বক্স
if prompt := st.chat_input("Gemini-কে কিছু জিজ্ঞাসা করুন..."):
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

                # ব্রাউজার ভয়েস আউটপুট (Male/Female কণ্ঠসহ)
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                js_code = f"""
                <script>
                if ('speechSynthesis' in window) {{
                    var msg = new SpeechSynthesisUtterance();
                    msg.text = `{reply.replace('`', '').replace('"', '\\"')}`;
                    msg.lang = 'bn-BD';
                    var voices = window.speechSynthesis.getVoices();
                    for(var i = 0; i < voices.length; i++) {{
                        if(voices[i].name.toLowerCase().includes('{selected_voice_filter}')) {{
                            msg.voice = voices[i];
                            break;
                        }}
                    }}
                    window.speechSynthesis.speak(msg);
                }}
                </script>
                """
                st.markdown(js_code, unsafe_allow_html=True)

            except Exception as err:
                st.error(f"Error: {err}")
