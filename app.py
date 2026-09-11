import streamlit as st

st.set_page_config(page_title="ViralHook AI", layout="centered", initial_sidebar_state="collapsed")

# জেমিনাই-স্টাইল ক্লিন লাইট/ডার্ক থিম এবং ফ্লোটিং ইনপুট বার সিএসএস
st.markdown("""
<style>
    /* পুরো পেজের মার্জিন ও প্যাডিং ঠিক করা */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
        max-width: 650px !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* টপ হেডার বার */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(128,128,128,0.15);
        margin-bottom: 25px;
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
    .icon-btn {
        font-size: 1.2rem;
        cursor: pointer;
        opacity: 0.8;
    }

    /* ইউজার মেসেজ বাবল (ডানপাশে গোল বাবল) */
    .user-bubble-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 20px;
    }
    .user-bubble {
        background-color: #f0f4f9;
        color: #1f1f1f;
        padding: 12px 20px;
        border-radius: 22px;
        max-width: 80%;
        font-size: 0.98rem;
        line-height: 1.5;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    @media (prefers-color-scheme: dark) {
        .user-bubble {
            background-color: #282a2c;
            color: #e3e3e3;
        }
    }

    /* এআই অ্যাসিস্ট্যান্টের মেসেজ (স্বাভাবিক টেক্সট) */
    .bot-response-container {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 25px;
    }
    .bot-sparkle {
        font-size: 1.1rem;
        margin-top: 2px;
    }
    .bot-text {
        font-size: 1rem;
        line-height: 1.6;
        flex: 1;
    }

    /* নিচের জেমিনাই স্টাইল সার্চ বার কাস্টমাইজেশন */
    div[data-testid="stChatInput"] {
        border-radius: 35px !important;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(128,128,128,0.2) !important;
        padding-left: 10px !important;
    }
    div[data-testid="stChatInput"] textarea {
        font-size: 0.98rem !important;
    }
</style>
""", unsafe_allow_html=True)

# টপ বার (Top Bar)
col_left, col_mid, col_right = st.columns([1, 6, 1])
with col_left:
    st.markdown('<div class="icon-btn">☰</div>', unsafe_allow_html=True)
with col_mid:
    st.markdown('<div class="model-title">ViralHook Flash <span class="model-dot"></span></div>', unsafe_allow_html=True)
with col_right:
    if st.button("✏️", help="New Chat"):
        st.session_state.messages = []
        st.rerun()

# মেসেজ হিস্ট্রি
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "assistant", "content": "আমি আপনার ভাইরাল হুক সহকারী। আপনার কনটেন্টের আইডিয়া বলুন বা ভিডিওর বিষয় লিখে জানান।"}
    ]

# মেসেজগুলো রেন্ডার করা
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'''
        <div class="user-bubble-container">
            <div class="user-bubble">{msg["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="bot-response-container">
            <div class="bot-sparkle">✦</div>
            <div class="bot-text">{msg["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)

# মাইক্রোফোন ভয়েস ইনপুট টগল (পপ-আপ / কলাপ্সিবল)
with st.expander("🎙️ ভয়েস রেকর্ড অন/অফ করতে এখানে ট্যাপ করুন"):
    voice_audio = st.audio_input("কথা বলুন")
    if voice_audio:
        st.info("ভয়েস রেকর্ড গ্রহণ করা হয়েছে।")

# নিচের জেমিনাই স্টাইল সার্চ বার
prompt = st.chat_input("ViralHook-কে কিছু জিজ্ঞাসা করুন...")

if prompt:
    # ইউজারের চ্যাট অ্যাড
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # আকর্ষণীয় ভাইরাল হুক তৈরি
    ai_reply = f"""**"{prompt}"**-এর জন্য কিছু দুর্দান্ত ভাইরাল হুক আইডিয়া:

1. **কৌতূহল হুক:** *"এই ভুলটা করার আগে মাত্র ৩ সেকেন্ড ভাবুন... কারণ এটাই আপনার ৯০% লস করাচ্ছে!"*
2. **চ্যালেঞ্জিং হুক:** *"ভিডিওটা শেষ অব্দি দেখার সাহস আছে তো? সত্যিটা শুনলে চমকে যাবেন!"*
3. **সরাসরি ভ্যালু হুক:** *"মাত্র ২টি নিয়ম মেনে চললে ফলাফল দেখে আপনি নিজেই বিশ্বাস করতে পারবেন না!"*"""
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.rerun()
