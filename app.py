import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(page_title="ViralHook AI", page_icon="⚡", layout="centered")

# মডার্ন স্টাইলিং ও কাস্টম সার্চ বার সিএসএস
st.markdown("""
    <style>
    /* ব্যাকগ্রাউন্ড ও টেক্সট স্টাইল */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* হেডার ও হুক স্টাইল */
    .header-box {
        text-align: center;
        padding: 20px 0;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ff4b4b, #ff8533);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #9aa0a6;
        font-size: 0.95rem;
    }
    /* কুইক অ্যাকশন হুক বাটন */
    .hook-pill {
        display: inline-block;
        background: #1f2937;
        color: #e5e7eb;
        padding: 8px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 4px;
        border: 1px solid #374151;
    }
    /* চ্যাট ইনপুট ডিজাইন */
    div[data-testid="stChatInput"] {
        border-radius: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)

# শীর্ষভাগ (Header)
st.markdown("""
<div class="header-box">
    <div class="main-title">⚡ ViralHook AI</div>
    <div class="sub-title">আকর্ষণীয় ভাইরাল হুক, ক্যাপশন ও স্ক্রিপ্ট তৈরির পার্সোনাল অ্যাসিস্ট্যান্ট</div>
</div>
""", unsafe_allow_html=True)

# ভয়েস ইনপুট ও মাইক কন্ট্রোল সেকশন
st.write("### 🎙️ ভয়েস ইনপুট (মাইক কন্ট্রোল)")
col_mic, col_status = st.columns([1, 2])

with col_mic:
    # ব্রাউজার সাপোর্টেড সরাসরি অডিও ইনপুট বাটন
    audio_data = st.audio_input("মাইক ট্যাপ করুন")

with col_status:
    if audio_data:
        st.success("মাইক রেকর্ড গ্রহণ করেছে! প্রসেস করা হচ্ছে...")
    else:
        st.info("কথা বলতে মাইক চাপুন, বন্ধ করতে আবার ট্যাপ করুন।")

# দ্রুত আইডিয়া পাওয়ার জন্য হুক বাটন
st.markdown("---")
st.write("**আইডিয়া বেছে নিন:**")
h_col1, h_col2 = st.columns(2)
with h_col1:
    if st.button("🔥 রোস্টিং/রিঅ্যাকশন হুক", use_container_width=True):
        st.session_state["preset_prompt"] = "একটি চরম আকর্ষণীয় রোস্টিং ভিডিওর ৩ সেকেন্ডের হুক লিখে দাও।"
with h_col2:
    if st.button("📢 প্রমোশনাল হুক", use_container_width=True):
        st.session_state["preset_prompt"] = "একটি কাস্টমার আকৃষ্ট করার মতো প্রমোশনাল বিজ্ঞাপনের হুক লিখে দাও।"

# চ্যাট হিস্ট্রি ধরে রাখার ব্যবস্থা
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "নমস্কার/সালাম! আমি আপনার ভাইরাল হুক সহকারী। আপনার ভিডিও বা পণ্যের বিষয় বলুন, অথবা নিচে মাইক দিয়ে কথা বলুন।"}
    ]

# চ্যাট মেসেজ প্রদর্শন
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# প্রিসেট বাটন থেকে আসা প্রম্পট হ্যান্ডেল করা
default_text = st.session_state.pop("preset_prompt", None)

# নিচে আধুনিক চ্যাট ইনপুট বার
user_query = st.chat_input("আপনার প্রশ্ন বা কনসেপ্ট এখানে লিখুন...") or default_text

if user_query:
    # ব্যবহারকারীর মেসেজ যোগ
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    # এআই উত্তর জেনারেট
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        reply_text = f"**{user_query}** নিয়ে কিছু দুর্দান্ত ভাইরাল হুক অপশন:\n\n1. *'আপনি কি জানেন ৯৯% মানুষ এই বড় ভুলটি করে?...'*\n2. *'ভিডিওটা স্কিপ করার আগে মাত্র ৩ সেকেন্ড সময় দিন!'*\n3. *'শেষ অব্দি না দেখলে কিন্তু চরম মিস করবেন!'*"
        response_placeholder.markdown(reply_text)
        st.session_state.messages.append({"role": "assistant", "content": reply_text})
