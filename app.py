import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AI অ্যাসিস্ট্যান্ট")
st.caption("আপনার যেকোনো প্রশ্ন লিখুন, সাথে সাথে বুদ্ধিমান উত্তর পেয়ে যাবেন।")

# Adsterra বিজ্ঞাপনের বাটন
ad_link = "https://www.profitableratecpmnetwork.com/h7ssyv17p?key=eb8a14de90b0395f65ebf374d7d4ca71"
st.markdown(
    f"""
    <div style="text-align: center; margin: 15px 0;">
        <a href="{ad_link}" target="_blank" style="text-decoration: none;">
            <button style="
                background: linear-gradient(90deg, #ff4b4b, #ff7676);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            ">
                🎁 Support Us / Check Offer
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# চ্যাট হিস্ট্রি
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# পূর্বের কথোপকথন দেখানো
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# প্রশ্ন করার বক্স
if user_prompt := st.chat_input("কী জানতে চান? এখানে লিখুন..."):
    # ইউজারের মেসেজ যোগ করা
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # আসল AI দিয়ে উত্তর আনা
    with st.chat_message("assistant"):
        with st.spinner("চিন্তাভাবনা করছি..."):
            try:
                system_instruction = "You are a helpful, smart AI assistant. Answer clearly and politely in Bengali."
                full_query = f"{system_instruction}\nUser: {user_prompt}"
                encoded_prompt = urllib.parse.quote(full_query)
                
                # আসল AI API কল
                api_url = f"https://text.pollinations.ai/{encoded_prompt}?model=openai"
                response = requests.get(api_url, timeout=30)
                
                if response.status_code == 200:
                    ai_reply = response.text
                else:
                    ai_reply = "দুঃখিত, এই মুহূর্তে উত্তর তৈরিতে সমস্যা হচ্ছে। আবার চেষ্টা করুন।"
            except Exception:
                ai_reply = "নেটওয়ার্ক সমস্যার কারণে উত্তর পাওয়া যায়নি। একটু পর আবার চেষ্টা করুন।"

            st.markdown(ai_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
