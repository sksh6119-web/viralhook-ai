import streamlit as st
from groq import Groq
import re
import json

st.set_page_config(
    page_title="AI Chat Master",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
    .chat-header {
        text-align: center;
        padding: 10px;
        margin-bottom: 20px;
    }
    .chat-header h1 {
        font-size: 2rem;
        background: linear-gradient(45deg, #FF4B4B, #FF8533);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .chat-header p {
        color: #6c757d;
        font-size: 0.95rem;
    }
    </style>
    <div class="chat-header">
        <h1>🤖 AI Chat Master</h1>
        <p>ধর্ম, রাজনীতি, রোমান্স কিংবা টেকনিক্যাল প্রশ্ন — যেকোনো ভাষায় সরাসরি উত্তর ও মিষ্টি লাইভ ভয়েস!</p>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ ভয়েস সেটিংস")
    voice_gender = st.radio(
        "কণ্ঠ নির্বাচন করুন:",
        ["মেয়ের মিষ্টি ও মধুর কণ্ঠ", "ছেলের গম্ভীর কণ্ঠ"],
        index=0
    )
    auto_speak = st.checkbox("স্বয়ংক্রিয়ভাবে কথা বলবে (Auto-Speak)", value=True)
    if st.button("🗑️ নতুন চ্যাট শুরু করুন", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

token = st.secrets.get("GROQ_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "নমস্কার/সালাম! আমি আপনার পার্সোনাল এআই। যেকোনো বিষয়ে প্রশ্ন করুন—আমি সরাসরি সেই ভাষাতেই আপনাকে উত্তর দেব।"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_prompt := st.chat_input("আপনার প্রশ্ন বা মনের কথা এখানে লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    if not token:
        st.error("API Key পাওয়া যায়নি! Streamlit Secrets চেক করুন।")
    else:
        try:
            client = Groq(api_key=token.strip())
            
            models_data = client.models.list().data
            usable_models = [m.id for m in models_data if "whisper" not in m.id and "vision" not in m.id]
            target_model = usable_models[0]

            with st.chat_message("assistant"):
                with st.spinner("উত্তর তৈরি হচ্ছে..."):
                    
                    system_prompt = """
                    You are a highly intelligent, empathetic, direct, and multi-lingual AI assistant.
                    Rules:
                    1. Match the exact language of the user's prompt (Bengali, Hindi, English, etc.).
                    2. Provide direct, objective, and deeply helpful answers immediately. No unnecessary introductory remarks or filler disclaimers.
                    3. If asked about love, relationships, or emotions, speak with genuine charm, warmth, and resonance.
                    4. If asked about scriptures (Quran, Bible, Gita), history, or politics, provide accurate, neutral, and respectful facts.
                    5. For photo/video editing, provide precise instructions or prompts.
                    6. Strictly NEVER output internal thoughts or <think> tags.
                    """

                    convo_history = [{"role": "system", "content": system_prompt}]
                    for m in st.session_state.messages:
                        convo_history.append({"role": m["role"], "content": m["content"]})

                    completion = client.chat.completions.create(
                        model=target_model,
                        messages=convo_history,
                        temperature=0.7,
                    )

                    raw_ans = completion.choices[0].message.content
                    clean_ans = re.sub(r'<think>.*?</think>', '', raw_ans, flags=re.DOTALL).strip()

                    st.markdown(clean_ans)
                    st.session_state.messages.append({"role": "assistant", "content": clean_ans})

                    if auto_speak:
                        speech_text = re.sub(r'[*#_`>\[\]\(\)]', '', clean_ans).replace("\n", " ")[:350]
                        speech_json = json.dumps(speech_text)
                        is_female = "true" if "মেয়ের" in voice_gender else "false"

                        st.components.v1.html(f"""
                        <script>
                            const speechData = {speech_json};
                            const femaleMode = {is_female};
                            window.speechSynthesis.cancel();
                            
                            const utterance = new SpeechSynthesisUtterance(speechData);
                            
                            const hasBengali = /[\\u0980-\\u09FF]/.test(speechData);
                            const hasHindi = /[\\u0900-\\u097F]/.test(speechData);
                            const targetLang = hasBengali ? 'bn-IN' : (hasHindi ? 'hi-IN' : 'en-US');
                            utterance.lang = targetLang;

                            if (femaleMode) {{
                                utterance.pitch = 1.25;
                                utterance.rate = 0.95;
                            }} else {{
                                utterance.pitch = 0.90;
                                utterance.rate = 0.95;
                            }}

                            const voices = window.speechSynthesis.getVoices();
                            const bestVoice = voices.find(v => v.lang.startsWith(targetLang.slice(0, 2)) && (v.name.includes("Google") || v.name.includes("Natural")));
                            if (bestVoice) {{
                                utterance.voice = bestVoice;
                            }}

                            window.speechSynthesis.speak(utterance);
                        </script>
                        """, height=0)

        except Exception as e:
            st.error(f"Error: {e}")
