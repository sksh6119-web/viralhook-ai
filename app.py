import streamlit as st
from groq import Groq
import json

st.set_page_config(
    page_title="Super AI Live",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF8533);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title {
        text-align: center;
        color: #6c757d;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎙️ Super AI Live Master</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">যা চাইবেন তাই পাবেন — সরাসরি লাইভ কথা বলবে আপনার সাথে!</p>', unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")

mode = st.selectbox(
    "💡 আপনি কী জানতে বা তৈরি করতে চান?",
    [
        "⚡ রিল ও শর্টস স্ক্রিপ্ট (হুক + ডায়ালগ)",
        "🔥 সোশ্যাল মিডিয়া ভাইরাল পোস্ট ও ক্যাপশন",
        "❓ যেকোনো বিষয়ের লাইভ প্রশ্ন-উত্তর",
        "✍️ গল্প, কবিতা ও ক্রিয়েটিভ কন্টেন্ট",
        "📢 ব্যবসা ও প্রোডাক্ট বিক্রির আকর্ষণীয় অফার"
    ]
)

user_input = st.text_area(
    "আপনার প্রশ্ন বা বিষয় লিখুন:",
    placeholder="যেমন: দ্রুত ভিউ বাড়ানোর ৩টি টিপস বলো, অথবা মজার একটি প্রেমের কবিতা শোনাও...",
    height=100
)

if st.button("🚀 উত্তর দিন ও লাইভ কথা বলুন", use_container_width=True):
    if not user_input.strip():
        st.warning("দয়া করে কিছু লিখুন!")
    elif not api_key:
        st.error("API Key পাওয়া যায়নি! Secrets চেক করুন।")
    else:
        try:
            client = Groq(api_key=api_key.strip())

            models_list = client.models.list().data
            valid_models = [m.id for m in models_list if "whisper" not in m.id and "vision" not in m.id]
            active_model = valid_models[0]

            with st.spinner("AI উত্তর তৈরি করছে..."):
                prompt = f"""
                You are an interactive Bengali AI assistant.
                Mode: {mode}
                Provide an energetic, direct, and conversational answer in clean Bengali.
                User: {user_input}
                """
                completion = client.chat.completions.create(
                    model=active_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                answer = completion.choices[0].message.content
                st.markdown(answer)

                clean_text = answer.replace("*", "").replace("#", "").replace("\n", " ")[:350]
                speech_text_json = json.dumps(clean_text)

                st.components.v1.html(f"""
                <script>
                    const text = {speech_text_json};
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'bn-IN';
                    utterance.rate = 1.0;
                    utterance.pitch = 1.0;
                    window.speechSynthesis.speak(utterance);
                </script>
                <div style="padding: 10px; background-color: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; color: #15803d; text-align: center; font-weight: bold;">
                    🔊 AI সরাসরি লাইভ কথা বলছে... (ভলিউম বাড়িয়ে শুনুন)
                </div>
                """, height=80)

        except Exception as e:
            st.error(f"Error: {e}")
