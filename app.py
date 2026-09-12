import streamlit as st
from groq import Groq

# পেজ কনফিগারেশন
st.set_page_config(
    page_title="বুদ্ধিদীপ্ত এআই অ্যাসিস্ট্যান্ট",
    page_icon="✨",
    layout="centered"
)

# কাস্টম স্টাইল ও ডিজাইন
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f2937;
        margin-top: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 1rem;
        color: #4b5563;
        margin-bottom: 25px;
    }
    .support-btn {
        display: block;
        width: fit-content;
        margin: 0 auto 30px auto;
        padding: 10px 24px;
        background-color: #ef4444;
        color: white;
        text-align: center;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
    }
    .support-btn:hover {
        background-color: #dc2626;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# হেডার সেকশন
st.markdown('<div class="main-title">✨ বুদ্ধিদীপ্ত এআই অ্যাসিস্ট্যান্ট</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">আপনার প্রতিটি কথা সুচারু ও নির্ভুলভাবে লিখে দেবো।</div>', unsafe_allow_html=True)

# সাপোর্ট বা অফার বাটন
st.markdown('<a href="#" class="support-btn">🔥 Support Us / Check Offer</a>', unsafe_allow_html=True)

st.divider()

# Groq ক্লায়েন্ট ইনিশিয়ালাইজেশন
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    client = None
    st.warning("দয়া করে Streamlit Secrets-এ আপনার GROQ_API_KEY যুক্ত করুন।")

# চ্যাট হিস্ট্রি ধরে রাখার জন্য সেশন স্টেট
if "messages" not in st.session_state:
    st.session_state.messages = []

# পূর্বের চ্যাট মেসেজগুলো দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ব্যবহারকারীর ইনপুট নেওয়া
if prompt := st.chat_input("আপনার যেকোনো প্রশ্ন বা কথা এখানে লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if client:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                model="llama3-70b-8192",
            )
            response = chat_completion.choices[0].message.content
        except Exception as e:
            response = f"দুঃখিত, একটি সমস্যা হয়েছে: {e}"
    else:
        response = f"আপনার কথাটি পেয়েছি: '{prompt}'। (এপিআই কি সেট করা নেই)"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
