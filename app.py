import streamlit as st
from groq import Groq
import re
import json

st.set_page_config(page_title="Super AI Master Live", page_icon="❤️", layout="centered")

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #ff416c, #ff4b2b);
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

st.markdown('<p class="main-title">❤️ Super AI Master Live</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ভালোবাসা, ধর্ম, রাজনীতি, ফটো-ভিডিও আইডিয়া — সরাসরি উত্তর ও লাইভ ভয়েস!</p>', unsafe_allow_html=True)

k = st.secrets.get("GROQ_API_KEY")

col1, col2 = st.columns(2)
with col1:
    voice_choice = st.selectbox("🎙️ কার কণ্ঠে শুনবেন?", ["মেয়ের মিষ্টি কণ্ঠ", "ছেলের রাশভারী কণ্ঠ"])
with col2:
    mode_choice = st.selectbox("💡 ক্যাটাগরি", [
        "ভালোবাসা ও রোমান্টিক কথা ❤️",
        "পবিত্র ধর্মগ্রন্থ ও ইতিহাস 📖",
        "রাজনীতি ও সমসাময়িক বিষয় 🏛️",
        "ফটো ও ভিডিও এডিটিং আইডিয়া 🎬",
        "যেকোনো সাধারণ প্রশ্নের উত্তর ⚡"
    ])

user_text = st.text_area(
    "আপনার মনের কথা বা প্রশ্ন লিখুন:",
    placeholder="যেমন: ভালোবাসার মানুষকে মুগ্ধ করার কথা, বা কোরআন/বাইবেলের তথ্য, কিংবা ফটো এডিটের আইডিয়া...",
    height=100
)

if st.button("🚀 সরাসরি উত্তর ও লাইভ ভয়েস শুনুন", use_container_width=True):
    if not user_text.strip():
        st.warning("দয়া করে কিছু একটি লিখুন!")
    elif not k:
        st.error("API Key পাওয়া যায়নি! Secrets চেক করুন।")
    else:
        try:
            client = Groq(api_key=k.strip())

            models_data = client.models.list().data
            usable_models = [m.id for m in models_data if "whisper" not in m.id and "vision" not in m.id]
            selected_model = usable_models[0]

            with st.spinner("উত্তর তৈরি হচ্ছে..."):
                prompt = f"""
                You are an all-knowing, empathetic, and sharp AI companion.
                Context/Category: {mode_choice}
                Rules:
                - Answer immediately and directly without any introductory greetings, disclaimers, or filler.
                - If the question is about romance, relationship, or feelings, respond with deep charm, emotional resonance, and lyrical warmth in natural Bengali.
                - If the question is about holy scriptures (Quran, Bible, Gita), politics, or technical steps (photo/video editing concepts), deliver direct, factual, and neutral answers in standard Bengali.
                - Strictly NEVER write thinking steps, internal scratchpads, or <think> tags.
                
                User Query: {user_text}
                """

                completion = client.chat.completions.create(
                    model=selected_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                response_content = completion.choices[0].message.content
                clean_text = re.sub(r'<think>.*?</think>', '', response_content, flags=re.DOTALL).strip()

                st.markdown(clean_text)

                spoken_text = re.sub(r'[*#_`>\[\]\(\)]', '', clean_text).replace("\n", " ")[:350]
                speech_payload = json.dumps(spoken_text)
                is_female = "true" if "মেয়ের" in voice_choice else "false"

                st.components.v1.html(f"""
                <script>
                    const speechData = {speech_payload};
                    const femaleMode = {is_female};
                    window.speechSynthesis.cancel();
                    const voiceMessage = new SpeechSynthesisUtterance(speechData);
                    voiceMessage.lang = 'bn-IN';
                    voiceMessage.pitch = femaleMode ? 1.35 : 0.85;
                    voiceMessage.rate = 1.0;
                    window.speechSynthesis.speak(voiceMessage);
                </script>
                <div style="margin-top:10px; padding: 8px; background-color: #ffe4e6; border: 1px solid #fda4af; border-radius: 8px; color: #be123c; text-align: center; font-weight: bold;">
                    🔊 AI সরাসরি {voice_choice} কথা বলছে...
                </div>
                """, height=70)

        except Exception as err:
            st.error(f"Error: {err}")
