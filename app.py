import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ViralHook Flash", page_icon="⚡", layout="centered", initial_sidebar_state="collapsed")

# জেমিনাই ইন্টারফেস ও ভয়েস স্ক্রিপ্ট
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 7rem !important;
        max-width: 650px !important;
    }
    header, footer { visibility: hidden !important; }

    /* টপ হেডার বার */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0 15px 0;
        border-bottom: 1px solid rgba(128,128,128,0.15);
    }
    .model-title {
        font-size: 1.15rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .model-dot {
        width: 8px;
        height: 8px;
        background-color: #1a73e8;
        border-radius: 50%;
        display: inline-block;
    }

    /* ইউজার মেসেজ বাবল */
    .user-bubble-container {
        display: flex;
        justify-content: flex-end;
        margin: 15px 0;
    }
    .user-bubble {
        background-color: #f0f4f9;
        color: #1f1f1f;
        padding: 12px 20px;
        border-radius: 22px;
        max-width: 82%;
        font-size: 0.98rem;
        line-height: 1.5;
    }
    @media (prefers-color-scheme: dark) {
        .user-bubble {
            background-color: #282a2c;
            color: #e3e3e3;
        }
    }

    /* এআই রেসপন্স বাবল */
    .bot-container {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin: 15px 0 25px 0;
    }
    .bot-sparkle {
        font-size: 1.2rem;
        margin-top: 2px;
    }
    .bot-content {
        flex: 1;
        font-size: 0.98rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# হেডার সেকশন
h_col1, h_col2, h_col3 = st.columns([1, 5, 2])
with h_col1:
    st.markdown('<div style="font-size:1.3rem; cursor:pointer;">☰</div>', unsafe_allow_html=True)
with h_col2:
    st.markdown('<div class="model-title">ViralHook Flash <span class="model-dot"></span></div>', unsafe_allow_html=True)
with h_col3:
    col_play, col_new = st.columns(2)
    with col_play:
        # নীল রঙের গোল পজ/স্টপ বাটন
        st.button("⏸", key="pause_btn", help="ভয়েস বন্ধ করুন")
    with col_new:
        if st.button("✏️", key="new_chat_btn", help="নতুন চ্যাট"):
            st.session_state.messages = []
            st.rerun()

# মেসেজ হিস্ট্রি
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "assistant", "content": "আমি আপনার ভাইরাল হুক সহকারী। আপনার বিষয় নিচে মুখে বলুন অথবা লিখে পাঠান!"}
    ]

# মেসেজগুলো স্ক্রিনে দেখানো
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'''
        <div class="user-bubble-container">
            <div class="user-bubble">{msg["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="bot-container">
            <div class="bot-sparkle">✦</div>
            <div class="bot-content">{msg["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)

# ভয়েস দিয়ে উত্তর শোনানোর জাভাস্ক্রিপ্ট প্লেয়ার
def speak_bengali_text(text_to_speak):
    clean_text = text_to_speak.replace('"', '').replace("'", "").replace("\n", " ")
    components.html(f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            let utterance = new SpeechSynthesisUtterance("{clean_text}");
            utterance.lang = "bn-IN";
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        }}
    </script>
    """, height=0)

# নিচে ইনপুট বার (মাইক আইকন এবং সেন্ড অপশন সহ)
user_prompt = st.chat_input("Gemini-কে প্রশ্ন করুন... 🎙️")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # এআই উত্তর জেনারেট
    reply = f"""'{user_prompt}'-এর জন্য ভাইরাল হুক তৈরি করা হলো:
1. প্রথম ৩ সেকেন্ডেই দর্শককে চমকে দেওয়ার মতো হুক লাইন।
2. ভিডিওর শেষে এমন একটি প্রশ্ন ছুঁড়ে দিন যাতে কমেন্টে ঝড় ওঠে!"""
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    speak_bengali_text(reply)
    st.rerun()
