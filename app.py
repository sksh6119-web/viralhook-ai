import streamlit as st
from groq import Groq
import base64

st.set_page_config(page_title="Echo AI - ভয়েস ও স্ক্রিনশট সহকারী", page_icon="🌐", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key error: " + str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Echo AI, a helpful, wise, and intelligent assistant. CRITICAL RULES: 1. Always reply in the EXACT same language that the user uses (Bengali if Bengali, English if English). 2. If an image or screenshot is uploaded, DO NOT generate new images. Only read, analyze, and explain the text or contents simply in the user's language so common people can understand. If you cannot understand, say 'আমি বুঝতে পারিনি'."},
        {"role": "assistant", "content": "নমস্কার! 🙏 আমি **Echo AI**। আপনার স্ক্রিনশট বা ছবি দিন, আমি সেটি পড়ে বাংলায় বুঝিয়ে দেব।"}
    ]

st.markdown("""
    <head>
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="application-name" content="Echo AI">
        <meta name="theme-color" content="#1a73e8">
    </head>
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f8f9fa; font-family: sans-serif; }
    .stChatMessage { border-radius: 15px !important; padding: 15px !important; margin-bottom: 12px !important; background-color: #ffffff !important; border: 1px solid #e0e0e0 !important; }
    </style>
""", unsafe_allow_html=True)

# প্রিমিয়াম হেডার
st.markdown("<h2 style='text-align: center; color: #1a73e8; margin-bottom: 0px;'>🌐 Echo AI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666666; font-size: 14px; margin-top: 2px;'>আপনার স্মার্ট ভয়েস ও স্ক্রিনশট সহকারী</p>", unsafe_allow_html=True)

# বিজ্ঞাপন ব্যানার
st.markdown("""
    <div style="background: #e8f0fe; border: 1px solid #d2e3fc; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 15px;">
        📢 <a href="https://www.profitableratecpmnetwork.com/h7ssyv17p?key=eb8a14de90b0395f65ebf374d7d4ca71" target="_blank" style="color: #1a73e8; font-weight: bold; text-decoration: none; font-size: 15px;">বিশেষ অফার ও আপডেট দেখতে এখানে ক্লিক করুন! 🚀</a>
    </div>
""", unsafe_allow_html=True)

# চ্যাট হিস্ট্রি রেন্ডার করা
for i, message in enumerate(st.session_state.messages):
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
            
            # অ্যাসিস্ট্যান্টের মেসেজের পাশে আলাদা এবং নিখুঁত ভয়েস প্লে ও স্টপ বাটন
            if message["role"] == "assistant":
                text_to_speak = content if isinstance(content, str) else "বিশ্লেষণ সম্পন্ন হয়েছে।"
                clean_text = text_to_speak.replace('"', '').replace("'", "").replace('\n', ' ')
                
                # Streamlit এর কলাম ব্যবহার করে বাটনগুলো একদম পরিপাটি ও আলাদা রাখা হয়েছে যাতে কোনো ওভারল্যাপ না হয়
                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("▶️ প্লে", key=f"play_{i}"):
                        st.markdown(f"""
                            <script>
                            if ('speechSynthesis' in window) {{
                                window.speechSynthesis.cancel();
                                var u = new SpeechSynthesisUtterance('{clean_text}');
                                u.rate = 0.9;
                                u.lang = 'bn-IN';
                                window.speechSynthesis.speak(u);
                            }}
                            </script>
                        """, unsafe_allow_html=True)
                with col2:
                    if st.button("⏹️ স্টপ", key=f"stop_{i}"):
                        st.markdown("""
                            <script>
                            if ('speechSynthesis' in window) {
                                window.speechSynthesis.cancel();
                            }
                            </script>
                        """, unsafe_allow_html=True)

# ফাইল আপলোড এবং ইনপুট অংশ
uploaded_file = st.file_uploader("📷 স্ক্রিনশট বা ছবি আপলোড করুন:", type=["jpg", "jpeg", "png"], key="echo_ai_uploader")
prompt = st.chat_input("Echo AI কে কিছু জিগ্যেস করুন...")

if prompt or uploaded_file:
    user_content = []
    
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        image_url = "data:" + uploaded_file.type + ";base64," + base64_image
        user_content.append({"type": "image_url", "image_url": {"url": image_url}})
    
    if prompt:
        user_content.append({"type": "text", "text": prompt})
    else:
        user_content.append({"type": "text", "text": "এই স্ক্রিনশট বা ছবিটিতে কী লেখা আছে বা কী বোঝানো হয়েছে, তা বাংলায় খুব স্পষ্ট ও সহজ করে বুঝিয়ে দিন।"})

    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="আপলোড করা স্ক্রিনশট", width=280)
        if prompt:
            st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Echo AI বিশ্লেষণ করছে..."):
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
                    reply = "আমি দুঃখিত, ছবিটির লেখা স্পষ্টভাবে পড়তে পারছি না।"
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
            except Exception as err:
                reply = "আমি বুঝতে পারিনি বা প্রযুক্তিগত সমস্যা হয়েছে।"
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
