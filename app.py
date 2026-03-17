import streamlit as st
from groq import Groq
import csv
import os
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="MindEase", page_icon="🌿", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #1A1A2E; }
.main-title { text-align: center; color: #02C39A; font-size: 2.8rem; font-weight: bold; }
.subtitle { text-align: center; color: #8FA3B1; font-size: 1rem; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌿 MindEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal AI companion for mental wellness</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Settings")
   api_key = st.secrets["GROQ_API_KEY"]
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

SYSTEM_PROMPT = "You are MindEase, a warm and caring AI mental health companion. Listen with kindness. Validate feelings. Ask gentle follow-up questions. Suggest breathing exercises or journaling when helpful. Use simple language. If user mentions self-harm share this: https://www.iasp.info/resources/Crisis_Centres/ Never diagnose or replace therapy."

tab1, tab2 = st.tabs(["💬 Chat", "😊 Mood Tracker"])

with tab1:
    st.divider()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown("Hi there! I am MindEase. How are you feeling today?")

    for message in st.session_state.messages:
        avatar = "🌿" if message["role"] == "assistant" else "🧑"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    user_input = st.chat_input("Share how you are feeling...")

    if user_input:
        if not api_key:
            st.warning("Please enter your Groq API key in the sidebar.")
        else:
            with st.chat_message("user", avatar="🧑"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("assistant", avatar="🌿"):
                with st.spinner("MindEase is listening..."):
                    try:
                        client = Groq(api_key=api_key)
                        all_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                        for m in st.session_state.messages:
                            all_messages.append({"role": m["role"], "content": m["content"]})
                        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=all_messages)
                        reply = response.choices[0].message.content
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"Something went wrong: {str(e)}")

with tab2:
    st.divider()
    st.markdown("### How are you feeling today?")

    mood = st.radio(
        "Select your mood:",
        ["😊 Happy", "😐 Okay", "😔 Sad", "😰 Stressed", "😡 Angry"],
        horizontal=True
    )

    note = st.text_input("Add a note (optional)", placeholder="What is making you feel this way?")

    if st.button("Save My Mood"):
        mood_file = "mood_log.csv"
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(mood_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([now, mood, note])
        st.success("Mood saved! Keep going Sasani, you are doing great! 🌿")

    st.divider()
    st.markdown("### Your Mood History")

    mood_file = "mood_log.csv"
    if os.path.exists(mood_file):
        df = pd.read_csv(mood_file, names=["Date", "Mood", "Note"])
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            mood_counts = df["Mood"].value_counts().reset_index()
            mood_counts.columns = ["Mood", "Count"]
            st.bar_chart(mood_counts.set_index("Mood"))
        else:
            st.info("No mood logs yet. Save your first mood above!")
    else:
        st.info("No mood logs yet. Save your first mood above!")
