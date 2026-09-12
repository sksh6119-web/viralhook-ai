import streamlit as st
from groq import Groq

# ফুল উইডথ লেআউট সেট করা যাতে পুরো স্ক্রিন জুড়ে সুন্দর দেখায়
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Assistant")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a supremely knowledgeable, wise, and incredibly friendly AI companion. You have access to all information in the universe and can answer any question accurately and instantly. Always use extremely polite, decent, respectful, and sweet language in Bengali. Never use any harsh, inappropriate, or bad words. When greeted like 'Hi' or 'Hello', warmly and affectionately ask how the user is doing, what's up, and offer a friendly chat just like a caring best friend."}
    ]

# কণ্ঠ নির্বাচনের অপশন
col1, col2 = st.columns([5, 1])
with col2:
    voice_gender = st.selectbox("ভয়েস:", ["Female", "Male"])

# চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ইনপুট বক্স (ফুল উইডথ মোডে এটি স্বাভাবিক ও বড় দেখাবে)
if prompt := st.chat_input("আপনার বার্তা এখানে লিখুন..."):
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

                # ভয়েস আউটপুট স্ক্রিপ্ট
                selected_voice_filter = "female" if voice_gender == "Female" else "male"
                js_code = f"""
                <script>
                var msg = new SpeechSynthesisUtterance();
                msg.text = `{reply.replace('`', '')}`;
                msg.lang = 'bn-BD';
                var voices = window.speechSynthesis.getVoices();
                for(var i = 0; i < voices.length; i++) {{
                    if(voices[i].name.toLowerCase().includes('{selected_voice_filter}')) {{
                        msg.voice = voices[i];
                        break;
                    }}
                }}
                window.speechSynthesis.speak(msg);
                </script>
                """
                st.markdown(js_code, unsafe_allow_html=True)

            except Exception as err:
                st.error(f"Error: {err}")
