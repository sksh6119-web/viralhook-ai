import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AI অ্যাসিস্ট্যান্ট")
st.caption("আপনার যেকোনো কথা লিখুন, বুদ্ধিমান AI সাথে সাথে উত্তর দেবে।")

# সাইডবারে Groq API Key দেওয়ার বক্স
api_key = st.sidebar.text_input("Groq API Key লিখুন:", type="password")

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

if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট হিস্ট্রি ও স্পিকার বাটন
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            clean_voice = message["content"].replace('"', '').replace("'", "").replace("\n", " ")
            if st.button("🔊 মুখে শুনুন", key=f"speak_{idx}"):
                components.html(
                    f"""
                    <script>
                        if ('speechSynthesis' in window) {{
                            window.speechSynthesis.cancel();
                            let msg = new SpeechSynthesisUtterance("{clean_voice}");
                            msg.lang = 'bn-IN';
                            msg.rate = 1.0;
                            window.speechSynthesis.speak(msg);
                        }}
                    </script>
                    """,
                    height=0
                )

# ইনপুট ও উত্তর তৈরি
if prompt := st.chat_input("কী জানতে চান? এখানে লিখুন..."):
    if not api_key:
        st.warning("⚠️ দয়া করে বাঁদিকের সাইডবার থেকে আপনার Groq API Key দিন!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=api_key.strip())
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a friendly, intelligent AI assistant. Answer warmly and naturally in Bengali. You know the user's name is Saheb."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    model="llama-3.3-70b-versatile",
                )
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.rerun()
            except Exception as e:
                st.error(f"ত্রুটি: {e}")
