import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("AI Assistant")
st.write("আপনার যেকোনো প্রশ্ন বা প্রম্পট এখানে লিখুন...")

# Streamlit Secrets থেকে API Key লোড করা
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("এপিআই কি (API Key) পাওয়া যায়নি! দয়া করে Streamlit Secrets-এ GROQ_API_KEY যুক্ত করুন। জোড়াসাঁকো বা অন্য কোথাও ভুল থাকলে ঠিক করুন।")
else:
    # Groq ক্লাইন্ট ইনিশিয়ালাইজ করা
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a highly intelligent, natural, and helpful AI assistant, similar to Google Gemini."
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("আপনার বার্তা লিখুন..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Groq চ্যাট কমপ্লিশন কল করা
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.7
            )
            response = chat_completion.choices[0].message.content
        except Exception as e:
            response = f"দুঃখিত, একটি সমস্যা হয়েছে: {e}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
