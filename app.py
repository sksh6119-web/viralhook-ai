import streamlit as st
from groq import Groq
import json

st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Gemini AI. Answer in the user's language accurately."}
    ]

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f0f4f9; font-family: 'Segoe UI', sans-serif; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 18px 22px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e1e6ed !important;
    }
    .stChatMessage p { color: #1f1f1f !important; font-size: 17px !important; line-height: 1.6; }
    .stChatInput {
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 88% !important;
        max-width: 850px !important;
        background: #ffffff !important;
        border-radius: 36px !important;
        padding: 8px 20px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
        border: 1px solid #dcdfe5 !important;
        z-index: 99999 !important;
    }
    .block-container { padding-top: 20px !important; padding-bottom: 150px !important; max-width: 900px !important; }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("<h3 style='color: #1f1f1f; margin-bottom: 0; font-weight: 600;'>✨ Gemini AI</h3>", unsafe_allow_html=True)
with col2:
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

ad_url = "https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3"
st.markdown(f"""
    <a href="{ad_url}" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #1a73e8, #34a853); color: white; padding: 12px 20px; border-radius: 14px; text-align: center; font-size: 15px; font-weight: 600; margin: 10px 0 20px 0; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
            🚀 বিশেষ অফার ও আপডেট দেখতে এখানে ক্লিক করুন! (Sponsored)
        </div>
    </a>
""", unsafe_allow_html=True)

for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant":
                safe_text = json.dumps(message["content"])
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                
                voice_button_html = f"""
                <div style="margin-top: 12px; border-top: 1px solid #f1f3f4; padding-top: 10px; display: flex; justify-content: flex-end;">
                    <button id="speaker_btn_{i}" onclick="speakText_{i}()" style="background: #e8f0fe; border: 1px solid #d2e3fc; border-radius: 24px; padding: 8px 18px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 600; color: #1a73e8;">
                        🔊 ভয়েস শুনুন
                    </button>
                </div>
                
                <script>
                function speakText_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('আপনার ব্রাউজার ভয়েস সাপোর্ট করে না।');
                        return;
                    }}
                    window.speechSynthesis.cancel();
                    var textToSpeak = {safe_text};
                    var msg = new SpeechSynthesisUtterance(textToSpeak);
                    msg.lang = 'bn-IN';
                    msg.rate = 0.95;
                    var voices = window.speechSynthesis.getVoices();
                    for(var v = 0; v < voices.length; v++) {{
                        if(voices[v].name.toLowerCase().includes('{selected_voice_filter}') || voices[v].lang.includes('bn')) {{
                            msg.voice = voices[v];
                            break;
                        }}
                    }}
                    var btn = document.getElementById('speaker_btn_{i}');
                    msg.onstart = function() {{
                        btn.style.background = '#fce8e6';
                        btn.style.color = '#c5221f';
                        btn.innerHTML = '🔊 বলছি...';
                    }};
                    msg.onend = function() {{
                        btn.style.background = '#e8f0fe';
                        btn.style.color = '#1a73e8';
                        btn.innerHTML = '🔊 ভয়েস শুনুন';
                    }};
                    msg.onerror = function() {{
                        btn.style.background = '#e8f0fe';
                        btn.style.color = '#1a73e8';
                        btn.innerHTML = '🔊 ভয়েস শুনুন';
                    }};
                    window.speechSynthesis.speak(msg);
                }}
                </script>
                """
                st.markdown(voice_button_html, unsafe_allow_html=True)

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
                    temperature=0.7
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

            except Exception as err:
                st.error(f"ত্রুটি ঘটেছে: {err}")
