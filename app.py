import streamlit as st
from groq import Groq
import json
import base64

st.set_page_config(page_title="সহকারী হাব", page_icon="✨", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, wise, and practical assistant. You know about religion, stories, songs, and viral trends. CRITICAL RULE: Always reply in the EXACT same language that the user uses (if user writes in Bengali, reply strictly in Bengali; if in English, reply in English). If a screenshot or image is provided, read and analyze it simply in the user's language."},
        {"role": "assistant", "content": "নমস্কার! 🙏 আমি আপনার সহকারী। আপনি যে ভাষায় কথা বলবেন বা প্রশ্ন করবেন, আমি ঠিক সেই ভাষাতেই আপনাকে উত্তর দেব। নিচে স্ক্রিনশট বা ছবি আপলোড করার ব্যবস্থাও আছে। বলুন, আজ আপনাকে কীভাবে সাহায্য করতে পারি?"}
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

st.markdown("<h3 style='text-align: center; color: #1a73e8;'>✨ জ্ঞান, স্ক্রিনশট ও ভয়েস সহকারী</h3>", unsafe_allow_html=True)

# গ্যালারি বা ক্যামেরা থেকে স্ক্রিনশট আপলোড করার অপশন
uploaded_file = st.file_uploader("📷 স্ক্রিনশট বা ছবি আপলোড করুন (গ্যালারি/ক্যামেরা):", type=["jpg", "jpeg", "png"])

for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            if isinstance(message["content"], list):
                for part in message["content"]:
                    if part.get("type") == "text":
                        st.markdown(part.get("text"))
                    elif part.get("type") == "image_url":
                        st.image(part.get("image_url").get("url"), caption="আপলোড করা স্ক্রিনশট", width=250)
            else:
                st.markdown(message["content"])
            
            if message["role"] == "assistant":
                text_to_read = message["content"] if isinstance(message["content"], str) else "বিশ্লেষণ সম্পন্ন হয়েছে।"
                safe_text = json.dumps(text_to_read)
                
                # ভয়েস প্লেব্যাক স্ক্রিপ্ট
                voice_html = f"""
                <div style="margin-top: 10px;">
                    <button id="v_btn_{i}" onclick="playVoice_{i}()" style="background: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; padding: 8px 16px; border-radius: 20px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 5px;">
                        🔊 ভয়েস শুনুন / Listen
                    </button>
                </div>
                
                <script>
                function playVoice_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('Voice not supported.');
                        return;
                    }}
                    
                    window.speechSynthesis.cancel();
                    
                    var text = {safe_text};
                    var utterance = new SpeechSynthesisUtterance(text);
                    utterance.rate = 0.90;
                    
                    var btn = document.getElementById('v_btn_{i}');
                    
                    utterance.onstart = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 বলছি / Speaking..."; 
                            btn.style.background = "#fce8e6"; 
                            btn.style.color = "#c5221f"; 
                        }}
                    }};
                    
                    utterance.onend = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 ভয়েস শুনুন / Listen"; 
                            btn.style.background = "#e8f0fe"; 
                            btn.style.color = "#1a73e8"; 
                        }}
                    }};
                    
                    utterance.onerror = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 ভয়েস শুনুন / Listen"; 
                            btn.style.background = "#e8f0fe"; 
                            btn.style.color = "#1a73e8"; 
                        }}
                    }};
                    
                    window.speechSynthesis.speak(utterance);
                }}
                </script>
                """
                st.markdown(voice_html, unsafe_allow_html=True)

prompt = st.chat_input("কিছু লিখুন বা প্রশ্ন করুন... / Ask anything...")

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
        user_content.append({"type": "text", "text": "এই স্ক্রিনশট বা ছবিটিতে কী আছে তা বাংলায় সহজ করে বুঝিয়ে দিন যাতে সবাই বুঝতে পারে। (Explain this image simply in Bengali)"})

    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="আপলোড করা স্ক্রিনশট", width=250)
        if prompt:
            st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("উত্তর তৈরি হচ্ছে... / Processing..."):
            try:
                # ছবি থাকলে ভিশন মডেল এবং সাধারণ লেখার জন্য জিপিটি মডেল ব্যবহার করা হবে
                model_to_use = "meta-llama/llama-3.2-11b-vision-preview" if uploaded_file is not None else "openai/gpt-oss-20b"
                
                res = client.chat.completions.create(
                    model=model_to_use,
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
                        messages=[{"role": m["role"], "content": "Please reply in the user's language." if isinstance(m["content"], list) else m["content"]} for m in st.session_state.messages],
                        temperature=0.7
                    )
                    reply = res_fallback.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except Exception as e2:
                    st.error(f"Error: {e2}")
