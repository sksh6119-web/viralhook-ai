import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="Gemini Flash", layout="centered", initial_sidebar_state="collapsed")

# বড় টেক্সট ও ফুলস্ক্রিন ক্লিন মোবাইল ইন্টারফেস
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 7rem !important;
        max-width: 100% !important;
    }
    header, footer { visibility: hidden !important; }

    /* টপ বার */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0 15px 0;
    }
    .model-name {
        font-size: 1.35rem;
        font-weight: 600;
        color: #1f1f1f;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .dot {
        width: 8px;
        height: 8px;
        background-color: #1a73e8;
        border-radius: 50%;
        display: inline-block;
    }
    .play-circle {
        background-color: #a8c7fa;
        color: #041e49;
        width: 46px;
        height: 46px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        margin-left: auto;
    }

    /* বড় ফন্টের ইউজার মেসেজ বাবল */
    .user-box {
        display: flex;
        justify-content: flex-end;
        margin: 20px 0;
    }
    .user-bubble {
        background-color: #f0f4f9;
        color: #1f1f1f;
        padding: 16px 22px;
        border-radius: 26px;
        max-width: 88%;
        font-size: 1.25rem;
        line-height: 1.5;
        font-weight: 500;
    }

    /* বড় ফন্টের এআই উত্তর বাবল */
    .bot-box {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        margin: 20px 0;
    }
    .bot-icon {
        font-size: 1.5rem;
        color: #1f1f1f;
        margin-top: 2px;
    }
    .bot-msg {
        font-size: 1.25rem;
        line-height: 1.6;
        color: #1f1f1f;
        flex: 1;
        font-weight: 450;
    }

    /* নিচে জেমিনাই স্টাইল সার্চ বার */
    div[data-testid="stChatInput"] {
        border-radius: 35px !important;
        background-color: #f0f4f9 !important;
        border: 1px solid #e0e3e7 !important;
        padding: 6px 14px !important;
    }
    div[data-testid="stChatInput"] textarea {
        font-size: 1.15rem !important;
        color: #1f1f1f !important;
    }
</style>
""", unsafe_allow_html=True)

# হেডার
h1, h2, h3 = st.columns([1, 6, 2])
with h1:
    st.markdown('<span style="font-size: 1.5rem; cursor:pointer;">☰</span>', unsafe_allow_html=True)
with h2:
    st.markdown('<div class="model-name">Gemini Flash <span class="dot"></span></div>', unsafe_allow_html=True)
with h3:
    st.markdown('<div class="play-circle">▶</div>', unsafe_allow_html=True)

# চ্যাট হিস্ট্রি
if "history" not in st.session_state:
    st.session_state.history = []

# মেসেজ ও ভয়েস প্রদর্শন
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f'<div class="user-box"><div class="user-bubble">{chat["text"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-box"><div class="bot-icon">✦</div><div class="bot-msg">{chat["text"]}</div></div>', unsafe_allow_html=True)
        if "audio" in chat:
            st.audio(chat["audio"], format="audio/mp3")

# ভয়েস রেকর্ড বাটন (মাইক)
voice_input = st.audio_input("মাইকে কথা বলতে ট্যাপ করুন")

# টেক্সট লেখার ইনপুট বার
prompt = st.chat_input("Gemini-কে প্রশ্ন করুন...")

active_text = prompt or ("ভয়েস মেসেজ পাঠানো হয়েছে" if voice_input else None)

if active_text:
    st.session_state.history.append({"role": "user", "text": active_text})
    
    bot_reply = f"আমি আপনার কথা বুঝতে পেরেছি: '{active_text}'। আপনার জন্য সেরা ভাইরাল কনটেন্ট তৈরি হচ্ছে।"
    
    # ভয়েসে কথা বলার অডিও তৈরি
    tts = gTTS(text=bot_reply, lang='bn', slow=False)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    
    st.session_state.history.append({
        "role": "assistant",
        "text": bot_reply,
        "audio": audio_fp
    })
    st.rerun()
