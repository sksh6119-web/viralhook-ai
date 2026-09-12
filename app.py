import streamlit as st

st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="wide")

# ব্যাকগ্রাউন্ড ও স্টাইলিং
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f0f4f9; font-family: 'Segoe UI', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='color: #1f1f1f;'>✨ Gemini AI</h3>", unsafe_allow_html=True)

# অ্যাড ব্যানার
st.markdown("""
    <a href="https://www.profitableratecpmnetwork.com/txpfccym?key=16ed7712c3ae7b7b8d90efb5c53300b3" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(135deg, #1a73e8, #34a853); color: white; padding: 14px 20px; border-radius: 16px; text-align: center; font-size: 16px; font-weight: 600; margin-bottom: 20px;">
            🚀 বিশেষ অফার ও আপডেট দেখতে এখানে ক্লিক করুন! (Sponsored)
        </div>
    </a>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "নমস্কার! 😊 আমি আপনার জেমিনি সহকারী। বলুন, আপনাকে কীভাবে সাহায্য করতে পারি?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Gemini-কে কিছু জিজ্ঞাসা করুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        reply = "আপনার কথাটি আমি পেয়েছি। এটি অত্যন্ত চমৎকার একটি বিষয়!"
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
