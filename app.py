import streamlit as st
from groq import Groq
import json

st.set_page_config(
    page_title="Gemini AI Assistant", 
    page_icon="✨", 
    layout="wide"
)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are Gemini AI. Reply accurately in the user's language."
        },
        {
            "role": "assistant", 
            "content": "নমস্কার! 😊 আমি আপনার জেমিনি সহকারী। যারা পড়তে পারেন না, তারা নিচের ভয়েস শুনুন বাটনে ক্লিক করলেই আমি পুরো লেখাটি মুখে পড়ে শোনাবো।"
        }
    ]

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f8f9fa;
        font-family: sans-serif;
    }
    
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        border: 1px solid #e9ecef !important;
    }
    
    .stChatMessage p {
        color: #202124 !important;
        font-size: 16px !important;
        line-height: 1.5;
    }
    
    .stChatInput {
        position: fixed !important;
        bottom: 20px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 85% !important;
        max-width: 800px !important;
        background: #ffffff !important;
        border-radius: 30px !important;
        padding: 4px 14px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        border: 1px solid #dadce0 !important;
        z-index: 99999 !important;
    }
    
    .block-container {
        padding-top: 20px !important;
        padding-bottom: 130px !important;
        max-width: 850px !important;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("<h3 style='color: #202124; margin-bottom: 0;'>✨ Gemini</h3>", unsafe_allow_html=True)
with col2:
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

ad_url = "https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3"
st.markdown(f"""
    <a href="{ad_url}" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #4285f4, #34a853); color: white; padding: 10px 16px; border-radius: 12px; text-align: center; font-size: 14px; font-weight: 500; margin: 10px 0 20px 0;">
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
                selected_filter = "female" if voice_gender == "Female" else "male"
                
                speech_script = f"""
                <div style="display: flex; justify-content: flex-end; margin-top: 10px; border-top: 1px solid #f1f3f4; padding-top: 6px;">
                    <button id="audio_btn_{i}" onclick="playTTS_{i}()" style="background: #e8f0fe; border: 1px solid #d2e3fc; border-radius: 20px; padding: 6px 14px; cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 500; color: #1a73e8;">
                        🔊 ভয়েস শুনুন
                    </button>
                </div>
                <script>
                function playTTS_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('ব্রাউজার ভয়েস সাপোর্ট করে না।');
                        return;
                    }}
                    window.speechSynthesis.cancel();
                    var textToSpeak = {safe_text};
                    var utterance = new SpeechSynthesisUtterance(textToSpeak);
                    utterance.lang = 'bn-IN';
                    utterance.rate = 0.95;
                    
                    var voices = window.speechSynthesis.getVoices();
                    for(var v = 0; v < voices.length; v++) {{
                        if(voices[v].name.toLowerCase().includes('{selected_filter}') || voices[v].lang.includes('bn')) {{
                            utterance.voice = voices[v];
                            break;
                        }}
                    }}
                    
                    var btn = document.getElementById('audio_btn_{i}');
                    utterance.onstart = function() {{
                        btn.style.background = '#fce8e6';
                        btn.style.color = '#c5221f';
                        btn.innerHTML = '🔊 বলছি...';
                    }};
                    utterance.onend = function() {{
                        btn.style.background = '#e8f0fe';
                        btn.style.color = '#1a73e8';
                        btn.innerHTML = '🔊 ভয়েস শুনুন';
                    }};
                    window.speechSynthesis.speak(utterance);
                }}
                </script>
                """
                st.markdown(speech_script, unsafe_allow_html=True)

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
