import streamlit as st
from groq import Groq
import json

st.set_page_config(page_title="জ্ঞান, ভাইরাল নিউজ ও ভয়েস হাব", page_icon="✨", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a highly intelligent, wise, and practical assistant. You have deep knowledge of holy scriptures like the Quran, Bhagavad Gita, and philosophical texts, storytelling, poetry, and song writing. Additionally, you are an expert in current viral news trends, social media strategies (Facebook, YouTube, Instagram), and practical common sense. Always provide accurate, peaceful, respectful, logical, and fluent responses in the user's language (Bengali). Keep the tone helpful, moral, and highly engaging."},
        {"role": "assistant", "content": "নমস্কার ও আসসালামু আলাইকুম! 🙏 আমি আপনার জ্ঞান, ভাইরাল নিউজ ও সাধারণ বুদ্ধিমত্তার সহকারী। পবিত্র ধর্মগ্রন্থ, নৈতিক গল্প, গান-কবিতা লেখার পাশাপাশি ফেসবুক ও ইউটিউবের বর্তমান ভাইরাল খবর এবং যেকোনো বিষয়ে বাস্তবসম্মত সাধারণ বুদ্ধি বা সঠিক পরামর্শ দিতে আমি প্রস্তুত। বলুন, আজ আপনাকে কীভাবে সাহায্য করতে পারি?"}
    ]

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #fcfcfc;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 18px 22px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        border: 1px solid #eaeaea !important;
    }
    
    .stChatMessage p {
        color: #2c3e50 !important;
        font-size: 16px !important;
        line-height: 1.7;
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
        border: 1px solid #dcdcdc !important;
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
    st.markdown("<h3 style='color: #1a202c; margin-bottom: 0; font-weight: 600;'>✨ জ্ঞান, ভাইরাল নিউজ ও ভয়েস হাব</h3>", unsafe_allow_html=True)
with col2:
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

ad_url = "https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3"
st.markdown(f"""
    <a href="{ad_url}" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #2b6cb0, #2f855a); color: white; padding: 10px 16px; border-radius: 12px; text-align: center; font-size: 14px; font-weight: 500; margin: 10px 0 15px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            ✨ বিশেষ আপডেট ও অফার দেখতে এখানে ক্লিক করুন! (Sponsored)
        </div>
    </a>
""", unsafe_allow_html=True)

for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant":
                safe_text = json.dumps(message["content"])
                selected_gender = "female" if voice_gender == "Female" else "male"
                
                # উন্নত এবং শক্তিশালী ভয়েস স্ক্রিপ্ট যা মোবাইলের ব্রাউজারে নিশ্চিতভাবে কাজ করবে
                voice_html = f"""
                <div style="display: flex; justify-content: flex-start; margin-top: 12px; padding-top: 8px;">
                    <button id="voice_btn_{i}" onclick="runVoice_{i}()" style="background: #edf2f7; border: 1px solid #cbd5e0; border-radius: 20px; padding: 6px 16px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 600; color: #2b6cb0;">
                        🔊 ভয়েস শুনুন
                    </button>
                </div>
                
                <script>
                function runVoice_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('আপনার ব্রাউজার ভয়েস সাপোর্ট করে না।');
                        return;
                    }}
                    
                    window.speechSynthesis.cancel();
                    
                    var textToRead = {safe_text};
                    var utterance = new SpeechSynthesisUtterance(textToRead);
                    utterance.lang = 'bn-IN';
                    utterance.rate = 0.90;
                    
                    function speakNow() {{
                        var voices = window.speechSynthesis.getVoices();
                        var selectedVoice = null;
                        
                        // সঠিক বাংলা বা জেন্ডার ভয়েস খোঁজা
                        for(var k = 0; k < voices.length; k++) {{
                            var vName = voices[k].name.toLowerCase();
                            var vLang = voices[k].lang.toLowerCase();
                            if (vLang.includes('bn') || vLang.includes('bangla')) {{
                                if (vName.includes('{selected_gender}')) {{
                                    selectedVoice = voices[k];
                                    break;
                                }} else if (!selectedVoice) {{
                                    selectedVoice = voices[k];
                                }}
                            }}
                        }}
                        
                        if (selectedVoice) {{
                            utterance.voice = selectedVoice;
                        }}
                        
                        var btnElem = document.getElementById('voice_btn_{i}');
                        
                        utterance.onstart = function() {{
                            if(btnElem) {{
                                btnElem.style.background = '#fed7d7';
                                btnElem.style.color = '#c53030';
                                btnElem.innerHTML = '🔊 বলছি...';
                            }}
                        }};
                        
                        utterance.onend = function() {{
                            if(btnElem) {{
                                btnElem.style.background = '#edf2f7';
                                btnElem.style.color = '#2b6cb0';
                                btnElem.innerHTML = '🔊 ভয়েস শুনুন';
                            }}
                        }};
                        
                        utterance.onerror = function() {{
                            if(btnElem) {{
                                btnElem.style.background = '#edf2f7';
                                btnElem.style.color = '#2b6cb0';
                                btnElem.innerHTML = '🔊 ভয়েস শুনুন';
                            }}
                        }};
                        
                        window.speechSynthesis.speak(utterance);
                    }}
                    
                    // ব্রাউজারের ভয়েস লিস্ট লোড হওয়ার জন্য ছোট বিরতি হ্যান্ডেল করা
                    var voices = window.speechSynthesis.getVoices();
                    if (voices.length > 0) {{
                        speakNow();
                    }} else {{
                        window.speechSynthesis.onvoiceschanged = function() {{
                            speakNow();
                        };
                        // ইমিডিয়েট ফলব্যাক যদি ইভেন্ট ফায়ার না করে
                        setTimeout(speakNow, 100);
                    }}
                }}
                </script>
                """
                st.markdown(voice_html, unsafe_allow_html=True)

if prompt := st.chat_input("ভাইরাল খবর, ধর্মগ্রন্থ, গল্প বা সাধারণ বুদ্ধি নিয়ে কিছু জিজ্ঞাসা করুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("তথ্য ও বাস্তবসম্মত বুদ্ধি বিশ্লেষণ করা হচ্ছে..."):
            try:
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.7,
                    tool_choice="none"
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

            except Exception as err:
                st.error(f"ত্রুটি ঘটেছে: {err}")
