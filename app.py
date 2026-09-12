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
        {"role": "system", "content": "You are a supremely knowledgeable, wise, and incredibly friendly AI companion. You have access to all information in the universe and can answer any question accurately and instantly. Always use extremely polite, decent, respectful, and sweet language in Bengali. Never use any harsh, inappropriate, or bad words. When greeted like 'Hi' or 'Hello', warmly and affectionately ask how the user is doing, what's up, and offer a friendly chat just like a caring best friend."}
    ]

# ডিসপ্লে ফিক্স এবং প্রিমিয়াম লুকের জন্য CSS (কোনো ছোট বক্স বা স্করলিং ঝামেলা ছাড়াই সরাসরি সাবলীল লেখা)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f0f4f9;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* চ্যাট মেসেজ বক্সের ব্যাকগ্রাউন্ড ও মার্জিন নিখুঁত করা যাতে কোনো লেখা কেটে না যায় */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 24px !important;
        padding: 20px 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        border: 1px solid #e1e6ed !important;
    }
    
    .stChatMessage p {
        color: #1f1f1f !important;
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    
    /* ভাসমান চ্যাট ইনপুট বক্স */
    .stChatInput {
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 90% !important;
        max-width: 850px !important;
        background: #ffffff !important;
        border-radius: 36px !important;
        padding: 10px 22px !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12) !important;
        border: 1px solid #dcdfe5 !important;
        z-index: 99999 !important;
    }
    
    .block-container {
        padding-top: 25px !important;
        padding-bottom: 160px !important;
        max-width: 900px !important;
    }
    </style>
""", unsafe_allow_html=True)

# হেডার ও ভয়েস সিলেক্টর
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("<h3 style='color: #1f1f1f; margin-bottom: 0; font-weight: 600;'>✨ Gemini AI</h3>", unsafe_allow_html=True)
with col2:
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

# আপনার অ্যাডস্টার্নার Smartlink ব্যানার
ad_url = "https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3"
st.markdown(f"""
    <a href="{ad_url}" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #1a73e8, #34a853); color: white; padding: 14px 20px; border-radius: 16px; text-align: center; font-size: 16px; font-weight: 600; margin: 10px 0 24px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            🚀 বিশেষ অফার ও আপডেট দেখতে এখানে ক্লিক করুন! (Sponsored)
        </div>
    </a>
""", unsafe_allow_html=True)

# চ্যাট হিস্ট্রি প্রদর্শন এবং এআই উত্তরের নিচে সরাসরি স্পষ্ট ভয়েস প্লে বাটন
for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant":
                safe_text = json.dumps(message["content"])
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                
                # সাউন্ড ও ভয়েস রিডিংয়ের শক্তিশালী জাভাস্ক্রিপ্ট কোড
                voice_button_html = f"""
                <div style="margin-top: 16px; border-top: 1px solid #f1f3f4; padding-top: 12px; display: flex; justify-content: flex-end;">
                    <button id="speaker_btn_{i}" onclick="playVoice_{i}()" style="background: #e8f0fe; border: 1px solid #d2e3fc; border-radius: 28px; padding: 10px 22px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 600; color: #1a73e8;">
                        🔊 ভয়েস শুনুন
                    </button>
                </div>
                
                <script>
                function playVoice_{i}() {{
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
