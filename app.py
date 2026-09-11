import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AI অ্যাসিস্ট্যান্ট")
st.caption("আপনার যেকোনো কথা বা প্রশ্ন লিখুন, বুদ্ধিমান AI সাথে সাথে সবকিছুর উত্তর দেবে।")

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

# আপনার ফিক্সড Groq API Key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# পুরনো চ্যাট মেসেজগুলো স্ক্রিনে দেখানোর জন্য
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

# প্রশ্ন করার বক্স (st.chat_input নিজে থেকেই রিস্টার্ট করে, আলাদা st.rerun() এর প্রয়োজন নেই)
if prompt := st.chat_input("যেকোনো প্রশ্ন বা কথা এখানে লিখুন..."):
    # ইউজারের মেসেজ সেশন স্টেটে যোগ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # অ্যাসিস্ট্যান্টের উত্তর জেনারেট করা
    with st.chat_message("assistant"):
        with st.spinner("ভেবে উত্তর তৈরি করছি..."):
            try:
                system_prompt = (
                    "You are a universally intelligent, polite, and helpful AI assistant. "
                    "You know your creator is Saheb. Greet Saheb with respect and warmth. "
                    "Answer any question thoroughly, accurately, and naturally in Bengali on all topics."
                )
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    model="llama-3.3-70b-versatile",
                )
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                
                # অ্যাসিস্ট্যান্টের উত্তর সেশন স্টেটে যোগ করা
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"ত্রুটি: {e}")
