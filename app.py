import streamlit as st
from groq import Groq
import re
import json

st.set_page_config(
    page_title="AI Chat Master",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("""
    <style>
    .chat-header {
        text-align: center;
        padding: 8px;
        margin-bottom: 15px;
    }
    .chat-header h1 {
        font-size: 2rem;
        background: linear-gradient(45deg, #FF4B4B, #FF8533);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .chat-header p {
        color: #6c757d;
        font-size: 0.95rem;
    }
    </style>
    <div class="chat-header">
        <h1>🎙️ AI Voice & Chat Master</h1>
        <p>সরাসরি উত্তর, মিষ্টি ও মধুর কণ্ঠ — নতুন প্রশ্ন করলেই আগের কথা সাথে সাথে বন্ধ!</p>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ অডিও সেটিংস")
    voice_gender = st.radio(
        "কণ্ঠ নির্বাচন করুন:",
        ["মেয়ের মিষ্টি ও নরম কণ্ঠ", "ছেলের স্পষ্ট ও গম্ভীর কণ্ঠ"],
        index=0
    )
    auto_speak = st.checkbox("ভয়েস আউটপুট চালু রাখুন", value=True)
    if st.button("🛑 চলমান কথা এখনই থামান", use_container_width=True):
        st.components.v1.html("<script>window.speechSynthesis.cancel();</script>", height=0)
    if st.button("🗑️ চ্যাট ক্লিয়ার করুন", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

token = st.secrets.get("GROQ_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "নমস্কার/সালাম! আমি আপনার পার্সোনাল এআই। যেকোনো প্রশ্ন করুন, সরাসরি উত্তর ও সুন্দর কণ্ঠে শুনতে পাবেন।"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_prompt := st.chat_input("আপনার প্রশ্ন বা মনের কথা লিখুন..."):
    # আপনি প্রশ্ন পাঠানোর সাথে সাথে আগের বাজতে থাকা ভয়েস এক সেকেন্ডে অফ হয়ে যাবে
    st.components.v1.html("<script>window.speechSynthesis.cancel();</script>", height=0)

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
                with st.spinner("উত্তর ভাবছি..."):
                    system_prompt = """
                    You are a highly intelligent, natural, empathetic, and sweet conversational AI.
                    Rules:
                    1. Detect the user's language automatically and answer strictly in that language (Bengali, Hindi, or English).
                    2. Never use robotic filler or formal announcements. Give direct, heartfelt, and clear responses.
                    3. If romance or emotions: Respond with gentle poetic grace and sweetness.
                    4. If religion, politics, or facts: Provide objective, respectful, and direct facts.
                    5. Strictly NEVER write internal thoughts or <think> tags.
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
                        speech_text = re.sub(r'[*#_`>\[\]\(\)]', '', clean_ans).replace("\n", " ")[:300]
                        speech_json = json.dumps(speech_text)
                        is_female = "true" if "মেয়ের" in voice_gender else "false"

                        st.components.v1.html(f"""
                        <script>
                            window.speechSynthesis.cancel();
                            const speechData = {speech_json};
                            const femaleMode = {is_female};
                            
                            const utterance = new SpeechSynthesisUtterance(speechData);
                            
                            const hasBengali = /[\\u0980-\\u09FF]/.test(speechData);
                            const hasHindi = /[\\u0900-\\u097F]/.test(speechData);
                            utterance.lang = hasBengali ? 'bn-IN' : (hasHindi ? 'hi-IN' : 'en-US');

                            // খেনখেনে ভাব দূর করার ন্যাচারাল মিষ্টি টিউনিং
                            if (femaleMode) {{
                                utterance.pitch = 1.05;  // খুব বেশি হাই নয়, সফট মিষ্টি টোন
                                utterance.rate = 0.90;   // শান্ত ও মিষ্টি ধীরগতি
                            }} else {{
                                utterance.pitch = 0.85;  // রাশভারী গম্ভীর টোন
                                utterance.rate = 0.92;
                            }}

                            const voices = window.speechSynthesis.getVoices();
                            const naturalVoice = voices.find(v => v.lang.startsWith(utterance.lang.slice(0, 2)) && 
                                (v.name.includes("Google") || v.name.includes("Natural") || v.name.includes("Neural")));
                            if (naturalVoice) {{
                                utterance.voice = naturalVoice;
                            }}

                            window.speechSynthesis.speak(utterance);
                        </script>
                        """, height=0)

        except Exception as e:
            st.error(f"Error: {e}")
