import streamlit as st
from groq import Groq
import json
import base64

st.set_page_config(page_title="Global AI & Voice Hub", page_icon="🌍", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a highly intelligent, multilingual, and wise assistant. You know about religion (Quran, Gita), stories, songs, and viral trends. If an image or screenshot is provided, read and analyze it carefully and explain it simply in the user's language so that common people can easily understand. Always reply in the exact same language that the user uses."},
        {"role": "assistant", "content": "নমস্কার / Hello! 🙏 আমি আপনার সার্বজনীন সহকারী। আপনি যেকোনো ভাষায় কথা বলতে পারেন, অথবা নিচে ক্যামেরা/গ্যালারি থেকে স্ক্রিনশট আপলোড করতে পারেন—আমি সেটি পড়ে বুঝিয়ে দেবো। ভয়েস বাটনে ক্লিক করলেই শুনতে পাবেন।"}
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

# ক্যামেরা বা গ্যালারি থেকে স্ক্রিনশট দেওয়ার অপশন
uploaded_file = st.file_uploader("📷 স্ক্রিনশট বা ছবি আপলোড করুন (ক্যামেরা/গ্যালারি):", type=["jpg", "jpeg", "png"])

for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            if isinstance(message["content"], list):
                for part in message["content"]:
                    if part.get("type") == "text":
                        st.markdown(part.get("text"))
                    elif part.get("type") == "image_url":
                        st.image(part.get("image_url").get("url"), caption="আপলোড করা ছবি", width=250)
            else:
                st.markdown(message["content"])
            
            if message["role"] == "assistant":
                text_to_read = message["content"] if isinstance(message["content"], str) else "বিশ্লেষণ সম্পন্ন হয়েছে।"
                safe_text = json.dumps(text_to_read)
                
                # উন্নত ভয়েস প্লেব্যাক স্ক্রিপ্ট
                voice_html = f"""
                <div style="margin-top: 10px;">
                    <button id="v_btn_{i}" onclick="playVoice_{i}()" style="background: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; padding: 8px 16px; border-radius: 20px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 5px;">
                        🔊 Listen / ভয়েস শুনুন
                    </button>
                </div>
                
                <script>
                function playVoice_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('Speech synthesis not supported.');
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
                            btn.innerText = "🔊 Listen / ভয়েস শুনুন"; 
                            btn.style.background = "#e8f0fe"; 
                            btn.style.color = "#1a73e8"; 
                        }}
                    }};
                    
                    utterance.onerror = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 Listen / ভয়েস শুনুন"; 
                            btn.style.background = "#e8f0fe"; 
                            btn.style.color = "#1a73e8"; 
                        }}
                    }};
                    
                    window.speechSynthesis.speak(utterance);
                }}
                </script>
                """
                st.markdown(voice_html, unsafe_allow_html=True)

prompt = st.chat_input("Ask anything or paste link... / কিছু লিখুন বা প্রশ্ন করুন...")

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
        user_content.append({"type": "text", "text": "Please read and explain this screenshot/image simply so that common people can understand it."})

    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="আপলোড করা ছবি", width=250)
        if prompt:
            st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing... / প্রক্রিয়াধীন..."):
            try:
                # ভিশন মডেল ব্যবহার করা হয়েছে যাতে ছবি বা স্ক্রিনশট পড়তে পারে
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
                try:
                    res_fallback = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[{"role": m["role"], "content": "Please explain the request simply." if isinstance(m["content"], list) else m["content"]} for m in st.session_state.messages],
                        temperature=0.7
                    )
                    reply = res_fallback.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except Exception as e2:
                    st.error(f"Error: {e2}")
