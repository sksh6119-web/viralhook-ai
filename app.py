import streamlit as st
from groq import Groq
import json
import base64

st.set_page_config(page_title="জ্ঞান, ভাইরাল নিউজ ও ভয়েস হাব", page_icon="🎙️", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a highly intelligent, wise, and practical assistant. You have deep knowledge of holy scriptures like the Quran, Bhagavad Gita, and philosophical texts, storytelling, poetry, and song writing. Additionally, you are an expert in current viral news trends, social media strategies (Facebook, YouTube, Instagram), and practical common sense. If an image or screenshot is provided, read and analyze the text/content in it carefully and explain it simply in Bengali. Always provide accurate, peaceful, respectful, logical, and fluent responses in the user's language (Bengali)."},
        {"role": "assistant", "content": "নমস্কার ও আসসালামু আলাইকুম! 🙏 আমি আপনার জ্ঞান ও ভয়েস সহকারী। আপনি লেখালেখির পাশাপাশি যেকোনো স্ক্রিনশট বা ছবি আপলোড করতে পারেন—আমি সেটি পড়ে ও বুঝে আপনাকে বাংলায় বুঝিয়ে দেব, আর নিচে ভয়েস বাটনে ক্লিক করলেই সেটি মুখে শুনে নিতে পারবেন। বলুন, আজ কীভাবে সাহায্য করতে পারি?"}
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

# ওপরের শিরোনাম ও ভয়েস সিলেক্ট অপশন
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("<h3 style='color: #1a202c; margin-bottom: 0; font-weight: 600;'>🎙️ জ্ঞান, স্ক্রিনশট রিডার ও ভয়েস হাব</h3>", unsafe_allow_html=True)
with col2:
    voice_gender = st.selectbox("ভয়েস", ["Female", "Male"], label_visibility="collapsed")

# স্পন্সর বা বিজ্ঞাপন লিংক
ad_url = "https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3"
st.markdown(f"""
    <a href="{ad_url}" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #2b6cb0, #2f855a); color: white; padding: 10px 16px; border-radius: 12px; text-align: center; font-size: 14px; font-weight: 500; margin: 10px 0 15px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            ✨ বিশেষ আপডেট ও অফার দেখতে এখানে ক্লিক করুন! (Sponsored)
        </div>
    </a>
""", unsafe_allow_html=True)

# স্ক্রিনশট বা ছবি আপলোড করার অপশন
uploaded_file = st.file_uploader("📥 কোনো স্ক্রিনশট বা ছবি থাকলে এখানে আপলোড করুন...", type=["jpg", "jpeg", "png"])

# বার্তা এবং ভয়েস প্লেয়ার সেকশন
for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            if isinstance(message["content"], list):
                for part in message["content"]:
                    if part.get("type") == "text":
                        st.markdown(part.get("text"))
                    elif part.get("type") == "image_url":
                        st.image("Attached Image", caption="আপলোড করা স্ক্রিনশট")
            else:
                st.markdown(message["content"])
            
            if message["role"] == "assistant":
                text_to_read = message["content"] if isinstance(message["content"], str) else "বিশ্লেষণ সম্পন্ন হয়েছে।"
                safe_text = json.dumps(text_to_read)
                selected_filter = "female" if voice_gender == "Female" else "male"
                
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
                    utterance.rate = 0.92;
                    
                    var voices = window.speechSynthesis.getVoices();
                    for(var k = 0; k < voices.length; k++) {{
                        if(voices[k].name.toLowerCase().includes('{selected_filter}') || voices[k].lang.includes('bn')) {{
                            utterance.voice = voices[k];
                            break;
                        }}
                    }}
                    
                    var btnElem = document.getElementById('voice_btn_{i}');
                    
                    utterance.onstart = function() {{
                        btnElem.style.background = '#fed7d7';
                        btnElem.style.color = '#c53030';
                        btnElem.innerHTML = '🔊 পাঠ করা হচ্ছে...';
                    }};
                    
                    utterance.onend = function() {{
                        btnElem.style.background = '#edf2f7';
                        btnElem.style.color = '#2b6cb0';
                        btnElem.innerHTML = '🔊 ভয়েস শুনুন';
                    }};
                    
                    window.speechSynthesis.speak(utterance);
                }}
                </script>
                """
                st.markdown(voice_html, unsafe_allow_html=True)

# ইনপুট বা ছবি সহ প্রসেসিং
prompt = st.chat_input("কিছু লিখুন অথবা ওপরে স্ক্রিনশট আপলোড করুন...")

if prompt or uploaded_file:
    user_content = []
    
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        image_url = f"data:{uploaded_file.type};base64,{base64_image}"
        user_content.append({"type": "image_url", "image_url": {"url": image_url}})
    
    if prompt:
        user_content.append({"type": "text", "text": prompt})
    else:
        user_content.append({"type": "text", "text": "এই স্ক্রিনশট বা ছবিটিতে কী লেখা আছে এবং এর মূল বিষয়বস্তু কী, তা সহজ বাংলায় বুঝিয়ে বলুন যাতে সবাই বুঝতে পারে।"})

    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="আপলোড করা স্ক্রিনশট", width=300)
        if prompt:
            st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("স্ক্রিনশট ও তথ্য বিশ্লেষণ করা হচ্ছে..."):
            try:
                # দৃষ্টিশক্তি বা ভিশন সমর্থিত মডেল ব্যবহার করা হলো
                res = client.chat.completions.create(
                    model="meta-llama/llama-3.2-11b-vision-preview",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.7,
                    max_tokens=1024
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

            except Exception as err:
                st.error(f"ত্রুটি ঘটেছে: {err}")
