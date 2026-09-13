import streamlit as st
from groq import Groq
import json
import base64

st.set_page_config(page_title="স্ক্রিনশট রিডার ও ভয়েস সহকারী", page_icon="🎙️", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful and practical assistant. CRITICAL RULES: 1. Always reply in the EXACT same language that the user uses (Bengali if Bengali, English if English). 2. If the user uploads an image or screenshot, DO NOT generate or create any new images. Only read, analyze, and explain the uploaded image text/content simply in the user's language so common people can understand."},
        {"role": "assistant", "content": "নমস্কার! 🙏 আমি আপনার সহকারী। আপনি যে ভাষায় লিখবেন বা প্রশ্ন করবেন, আমি ঠিক সেই ভাষাতেই উত্তর দেব। কোনো স্ক্রিনশট বা ছবি দিলে আমি সেটি শুধু পড়ে বুঝিয়ে দেব, এবং সাথে সাথে ভয়েস বেজে উঠবে। ভয়েস বন্ধ করতে চাইলে 'স্টপ' বাটনে ক্লিক করতে পারবেন।"}
    ]

st.markdown("""
    <head>
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="application-name" content="স্ক্রিনশট রিডার হাব">
        <meta name="theme-color" content="#1a73e8">
    </head>
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

st.markdown("<h3 style='text-align: center; color: #1a73e8;'>🎙️ স্ক্রিনশট রিডার ও ভয়েস সহকারী</h3>", unsafe_allow_html=True)

st.markdown("""
    <div style="background: #e8f0fe; border: 1px solid #d2e3fc; padding: 10px 14px; border-radius: 10px; font-size: 13px; color: #174ea6; margin-bottom: 15px; text-align: center;">
        📱 <b>অ্যাপ ইনস্টল:</b> হোম স্ক্রিনে রাখতে ক্রোম ব্রাউজারের তিন ডটে (⋮) ক্লিক করে <b>"Add to Home screen"</b> বা <b>"Install app"</b> করুন!
    </div>
""", unsafe_allow_html=True)

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
                
                # অটো-ভয়েস প্লে এবং স্টপ বাটন সহ স্ক্রিপ্ট
                voice_html = f"""
                <div style="margin-top: 10px; display: flex; gap: 10px;">
                    <button id="v_btn_{i}" onclick="playVoice_{i}()" style="background: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; padding: 8px 16px; border-radius: 20px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; font-size: 14px;">
                        🔊 ভয়েস শুনুন
                    </button>
                    <button onclick="stopVoice_{i}()" style="background: #fce8e6; color: #c5221f; border: 1px solid #fadcda; padding: 8px 14px; border-radius: 20px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; font-size: 14px;">
                        ⏹️ বন্ধ করুন (Stop)
                    </button>
                </div>
                
                <script>
                var utterance_{i} = null;
                
                function playVoice_{i}() {{
                    if (!('speechSynthesis' in window)) {{
                        alert('Speech synthesis not supported.');
                        return;
                    }}
                    
                    window.speechSynthesis.cancel();
                    
                    var text = {safe_text};
                    utterance_{i} = new SpeechSynthesisUtterance(text);
                    utterance_{i}.rate = 0.90;
                    
                    var btn = document.getElementById('v_btn_{i}');
                    
                    utterance_{i}.onstart = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 বলছি..."; 
                            btn.style.background = "#fce8e6"; 
                            btn.style.color = "#c5221f"; 
                        }}
                    }};
                    
                    utterance_{i}.onend = function() {{
                        if(btn) {{ 
                            btn.innerText = "🔊 ভয়েস শুনুন"; 
                            btn.style.background = "#e8f0fe"; 
                            btn.style.color = "#1a73e8"; 
                        }}
                    }};
                    
                    var voices = window.speechSynthesis.getVoices();
                    for(var k = 0; k < voices.length; k++) {{
                        if(voices[k].lang.includes('bn') || voices[k].lang.includes('hi') || voices[k].lang.includes('en')) {{
                            utterance_{i}.voice = voices[k];
                            break;
                        }}
                    }}
                    
                    window.speechSynthesis.speak(utterance_{i});
                }}
                
                function stopVoice_{i}() {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        var btn = document.getElementById('v_btn_{i}');
                        if(btn) {{ 
                            btn.innerText = "🔊 ভয়েস শুনুন"; 
                            btn.style.background = "#e8f0fe"; 
                            btn.style.color = "#1a73e8"; 
                        }}
                    }}
                }}
                
                // উত্তর আসার সাথে সাথে স্বয়ংক্রিয়ভাবে ভয়েস চালু হওয়া
                setTimeout(function() {{
                    playVoice_{i}();
                }}, 500);
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
        user_content.append({"type": "text", "text": "এই ছবি বা স্ক্রিনশটটিতে কী লেখা আছে তা বাংলায় খুব সহজ করে বুঝিয়ে দিন যাতে সবাই বুঝতে পারে। (Explain this image simply in Bengali without generating new images)"})

    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="আপলোড করা ছবি", width=250)
        if prompt:
            st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("বিশ্লেষণ করা হচ্ছে..."):
            try:
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
