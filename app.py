import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# পৃষ্ঠার কনফিগারেশন এবং লেআউট সাজানো
st.set_page_config(page_title="AI Companion - Saheb", page_icon="✨", layout="centered")

# কাস্টম স্টাইল ও আকর্ষণীয় ডিজাইন
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stChatInput {
        position: fixed;
        bottom: 20px;
        background: white;
        z-index: 999;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("✨ বুদ্ধিদীপ্ত এআই অ্যাসিস্ট্যান্ট")
st.caption("আপনার প্রতিটি কথার বুদ্ধিমান ও মিষ্টি উত্তর দিতে আমি প্রস্তুত।")

# Adsterra বিজ্ঞাপনের আকর্ষণীয় বাটন
ad_link = "https://www.profitableratecpmnetwork.com/h7ssyv17p?key=eb8a14de90b0395f65ebf374d7d4ca71"
button_html = """
    <div style="text-align: center; margin: 15px 0;">
        <a href="{}" target="_blank" style="text-decoration: none;">
            <button style="
                background: linear-gradient(90deg, #ff4b4b, #ff7676);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
            ">
                🎁 Support Us / Check Offer
            </button>
        </a>
    </div>
"""
st.markdown(button_html.format(ad_link), unsafe_allow_html=True)

# আপনার প্রদান করা নতুন Groq API Key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট ইতিহাস এবং মিষ্টি ভয়েস বাটন রেন্ডার করা
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            clean_voice = message["content"].replace('"', '').replace("'", "").replace("\n", " ")
            if st.button("🔊 মিষ্টি সুরে শুনুন", key=f"speak_{idx}"):
                js_code = """
                    <script>
                        if ('speechSynthesis' in window) {
                            window.speechSynthesis.cancel();
                            let msg = new SpeechSynthesisUtterance("{}");
                            msg.lang = 'bn-IN';
                            msg.rate = 0.92;  // ধীর ও স্পষ্ট উচ্চারণ
                            msg.pitch = 1.15; // মিষ্টি ও সুরেলা কণ্ঠস্বর
                            window.speechSynthesis.speak(msg);
                        }
                    </script>
                """
                components.html(js_code.format(clean_voice), height=0)

# ব্যবহারকারীর প্রশ্ন ইনপুট নেওয়ার বক্স
if prompt := st.chat_input("আপনার যেকোনো প্রশ্ন বা কথা এখানে লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("গভীরভাবে ভেবে সুন্দর উত্তর তৈরি করছি..."):
            try:
                # এআই-এর বুদ্ধিমত্তা, ব্যক্তিত্ব ও মিষ্টি স্বভাবের প্রম্পট
                system_prompt = (
                    "You are an exceptionally intelligent, wise, sweet, and warm AI companion. "
                    "You know your creator is Saheb. Always greet Saheb with profound respect, affection, and warmth. "
                    "Provide deep, accurate, thoughtful, and natural responses in Bengali to any topic or question asked, "
                    "empowering the user with wisdom and clarity."
                )
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    model="llama-3.1-8b-instant",
                )
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"ত্রুটি: {e}")
