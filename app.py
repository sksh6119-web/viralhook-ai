import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("AI Assistant")
st.write("আপনার যেকোনো প্রশ্ন বা প্রম্পট এখানে লিখুন...")

# Initialize Groq client using Streamlit secrets
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception as e:
    st.error(f"এপিআই কি (API Key) কনফিগারেশনে সমস্যা হয়েছে: {e}")
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("আপনার বার্তা লিখুন..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        try:
            # Using the fast and lightweight llama-3.1-8b-instant model
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.7
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_message = f"দুঃখিত, একটি সমস্যা হয়েছে: {str(e)}"
            st.error(error_message)
