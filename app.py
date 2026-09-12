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

# প্রিমিয়াম ডিজাইন ও ফ্লোটিং ইনপুট বক্সের জন্য CSS (আইকন ডানপাশে সাজানোর জন্য)
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

# হেডার ও ভয়েস ড্রপডাউন
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("<h3 style='color: #202124; margin-bottom: 0; font-weight: 500;'>✨ Gemini</h3>", unsafe_allow_html=True)
with col2:
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

# আপনার অ্যাডস্টার্নার Smartlink ব্যানার
ad_url = "https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3"
st.markdown(f"""
    <a href="{ad_url}" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #4285f4, #34a853); color: white; padding: 10px 16px; border-radius: 12px; text-align: center; font-size: 14px; font-weight: 500; margin: 10px 0 20px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            🚀 বিশেষ অফার ও আপডেট দেখতে এখানে ক্লিক করুন! (Sponsored)
        </div>
    </a>
""", unsafe_allow_html=True)

# চ্যাট হিস্ট্রি এবং এআই উত্তরের নিচে প্রফেশনাল SVG আইকন বার (ডানপাশে ফিক্সড)
for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant":
                safe_text = json.dumps(message["content"])
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                
                # আসল জেমিনির মতো অপশন বার যেখানে আইকনগুলোতে ক্লিক করলে কাজ হবে
                gemini_toolbar_html = f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; border-top: 1px solid #f1f3f4; padding-top: 10px;">
                    <!-- বাম বা মাঝখানের অপশনগুলো -->
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <button title="লাইক" onclick="this.style.color='#1a73e8'; alert('ফিডব্যাকের জন্য ধন্যবাদ!');" style="background:none; border:none; cursor:pointer; font-size:16px; color:#5f6368;">👍</button>
                        <button title="ডিসলাইক" onclick="this.style.color='#d93025'; alert('মতামত রেকর্ড করা হয়েছে!');" style="background:none; border:none; cursor:pointer; font-size:16px; color:#5f6368;">👎</button>
                        <button title="পুনরায় লিখুন" onclick="location.reload();" style="background:none; border:none; cursor:pointer; font-size:16px; color:#5f6368;">🔄</button>
                        <button title="শেয়ার করুন" onclick="navigator.clipboard.writeText({safe_text}); alert('টেক্সট কপি ও শেয়ারের জন্য প্রস্তুত!');" style="background:none; border:none; cursor:pointer; font-size:16px; color:#5f6368;">📤</button>
                        <button title="কপি করুন" onclick="navigator.clipboard.writeText({safe_text}); alert('টেক্সট কপি করা হয়েছে!');" style="background:none; border:none; cursor:pointer; font-size:16px; color:#5f6368;">📋</button>
                    </div>
                    
                    <!-- একদম ডানপাশের ভয়েস স্পিকার আইকন (ট্যাপ করলে বলবে ও বন্ধ হবে) -->
                    <div>
                        <button id="speaker_btn_{i}" title="ভয়েস শুনুন / বন্ধ করুন" onclick="toggleSpeech_{i}()" style="background: #f1f3f4; border: none; border-radius: 50%; width: 38px; height: 38px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; transition: 0.2s;">
                            🔊
                        </button>
                    </div>
                </div>
                
                <script>
                var isSpeaking_{i} = false;
                function toggleSpeech_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('আপনার ব্রাউজার ভয়েস সাপোর্ট করছে না।');
                        return;
                    }}
                    
                    var btn = document.getElementById('speaker_btn_{i}');
                    
                    if (isSpeaking_{i}) {{
                        window.speechSynthesis.cancel();
                        isSpeaking_{i} = false;
                        btn.style.background = '#f1f3f4';
                        btn.innerHTML = '🔊';
                    }} else {{
                        window.speechSynthesis.cancel();
                        var textToSpeak = {safe_text};
                        var msg = new SpeechSynthesisUtterance(textToSpeak);
                        msg.lang = 'bn-IN';
                        msg.rate = 1.0;
                        
                        var voices = window.speechSynthesis.getVoices();
                        for(var v = 0; v < voices.length; v++) {{
                            if(voices[v].name.toLowerCase().includes('{selected_voice_filter}') || voices[v].lang.includes('bn')) {{
                                msg.voice = voices[v];
                                break;
                            }}
                        }}
                        
                        msg.onend = function() {{
                            isSpeaking_{i} = false;
                            btn.style.background = '#f1f3f4';
                            btn.innerHTML = '🔊';
                        }};
                        
                        isSpeaking_{i} = true;
                        btn.style.background = '#e8f0fe';
                        btn.innerHTML = '🔇';
                        window.speechSynthesis.speak(msg);
                    }}
                }}
                </script>
                """
                st.markdown(gemini_toolbar_html, unsafe_allow_html=True)

# ইউজার ইনপুট
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
                st.rerun()

            except Exception as err:
                st.error(f"ত্রুটি ঘটেছে: {err}")
