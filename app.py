import streamlit as st
from groq import Groq
import json
import base64

st.set_page_config(page_title="সহকারী হাব", page_icon="🎙️", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, wise, and practical assistant. CRITICAL RULES: 1. Always reply in the EXACT same language that the user uses (if user writes in Bengali, reply strictly in Bengali; if in English, reply in English). 2. If the user uploads a photo or screenshot, do NOT generate new images. Instead, read and analyze the text/content in the uploaded image and explain it simply in the user's language so that common people can easily understand."},
        {"role": "assistant", "content": "নমস্কার! 🙏 আমি আপনার সহকারী। আপনি যে ভাষায় লিখবেন, আমি ঠিক সেই ভাষাতেই উত্তর দেব। আর কোনো স্ক্রিনশট বা ছবি দিলে আমি সেটি পড়ে বুঝিয়ে দেব, এবং নিচে 'ভয়েস শুনুন' বাটনে টিপলেই তা পরিষ্কার শুনতে পাবেন। বলুন, আজ কীভাবে সাহায্য করতে পারি?"}
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

st.markdown("<h3 style='text-align: center; color: #1a73e8;'>🎙️ স্ক্রিনশট রিডার ও ভয়েস হাব</h3>", unsafe_allow_html=True)

# স্ক্রিনশট বা ছবি আপলোড অপশন
uploaded_file = st.file_uploader("📷 স্ক্রিনশট বা ছবি আপলোড করুন:", type=["jpg", "jpeg", "png"])

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
                text_to_read = message["content"] if isinstance(message["content"], str) else "তথ্য বিশ্লেষণ সম্পন্ন হয়েছে।"
                safe_text = json.dumps(text_to_read)
                
                # নিশ্চিত এবং শক্তিশালী ভয়েস প্লেব্যাক স্ক্রিপ্ট
                voice_html = f"""
                <div style="margin-top: 10px;">
                    <button id="v_btn_{i}" onclick="playVoice_{i}()" style="background: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; padding: 10px 20px; border-radius: 25px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 15px;">
                        🔊 ভয়েস শুনুন / Listen
                    </button>
                </div>
                
                <script>
                function playVoice_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('Browser does not support speech synthesis.');
                        return;
                    }}
                    
                    window.speechSynthesis.cancel();
                    
                    var text = {safe_text};
                    var utterance = new SpeechSynthesisUtterance(text);
                    utterance.rate = 0.90;
                    
                    var btn = document.getElementById('v_btn_{i}');
                    
                    utterance.onstart = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 বলছি... / Speaking..."; 
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
                    
                    // ব্রাউজারের ভয়েস সেট করে প্লে করা
                    var voices = window.speechSynthesis.getVoices();
                    for(var k = 0; k < voices.length; k++) {{
                        if(voices[k].lang.includes('bn') || voices[k].lang.includes('hi') || voices[k].lang.includes('en')) {{
                            utterance.voice = voices[k];
                            break;
                        }}
                    }}
                    
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
        user_content.append({"type": "text", "text": "এই ছবি বা স্ক্রিনশটটিতে কী লেখা আছে বা কী দেখা যাচ্ছে, তা বাংলায় খুব সহজ করে বুঝিয়ে বলুন যাতে সবাই বুঝতে পারে। (Explain this image simply in Bengali)"})

    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="আপলোড করা ছবি", width=250)
        if prompt:
            st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("বিশ্লেষণ করা হচ্ছে... / Processing..."):
            try:
                # ছবি থাকলে ভিশন মডেল এবং টেক্সটের জন্য স্ট্যান্ডার্ড মডেল ব্যবহার করা হবে
                model_name = "meta-llama/llama-3.2-11b-vision-preview" if uploaded_file is not None else "openai/gpt-oss-20b"
                
                res = client.chat.completions.create(
                    model=model_name,
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
                        messages=[{"role": m["role"], "content": "Please reply simply in the user's language." if isinstance(m["content"], list) else m["content"]} for m in st.session_state.messages],
                        temperature=0.7
                    )
                    reply = res_fallback.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except Exception as e2:
                    st.error(f"Error: {e2}")
