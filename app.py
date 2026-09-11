import streamlit as st

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AI অ্যাসিস্ট্যান্ট")
st.caption("আপনার যেকোনো প্রশ্ন লিখুন, নিচে উত্তর পাবেন।")

# Adsterra বাটন
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

def get_smart_reply(text):
    text_clean = text.lower().strip()
    if any(w in text_clean for w in ["কেমন আছো", "কেমন আছেন", "how are you"]):
        return "আমি খুব ভালো আছি! আপনি কেমন আছেন? আপনাকে কীভাবে সাহায্য করতে পারি বলুন।"
    elif any(w in text_clean for w in ["হাই", "হ্যালো", "নমস্কার", "সালাম", "hello", "hi"]):
        return "নমস্কার! বলুন, আজ আপনাকে কীভাবে সাহায্য করব?"
    elif any(w in text_clean for w in ["নাম কি", "তোমার নাম", "who are you"]):
        return "আমি একটি কৃত্রিম বুদ্ধিমত্তা চালিত স্মার্ট চ্যাটবট। আপনার প্রশ্নের উত্তর দিতে এখানে আছি।"
    elif any(w in text_clean for w in ["রাজনীতি", "রাজনীতির অবস্থা"]):
        return "রাজনীতি সবসময়ই পরিবর্তনশীল ও গতিশীল একটি ক্ষেত্র। আপনি নির্দিষ্ট কোন বিষয়ে বা অঞ্চলের রাজনৈতিক পরিস্থিতি সম্পর্কে জানতে চান বলুন।"
    elif any(w in text_clean for w in ["ধন্যবাদ", "thanks", "thank you"]):
        return "আপনাকে অনেক ধন্যবাদ! আরো কিছু জানতে চাইলে স্বচ্ছন্দে বলুন।"
    else:
        return f"আমি আপনার বিষয়টি বুঝতে পেরেছি। '{text}' সম্পর্কিত আরও সুনির্দিষ্ট তথ্য পেতে আপনার প্রশ্নটি একটু বিস্তারিত লিখুন।"

if user_prompt := st.chat_input("কী জানতে চান? এখানে লিখুন..."):
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        ai_reply = get_smart_reply(user_prompt)
        st.markdown(ai_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
