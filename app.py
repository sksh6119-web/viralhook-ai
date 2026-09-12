import streamlit as st
from groq import Groq
from gtts import gTTS
import os

st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Gemini AI. Always reply accurately and fluently in the user's language. Be polite and helpful."},
        {"role": "assistant", "content": "নমস্কার! 😊 আমি আপনার জেমিনি সহকারী। নিচে স্পষ্ট অডিও প্লেয়ার দেওয়া আছে, প্লে বাটনে টাচ করলেই কথা শুনতে পাবেন। বলুন, কীভাবে সাহায্য করতে পারি?"}
    ]

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 18px 22px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        border: 1px solid #e9ecef !important;
    }
    
    .stChatMessage p {
        color: #202124 !important;
        font-size: 16px !important;
        line-height: 1.6;
    }
    
    .stChatInput {
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 85% !important;
        max-width: 800px !important;
        background: #ffffff !important;
        border-radius: 32px !important;
        padding: 6px 16px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
        border: 1px solid #dadce0 !important;
        z-index: 99999 !important;
    }
    
    .block-container {
        padding-top: 20px !important;
        padding-bottom: 140px !important;
        max-width: 850px !important;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("<h3 style='color: #202124; margin-bottom: 0; font-weight: 500;'>✨ Gemini</h3>", unsafe_allow_html=True)
with col2:
    voice_lang = st.selectbox("ভাষা", ["bn", "hi", "en"], label_visibility="collapsed")

ad_url = "https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3"
st.markdown(f"""
    <a href="{ad_url}" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #4285f4, #34a853); color: white; padding: 10px 16px; border-radius: 12px; text-align: center; font-size: 14px; font-weight: 500; margin: 10px 0 20px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            🚀 বিশেষ অফার ও আপডেট দেখতে এখানে ক্লিক করুন! (Sponsored)
        </div>
    </a>
""", unsafe_allow_html=True)

for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant":
                try:
                    tts = gTTS(text=message["content"], lang=voice_lang, slow=False)
                    audio_path = f"voice_audio_{i}.mp3"
                    tts.save(audio_path)
                    st.markdown("<div style='margin-top: 8px; font-size: 13px; color: #1a73e8; font-weight: 600;'>🔊 ভয়েস শুনতে নিচের প্লে বাটনে চাপ দিন:</div>", unsafe_allow_html=True)
                    st.audio(audio_path, format='audio/mp3')
                except Exception as ex:
                    st.info("🔊 (অডিও লোড হচ্ছে...)")

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
                    temperature=0.7,
                    tool_choice="none"
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                
                tts = gTTS(text=reply, lang=voice_lang, slow=False)
                audio_path = f"voice_audio_{len(st.session_state.messages)}.mp3"
                tts.save(audio_path)
                st.markdown("<div style='margin-top: 8px; font-size: 13px; color: #1a73e8; font-weight: 600;'>🔊 ভয়েস শুনতে নিচের প্লে বাটনে চাপ দিন:</div>", unsafe_allow_html=True)
                st.audio(audio_path, format='audio/mp3')

                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

            except Exception as err:
                st.error(f"ত্রুটি ঘটেছে: {err}")
