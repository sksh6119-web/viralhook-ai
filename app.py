import streamlit as st
from groq import Groq
import base64

st.set_page_config(page_title="স্ক্রিনশট রিডার ও ভয়েস হাব", page_icon="🎙️", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a direct, honest, and practical assistant. Rules: 1. Always reply in clear, simple Bengali. 2. If you don't understand something or cannot process an image, clearly state 'আমি বুঝতে পারিনি' (I couldn't understand). 3. If an image or screenshot is uploaded, DO NOT generate new images. Only read and explain the text or contents of the image in plain Bengali."},
        {"role": "assistant", "content": "নমস্কার! 🙏 আমি আপনার সহকারী। আপনি স্ক্রিনশট বা ছবি দিন, আমি সাথে সাথে সেটির অর্থ বাংলায় বুঝিয়ে দিচ্ছি।"}
    ]

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f8f9fa; font-family: sans-serif; }
    .stChatMessage { border-radius: 15px !important; padding: 15px !important; margin-bottom: 12px !important; background-color: #ffffff !important; border: 1px solid #e0e0e0 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #1a73e8;'>🎙️ স্ক্রিনশট রিডার ও ভয়েস হাব</h3>", unsafe_allow_html=True)

# চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            content = message["content"]
            if isinstance(content, list):
                for part in content:
                    if part.get("type") == "text":
                        st.markdown(part.get("text"))
                    elif part.get("type") == "image_url":
                        st.image(part.get("image_url").get("url"), caption="আপলোড করা স্ক্রিনশট", width=280)
            else:
                st.markdown(content)
            
            # ভয়েস প্লে ও স্টপ বাটন
            if message["role"] == "assistant":
                text_to_speak = content if isinstance(content, str) else "বিশ্লেষণ সম্পন্ন হয়েছে।"
                safe_js_text = text_to_speak.replace('"', '\\"').replace('\n', ' ').replace("'", "\\'")
                
                voice_html = f"""
                <div style="margin-top: 10px; display: flex; gap: 8px; align-items: center;">
                    <button onclick="
                        if ('speechSynthesis' in window) {{
                            window.speechSynthesis.cancel();
                            var u = new SpeechSynthesisUtterance('{safe_js_text}');
                            u.rate = 0.9;
                            u.lang = 'bn-IN';
                            window.speechSynthesis.speak(u);
                        }}
                    " style="background: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; padding: 6px 14px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 13px;">
                        🔊 ভয়েস শুনুন
                    </button>
                    <button onclick="
                        if ('speechSynthesis' in window) {{
                            window.speechSynthesis.cancel();
                        }}
                    " style="background: #fce8e6; color: #c5221f; border: 1px solid #fadcda; padding: 6px 12px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 13px;">
                        ⏹️ বন্ধ করুন
                    </button>
                </div>
                
                <script>
                (function() {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        var u = new SpeechSynthesisUtterance('{safe_js_text}');
                        u.rate = 0.9;
                        u.lang = 'bn-IN';
                        setTimeout(function() {{
                            window.speechSynthesis.speak(u);
                        }, 300);
                    }}
                }})();
                </script>
                """
                st.markdown(voice_html, unsafe_allow_html=True)

# ফাইল আপলোড এবং ইনপুট
uploaded_file = st.file_uploader("📷 স্ক্রিনশট বা ছবি আপলোড করুন:", type=["jpg", "jpeg", "png"], key="clean_img_uploader")
prompt = st.chat_input("কিছু লিখুন বা প্রশ্ন করুন...")

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
        user_content.append({"type": "text", "text": "এই স্ক্রিনশট বা ছবিটিতে কী লেখা আছে বা কী বোঝানো হয়েছে, তা বাংলায় খুব স্পষ্ট করে বুঝিয়ে দিন। যদি বুঝতে না পারেন তবে বলুন যে বুঝতে পারেননি।"})

    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="আপলোড করা স্ক্রিনশট", width=280)
        if prompt:
            st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("বিশ্লেষণ করা হচ্ছে..."):
            try:
                model_to_use = "meta-llama/llama-3.2-11b-vision-preview" if uploaded_file is not None else "openai/gpt-oss-20b"
                
                res = client.chat.completions.create(
                    model=model_to_use,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.5,
                    max_tokens=1024
                )
                reply = res.choices[0].message.content
                
                if not reply or reply.strip().lower() in ["sure.", "sure", "ok", "okay"]:
                    reply = "আমি দুঃখিত, ছবিটির লেখা বা বিষয়বস্তু স্পষ্টভাবে পড়তে পারছি না। দয়া করে পরিষ্কার স্ক্রিনশট দিন।"
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
            except Exception as err:
                reply = f"আমি বুঝতে পারিনি বা প্রযুক্তিগত সমস্যার কারণে প্রক্রিয়াটি সম্পন্ন হয়নি।"
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
