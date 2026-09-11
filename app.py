import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gemini Flash", layout="centered", initial_sidebar_state="collapsed")

# বড় টেক্সট ও ক্লিন জেমিনাই ইন্টারফেস
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
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
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
        padding: 14px 20px;
        border-radius: 24px;
        max-width: 85%;
        font-size: 1.2rem;
        line-height: 1.5;
    }

    /* বড় ফন্টের এআই উত্তর বাবল */
    .bot-box {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin: 15px 0;
    }
    .bot-icon {
        font-size: 1.4rem;
        color: #1f1f1f;
        margin-top: 2px;
    }
    .bot-msg {
        font-size: 1.2rem;
        line-height: 1.6;
        color: #1f1f1f;
        flex: 1;
    }

    /* নিচে জেমিনাই স্টাইল সার্চ বার */
    div[data-testid="stChatInput"] {
        border-radius: 35px !important;
        background-color: #f0f4f9 !important;
        border: 1px solid #e0e3e7 !important;
        padding: 4px 12px !important;
    }
    div[data-testid="stChatInput"] textarea {
        font-size: 1.15rem !important;
        color: #1f1f1f !important;
    }
</style>
""", unsafe_allow_html=True)

# শীর্ষভাগ
h1, h2, h3 = st.columns([1, 6, 2])
with h1:
    st.markdown('<span style="font-size: 1.4rem; cursor:pointer;">☰</span>', unsafe_allow_html=True)
with h2:
    st.markdown('<div class="model-name">Gemini Flash <span class="dot"></span></div>', unsafe_allow_html=True)
with h3:
    st.markdown('<div class="play-circle">▶</div>', unsafe_allow_html=True)

# চ্যাট হিস্ট্রি
if "history" not in st.session_state:
    st.session_state.history = []

# মেসেজগুলো এবং স্পিকার বাটন দেখানো
for idx, chat in enumerate(st.session_state.history):
    if chat["role"] == "user":
        st.markdown(f'<div class="user-box"><div class="user-bubble">{chat["text"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-box"><div class="bot-icon">✦</div><div class="bot-msg">{chat["text"]}</div></div>', unsafe_allow_html=True)
        # প্রতিটি উত্তরের নিচে স্পষ্ট স্পিকার বাটন
        clean_voice = chat["text"].replace('"', '').replace("'", "").replace("\n", " ")
        btn_col, _ = st.columns([2, 5])
        with btn_col:
            if st.button(f"🔊 মুখে শুনুন", key=f"speak_{idx}"):
                components.html(f"""
                <script>
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        let msg = new SpeechSynthesisUtterance("{clean_voice}");
                        msg.lang = 'bn-IN';
                        msg.rate = 1.0;
                        window.speechSynthesis.speak(msg);
                    }}
                </script>
                """, height=0)

# নিচে জেমিনাই ইনপুট বার
prompt = st.chat_input("Gemini-কে প্রশ্ন করুন...")

if prompt:
    st.session_state.history.append({"role": "user", "text": prompt})
    bot_reply = f"আমি আপনার কথা বুঝতে পেরেছি: '{prompt}'। আপনার জন্য ভাইরাল কনটেন্ট তৈরি করা হলো!"
    st.session_state.history.append({"role": "assistant", "text": bot_reply})
    st.rerun()
st.markdown("""<div style="text-align: center; margin: 20px 0;"><a href="https://www.profitableratecpmnetwork.com/h7ssyv17p?key=eb8a14de90b0395f65ebf374d7d4ca71" target="_blank"><button style="background: linear-gradient(90deg, #ff4b4b, #ff7676); color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer;">🎁 Support Us / Check Offer</button></a></div>""", unsafe_allow_html=True)
