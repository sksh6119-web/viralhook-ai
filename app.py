import streamlit as st
from groq import Groq
import json

st.set_page_config(page_title="Global AI & Voice Hub", page_icon="🌍", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a highly intelligent, multilingual, and wise assistant. You know about religion (Quran, Gita), stories, songs, and viral trends. Always reply in the exact same language that the user uses to ask the question (e.g., if asked in English, reply in English; if in Bengali, reply in Bengali; if in Hindi, reply in Hindi). Keep the response clear, accurate, and helpful."},
        {"role": "assistant", "content": "নমস্কার / Hello! 🙏 আমি আপনার সার্বজনীন সহকারী। আপনি যেকোনো ভাষায় (বাংলা, ইংরেজি, হিন্দি ইত্যাদি) আমার সাথে কথা বলতে পারেন বা প্রশ্ন করতে পারেন। আমি ঠিক সেই ভাষাতেই আপনাকে উত্তর দেব এবং ভয়েস বাটনে ক্লিক করলে সেটি উচ্চারণ করে শোনাব। বলুন, আজ কীভাবে সাহায্য করতে পারি?"}
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
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #1a73e8;'>🌍 গ্লোবাল এআই ও ভয়েস হাব</h3>", unsafe_allow_html=True)

for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant":
                safe_text = json.dumps(message["content"])
                
                # ইউনিভার্সাল ভয়েস স্ক্রিপ্ট যা লেখার ভাষা অনুযায়ী স্বয়ংক্রিয়ভাবে মানিয়ে নেবে
                voice_html = f"""
                <div style="margin-top: 10px;">
                    <button id="v_btn_{i}" onclick="playVoice_{i}()" style="background: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; padding: 8px 16px; border-radius: 20px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 5px;">
                        🔊 Listen Voice / ভয়েস শুনুন
                    </button>
                </div>
                
                <script>
                function playVoice_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('Your browser does not support voice speech.');
                        return;
                    }}
                    
                    window.speechSynthesis.cancel();
                    
                    var text = {safe_text};
                    var utterance = new SpeechSynthesisUtterance(text);
                    utterance.rate = 0.90;
                    
                    var btn = document.getElementById('v_btn_{i}');
                    
                    utterance.onstart = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 Speaking..."; 
                            btn.style.background = "#fce8e6"; 
                            btn.style.color = "#c5221f"; 
                        }}
                    }};
                    
                    utterance.onend = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 Listen Voice / ভয়েস শুনুন"; 
                            btn.style.background = "#e8f0fe"; 
                            btn.style.color = "#1a73e8"; 
                        }}
                    }};
                    
                    utterance.onerror = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 Listen Voice / ভয়েস শুনুন"; 
                            btn.style.background = "#e8f0fe"; 
                            btn.style.color = "#1a73e8"; 
                        }}
                    }};
                    
                    window.speechSynthesis.speak(utterance);
                }}
                </script>
                """
                st.markdown(voice_html, unsafe_allow_html=True)

if prompt := st.chat_input("Ask anything in any language... / যেকোনো ভাষায় কিছু লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generating response... / উত্তর তৈরি হচ্ছে..."):
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
                st.error(f"Error: {err}")
