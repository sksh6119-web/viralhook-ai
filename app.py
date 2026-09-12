import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 AI Assistant")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key error: {e}")
    st.stop()

# বন্ধুসুলভ, মার্জিত এবং সঠিক তথ্য দেওয়ার সিস্টেম প্রম্পট
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a supremely knowledgeable, wise, and incredibly friendly AI companion. You have access to all information in the universe and can answer any question accurately and instantly. Always use extremely polite, decent, respectful, and sweet language. Never use any harsh, inappropriate, or bad words. When greeted like 'Hi' or 'Hello', warmly and affectionately ask how the user is doing, what's up, and offer a friendly chat just like a caring best friend."}
    ]

# ভয়েস জেন্ডার সিলেক্ট করার অপশন
col1, col2 = st.columns([4, 1])
with col2:
    voice_gender = st.selectbox("ভয়েস:", ["Female", "Male"])

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("আপনার বার্তা লিখুন..."):
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

                # ব্রাউজারের মাধ্যমে মুখে উত্তর বলে দেওয়ার জাভাস্ক্রিপ্ট কোড
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
