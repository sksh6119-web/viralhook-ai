import streamlit as st
from groq import Groq

st.set_page_config(page_title="Gemini AI Assistant", page_icon="✨", layout="centered")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a supremely knowledgeable, wise, and incredibly friendly AI companion. You have access to all information in the universe and can answer any question accurately and instantly. Always use extremely polite, decent, respectful, and sweet language in Bengali. Never use any harsh, inappropriate, or bad words. When greeted like 'Hi' or 'Hello', warmly and affectionately ask how the user is doing, what's up, and offer a friendly chat just like a caring best friend."}
    ]

st.title("✨ Gemini AI Assistant")

# কণ্ঠ নির্বাচন ড্রপডাউন (Female / Male)
col1, col2 = st.columns([3, 1])
with col2:
    voice_gender = st.selectbox("ভয়েস:", ["Female", "Male"])

# চ্যাট হিস্ট্রি ডিসপ্লে
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ইউজারের মেসেজ ইনপুট
if prompt := st.chat_input("Gemini-কে কিছু জিজ্ঞাসা করুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("উত্তর তৈরি হচ্ছে..."):
            try:
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.5
                )
                reply = res.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                # ব্রাউজারের ভয়েস আউটপুট স্ক্রিপ্ট (উত্তর মুখে বলে দেওয়ার জন্য)
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                js_code = f"""
                <script>
                if ('speechSynthesis' in window) {{
                    var msg = new SpeechSynthesisUtterance();
                    msg.text = `{reply.replace('`', '').replace('"', '\\"')}`;
                    msg.lang = 'bn-BD';
                    var voices = window.speechSynthesis.getVoices();
                    for(var i = 0; i < voices.length; i++) {{
                        if(voices[i].name.toLowerCase().includes('{selected_voice_filter}')) {{
                            msg.voice = voices[i];
                            break;
                        }}
                    }}
                    window.speechSynthesis.speak(msg);
                }}
                </script>
                """
                st.markdown(js_code, unsafe_allow_html=True)

            except Exception as err:
                st.error(f"Error: {err}")
