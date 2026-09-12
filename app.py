import streamlit as st
from groq import Groq
import json

st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

# ইউনিভার্সাল ভাষা ডিটেকশন সিস্টেম (যেই ভাষা, সেই ভাষায় উত্তর)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Gemini, an advanced and friendly AI assistant. Detect the language of the user's input automatically and always reply fluently in that exact same language (Bengali, Hindi, English, Spanish, etc.). Be polite, accurate, and helpful."},
        {"role": "assistant", "content": "নমস্কার! 😊 আমি আপনার জেমিনি সহকারী। আপনি বাংলা, হিন্দি, ইংরেজি বা যেকোনো ভাষায় কথা বলতে পারেন—আমি সেই ভাষাতেই উত্তর দেব এবং যারা পড়তে পারেন না, তারা নিচের '🔊 ভয়েস শুনুন' বাটনে ক্লিক করলেই শুনতে পাবেন। বলুন, কীভাবে সাহায্য করতে পারি?"}
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
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

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
                safe_text = json.dumps(message["content"])
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                
                voice_toolbar_html = f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; border-top: 1px solid #f1f3f4; padding-top: 10px;">
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <span title="লাইক" style="cursor: pointer; font-size: 16px;" onclick="alert('ধন্যবাদ!')">👍</span>
                        <span title="ডিসলাইক" style="cursor: pointer; font-size: 16px;" onclick="alert('ধন্যবাদ!')">👎</span>
                        <span title="পুনরায় লিখুন" style="cursor: pointer; font-size: 16px;" onclick="location.reload();">🔄</span>
                        <span title="কপি করুন" style="cursor: pointer; font-size: 16px;" onclick="navigator.clipboard.writeText({safe_text}); alert('টেক্সট কপি করা হয়েছে!');">📋</span>
                    </div>
                    
                    <div>
                        <button id="speaker_btn_{i}" onclick="playAudio_{i}()" style="background: #e8f0fe; border: 1px solid #d2e3fc; border-radius: 20px; padding: 6px 14px; cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 500; color: #1a73e8;">
                            🔊 ভয়েস শুনুন
                        </button>
                    </div>
                </div>
                
                <script>
                function playAudio_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('আপনার ব্রাউজার ভয়েস সাপোর্ট করে না।');
                        return;
                    }}
                    window.speechSynthesis.cancel();
                    var textToRead = {safe_text};
                    var speech = new SpeechSynthesisUtterance(textToRead);
                    speech.lang = 'bn-IN';
                    speech.rate = 0.95;
                    var voices = window.speechSynthesis.getVoices();
                    for(var k = 0; k < voices.length; k++) {{
                        if(voices[k].name.toLowerCase().includes('{selected_voice_filter}') || voices[k].lang.includes('bn')) {{
                            speech.voice = voices[k];
                            break;
                        }}
                    }}
                    var btnElem = document.getElementById('speaker_btn_{i}');
                    speech.onstart = function() {{
                        btnElem.style.background = '#fce8e6';
                        btnElem.style.color = '#c5221f';
                        btnElem.innerHTML = '🔊 বলছি...';
                    }};
                    speech.onend = function() {{
                        btnElem.style.background = '#e8f0fe';
                        btnElem.style.color = '#1a73e8';
                        btnElem.innerHTML = '🔊 ভয়েস শুনুন';
                    }};
                    speech.onerror = function() {{
                        btnElem.style.background = '#e8f0fe';
                        btnElem.style.color = '#1a73e8';
                        btnElem.innerHTML = '🔊 ভয়েস শুনুন';
                    }};
                    window.speechSynthesis.speak(speech);
                }}
                </script>
                """
                st.markdown(voice_toolbar_html, unsafe_allow_html=True)

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
