import streamlit as st
from groq import Groq

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

# প্রিমিয়াম ডিজাইন ও ভাসমান ইনপুট বক্সের জন্য CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f0f4f9;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 16px 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        border: 1px solid #e1e6ed !important;
    }
    
    .stChatMessage p {
        color: #1f1f1f !important;
        font-size: 16px !important;
        line-height: 1.5;
    }
    
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
    
    .block-container {
        padding-top: 30px !important;
        padding-bottom: 140px !important;
        max-width: 850px !important;
    }
    </style>
""", unsafe_allow_html=True)

# হেডার ও ভয়েস সিলেক্টর
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("<h3 style='color: #1f1f1f; margin-bottom: 0;'>✨ Gemini AI</h3>", unsafe_allow_html=True)
with col2:
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px; border: 0; border-top: 1px solid #e1e6ed;'>", unsafe_allow_html=True)

# চ্যাট হিস্ট্রি প্রদর্শন এবং প্রতিটি এআই উত্তরের সাথে প্লে (▶️) বাটন যুক্ত করা
for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # যদি মেসেজটি অ্যাসিস্ট্যান্ট বা এআই-এর হয়, তবে নিচে একটি প্লে বাটন দেখাবে
            if message["role"] == "assistant":
                clean_text = message["content"].replace('`', '').replace('"', '\\"').replace('\n', ' ')
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                
                play_button_html = f"""
                <div style="margin-top: 8px;">
                    <button onclick="playVoice_{i}()" style="background-color: #f0f4f9; border: 1px solid #dcdfe5; border-radius: 15px; padding: 5px 12px; cursor: pointer; font-size: 14px; display: inline-flex; align-items: center; gap: 5px;">
                        ▶️ শুনুন
                    </button>
                </div>
                <script>
                function playVoice_{i}() {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        var msg = new SpeechSynthesisUtterance();
                        msg.text = "{clean_text}";
                        msg.lang = 'bn-IN';
                        msg.rate = 1.0;
                        
                        var voices = window.speechSynthesis.getVoices();
                        for(var v = 0; v < voices.length; v++) {{
                            if(voices[v].name.toLowerCase().includes('{selected_voice_filter}') || voices[v].lang.includes('bn')) {{
                                msg.voice = voices[v];
                                break;
                            }}
                        }}
                        window.speechSynthesis.speak(msg);
                    }}
                }}
                </script>
                """
                st.markdown(play_button_html, unsafe_allow_html=True)

# ইউজার ইনপুট
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
                st.rerun()

            except Exception as err:
                st.error(f"ত্রুটি ঘটেছে: {err}")
