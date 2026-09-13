import streamlit as st
from groq import Groq
import base64
from gtts import gTTS
import os

st.set_page_config(page_title="Echo AI - আপনার ভয়েস ও স্ক্রিনশট সহকারী", page_icon="🌐", layout="centered")

# সাউন্ড অন/অফ করার গ্লোবাল কন্ট্রোল (Sidebar-এ সুইচ)
st.sidebar.title("⚙️ সেটিংস")
sound_enabled = st.sidebar.toggle("🔊 ভয়েস আউটপুট (Sound)", value=True)

# অটোমেটিক ক্লিয়ার এবং স্ট্যান্ডার্ড বাংলা ভয়েস জেনারেট করার ফাংশন
def play_auto_voice(text, unique_id):
    if not sound_enabled:
        return
    try:
        clean_text = str(text).replace('"', '').replace("'", "").replace('\n', ' ')
        if len(clean_text.strip() > 0):
            tts = gTTS(text=clean_text, lang='bn', slow=False)
            audio_file = f"voice_{unique_id}.mp3"
            tts.save(audio_file)
            st.audio(audio_file, format="audio/mp3", autoplay=True)
    except Exception as e:
        pass

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key error: " + str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Echo AI, a helpful, wise, and intelligent assistant. CRITICAL RULES: 1. Always reply in Bengali language. 2. When the user provides an image or screenshot, thoroughly analyze it, read any text present in it, and explain its contents clearly in Bengali."},
        {"role": "assistant", "content": "নমস্কার! 🙏 আমি Echo AI। আপনার স্ক্রিনশট বা ছবি দিন, আমি সেটি পড়ে বাংলায় বুঝিয়ে দেব।"}
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
    .stApp {background-color: #f8f9fa; font-family: sans-serif;}
    .stChatMessage { border-radius: 15px !important; padding: 15px !important; margin-bottom: 12px !important; background-color: white !important; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# প্রিমিয়াম হেডার
st.markdown("<h2 style='text-align: center; color: #1a73e8; margin-bottom: 0px;'>🌐 Echo AI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666666; font-size: 14px; margin-top: 2px;'>আপনার স্মার্ট ভয়েস ও স্ক্রিনশট সহকারী</p>", unsafe_allow_html=True)

# প্রমোশন ব্যানার
st.markdown("""
    <div style="background: #e8f0fe; border: 1px solid #d2e3fc; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
        📢 <a href="https://www.profitableratecpmnetwork.com/h7syyv17p?key=ebdal4de90b6395f05ef374d764ca71" target="_blank" style="color: #1a73e8; text-decoration: none; font-weight: bold;">বিশেষ অফার ও আপডেট দেখতে এখানে ক্লিক করুন!</a> 🚀
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
                        text_val = part.get("text")
                        st.markdown(text_val)
                    elif part.get("type") == "image_url":
                        st.image(part.get("image_url").get("url"), caption="আপলোড করা স্ক্রিনশট", width=200)
            else:
                st.markdown(content)

# ফাইল আপলোড এবং ইনপুট অংশ
uploaded_file = st.file_uploader("📸 স্ক্রিনশট বা ছবি আপলোড করুন:", type=["jpg", "jpeg", "png"], key="echo_ai_uploader")
prompt = st.chat_input("Echo AI কে কিছু জিগ্যেস করুন...")

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
        user_content.append({"type": "text", "text": "এই স্ক্রিনশট বা ছবিটির কী লেখা আছে বা কী বোঝানো হয়েছে, তা বাংলায় খুব স্পষ্ট ও বিস্তারিতভাবে বুঝিয়ে বলুন।"})

    st.session_state.messages.append({"role": "user", "content": user_content})

    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, caption="আপলোড করা স্ক্রিনশট", width=200)
        if prompt:
            st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Echo AI চিন্তা করছে..."):
            try:
                model_to_use = "meta-llama/llama-3.2-11b-vision-preview" if uploaded_file is not None else "openai/gpt-oss-120b"
                
                res = client.chat.completions.create(
                    model=model_to_use,
                    messages=[{"role": n["role"], "content": n["content"]} for n in st.session_state.messages],
                    temperature=0.5,
                    max_tokens=1024
                )
                
                reply = res.choices[0].message.content
                
                if not reply or reply.strip().lower() in ["sure.", "sure", "ok", "okay"]:
                    reply = "আমি দুঃখিত, অতিরিক্ত লেখা পড়তে পারিনি বা বুঝতে পারিনি।"
                
                st.markdown(reply)
                
                # অটোমেটিক ভয়েস প্লে এবং সাউন্ড অন/অফ কন্ট্রোল
                play_auto_voice(reply, unique_id=len(st.session_state.messages))
                
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
            except Exception as e:
                reply = "আমি বুঝতে পারিনি বা প্রযুক্তিগত সমস্যা হয়েছে।"
                st.markdown(reply)
                play_auto_voice(reply, unique_id="error")
                st.session_state.messages.append({"role": "assistant", "content": reply})
