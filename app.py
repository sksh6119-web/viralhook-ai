import streamlit as st
from groq import Groq

st.set_page_config(page_title="ViralHook AI", page_icon="⚡", layout="centered")

st.title("⚡ ViralHook AI")
st.caption("Reels & Shorts Viral Hook + Script Generator")

api_key = st.sidebar.text_input("Groq API Key", type="password")

topic = st.text_area("ভিডিওর বিষয় বা টপিক লিখুন:", placeholder="যেমন: ফেসবুক থেকে টাকা আয় করার ৩টি সহজ উপায়...")

if st.button("Generate Viral Pack"):
    if not api_key:
        st.error("দয়া করে সাইডবার থেকে আপনার Groq API Key দিন!")
    elif not topic:
        st.warning("দয়া করে কোনো টপিক লিখুন!")
    else:
        try:
            clean_key = api_key.strip()
            client = Groq(api_key=clean_key)

            # Groq এর সার্ভার থেকে বর্তমানে চালু থাকা টেক্সট মডেল স্বয়ংক্রিয়ভাবে নেওয়া
            models_list = client.models.list().data
            valid_models = [m.id for m in models_list if "whisper" not in m.id and "vision" not in m.id]
            active_model = valid_models[0]

            with st.spinner("AI স্ক্রিপ্ট তৈরি করছে..."):
                prompt = f"""
                You are an expert viral social media scriptwriter. Write in Bengali.
                Create:
                1. Three scroll-stopping hooks.
                2. A full 30-45 second short video script with visual/action cues.
                3. One clickable thumbnail idea.

                Topic: {topic}
                """
                completion = client.chat.completions.create(
                    model=active_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                st.success("তৈরি সম্পন্ন হয়েছে!")
                st.markdown(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")
