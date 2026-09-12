import streamlit as st
from groq import Groq

# পেজ সেটআপ (ওয়াইড লেআউট)
st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

# সিস্টেম প্রম্পট এবং চ্যাট হিস্ট্রি ইনিশিয়ালাইজেশন
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a supremely knowledgeable, wise, and incredibly friendly AI companion. You have access to all information in the universe and can answer any question accurately and instantly. Always use extremely polite, decent, respectful, and sweet language in Bengali. Never use any harsh, inappropriate, or bad words. When greeted like 'Hi' or 'Hello', warmly and affectionately ask how the user is doing, what's up, and offer a friendly chat just like a caring best friend."}
    ]

# জেমিনির মতো প্রিমিয়াম, মডার্ন এবং ফ্লোটিং ইউআই ডিজাইন (CSS)
st.markdown("""
    <style>
    /* ডিফল্ট হেডার ও ফুটার লুকিয়ে ফেলা */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* পেজের ব্যাকগ্রাউন্ড ও কালার টোন */
    .stApp {
        background-color: #f0f4f9;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* চ্যাট মেসেজ কন্টেইনার স্টাইল */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 16px 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        border: 1px solid #e1e6ed !important;
    }
    
    /* ইউজার ও এআইয়ের টেক্সট সাইজ ও কালার */
    .stChatMessage p {
        color: #1f1f1f !important;
        font-size: 16px !important;
        line-height: 1.5;
    }
    
    /* চ্যাট ইনপুট বক্সকে একদম জেমিনির মতো নিচে ভাসমান ও আকর্ষণীয় করা */
    .stChatInput {
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 85% !important;
        max-width: 800px !important;
        background: #ffffff !important;
        border-radius: 30px !important;
        padding: 8px 20px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
        border: 1px solid #dcdfe5 !important;
        z-index: 99999 !important;
    }
    
    /* নিচে ইনপুট বক্সের জন্য পর্যাপ্ত গ্যাপ রাখা যাতে লেখা ঢাকা না পড়ে */
    .block-container {
        padding-top: 30px !important;
        padding-bottom: 140px !important;
        max-width: 850px !important;
    }
    
    /* ভয়েস সিলেক্ট ড্রপডাউন ডিজাইন */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# ওপরের হেডার ও ভয়েস জেন্ডার টগল অপশন
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("<h3 style='color: #1f1f1f; margin-bottom: 0;'>✨ Gemini AI</h3>", unsafe_allow_html=True)
with col2:
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px; border: 0; border-top: 1px solid #e1e6ed;'>", unsafe_allow_html=True)

# চ্যাট হিস্ট্রি স্ক্রিনে রেন্ডার করা
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ইনপুট ফিল্ড এবং প্রম্পট হ্যান্ডলিং
if prompt := st.chat_input("Gemini-কে কিছু জিজ্ঞাসা করুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("চিন্তা করছি..."):
            try:
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.5
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                # ব্রাউজারের ভয়েস আউটপুট স্ক্রিপ্ট (Male/Female কণ্ঠসহ)
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
                st.error(f"ত্রুটি ঘটেছে: {err}")
