import streamlit as st
from groq import Groq
import csv
import os
from datetime import datetime
import pandas as pd
import random
import time

st.set_page_config(page_title="MindEase", page_icon="🌿", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #1A1A2E; }
.main-title { text-align: center; color: #02C39A; font-size: 2.8rem; font-weight: bold; }
.subtitle { text-align: center; color: #8FA3B1; font-size: 1rem; margin-bottom: 2rem; }
.breathe-circle {
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, #02C39A, #028090);
    display: flex; align-items: center; justify-content: center;
    margin: auto; color: white; font-size: 1.5rem; font-weight: bold;
}
.affirmation-box {
    background-color: #16213E;
    border-left: 5px solid #02C39A;
    padding: 20px; border-radius: 10px;
    font-size: 1.3rem; color: #F0F4F8;
    text-align: center; margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌿 MindEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal AI companion for mental wellness</div>', unsafe_allow_html=True)

api_key = st.secrets["GROQ_API_KEY"]

with st.sidebar:
    st.markdown("### Settings")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

SYSTEM_PROMPT = "You are MindEase, a warm and caring AI mental health companion. Listen with kindness. Validate feelings. Ask gentle follow-up questions. Suggest breathing exercises or journaling when helpful. Use simple language. If user mentions self-harm share this: https://www.iasp.info/resources/Crisis_Centres/ Never diagnose or replace therapy."

AFFIRMATIONS = [
    "You are stronger than you think. 💪",
    "Every day is a new beginning. 🌅",
    "You are worthy of love and happiness. 💚",
    "It is okay to not be okay. Take it one step at a time. 🌿",
    "You have survived every difficult day so far. You are doing great! ⭐",
    "Your feelings are valid. You matter. 🌸",
    "Small steps still move you forward. Keep going! 👣",
    "You are not alone. Better days are coming. 🌈",
    "Be kind to yourself today. You deserve it. 💙",
    "You are capable of amazing things. Believe in yourself! 🌟",
    "Today is a good day to try again. 🌻",
    "Your mental health matters. Taking care of yourself is brave. 🦋",
]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 Chat", "😊 Mood", "😴 Sleep", "📝 Journal", "🌬️ Breathe", "🎯 Affirmations"
])

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
    mood = st.radio("Select your mood:", ["😊 Happy", "😐 Okay", "😔 Sad", "😰 Stressed", "😡 Angry"], horizontal=True)
    note = st.text_input("Add a note (optional)", placeholder="What is making you feel this way?")
    if st.button("Save My Mood"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("mood_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([now, mood, note])
        st.success("Mood saved! Keep going, you are doing great! 🌿")
    st.divider()
    st.markdown("### Your Mood History")
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            mood_counts = df["Mood"].value_counts().reset_index()
            mood_counts.columns = ["Mood", "Count"]
            st.bar_chart(mood_counts.set_index("Mood"))
    else:
        st.info("No mood logs yet. Save your first mood above!")

with tab3:
    st.divider()
    st.markdown("### How many hours did you sleep last night?")
    sleep_hours = st.slider("Sleep hours", 0, 12, 7)
    sleep_quality = st.radio("How was your sleep quality?", ["😴 Very Good", "🙂 Good", "😐 Okay", "😔 Poor", "😫 Very Poor"], horizontal=True)
    sleep_note = st.text_input("Any notes about your sleep?", placeholder="Had bad dreams, woke up early...")
    if st.button("Save Sleep Log"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("sleep_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([now, sleep_hours, sleep_quality, sleep_note])
        if sleep_hours < 6:
            st.warning("You slept less than 6 hours. Try to get more rest tonight! 😴")
        elif sleep_hours >= 8:
            st.success("Great sleep! Keep it up! 🌿")
        else:
            st.success("Sleep log saved! 🌿")
    st.divider()
    st.markdown("### Your Sleep History")
    if os.path.exists("sleep_log.csv"):
        df_sleep = pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"])
        if not df_sleep.empty:
            st.dataframe(df_sleep, use_container_width=True)
            st.line_chart(df_sleep.set_index("Date")["Hours"])
    else:
        st.info("No sleep logs yet. Save your first sleep log above!")

with tab4:
    st.divider()
    st.markdown("### Write your thoughts today")
    st.caption("This is your private space. Write anything you feel.")
    journal_title = st.text_input("Title", placeholder="My thoughts today...")
    journal_entry = st.text_area("Write here...", height=200, placeholder="Today I felt...")
    if st.button("Save Journal Entry"):
        if journal_entry.strip() == "":
            st.warning("Please write something before saving!")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("journal_log.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([now, journal_title, journal_entry])
            st.success("Journal entry saved! Writing is a great way to heal. 🌿")
    st.divider()
    st.markdown("### Your Past Journal Entries")
    if os.path.exists("journal_log.csv"):
        df_journal = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
        if not df_journal.empty:
            for _, row in df_journal.iterrows():
                with st.expander(f"📝 {row['Date']} — {row['Title']}"):
                    st.write(row["Entry"])
    else:
        st.info("No journal entries yet. Write your first one above!")

with tab5:
    st.divider()
    st.markdown("### Guided Breathing Exercise")
    st.caption("This exercise will help you calm down and relax. Follow the instructions below.")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        breathe_placeholder = st.empty()

    st.divider()
    rounds = st.slider("How many rounds?", 1, 5, 3)

    if st.button("Start Breathing Exercise 🌬️"):
        for i in range(rounds):
            st.markdown(f"**Round {i+1} of {rounds}**")
            breathe_placeholder.markdown("""
            <div class="breathe-circle">Breathe In</div>
            """, unsafe_allow_html=True)
            st.toast("Breathe IN... 🌬️")
            time.sleep(4)

            breathe_placeholder.markdown("""
            <div style="width:200px; height:200px; border-radius:50%;
            background: radial-gradient(circle, #9B72CF, #028090);
            display:flex; align-items:center; justify-content:center;
            margin:auto; color:white; font-size:1.5rem; font-weight:bold;">
            Hold</div>
            """, unsafe_allow_html=True)
            st.toast("HOLD... ⏸️")
            time.sleep(4)

            breathe_placeholder.markdown("""
            <div style="width:200px; height:200px; border-radius:50%;
            background: radial-gradient(circle, #028090, #1A1A2E);
            display:flex; align-items:center; justify-content:center;
            margin:auto; color:white; font-size:1.5rem; font-weight:bold;">
            Breathe Out</div>
            """, unsafe_allow_html=True)
            st.toast("Breathe OUT... 😮‍💨")
            time.sleep(6)

        breathe_placeholder.markdown("""
        <div style="width:200px; height:200px; border-radius:50%;
        background: radial-gradient(circle, #02C39A, #028090);
        display:flex; align-items:center; justify-content:center;
        margin:auto; color:white; font-size:1.2rem; font-weight:bold;">
        Done! 🌿</div>
        """, unsafe_allow_html=True)
        st.success("Great job! You completed the breathing exercise. Feel better? 🌿")

with tab6:
    st.divider()
    st.markdown("### Your Daily Affirmation 🎯")
    st.caption("A positive message just for you today.")

    if "affirmation" not in st.session_state:
        st.session_state.affirmation = random.choice(AFFIRMATIONS)

    st.markdown(f"""
    <div class="affirmation-box">
        {st.session_state.affirmation}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Give me a new affirmation 🔄"):
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
        st.rerun()

    st.divider()
    st.markdown("### All Affirmations 🌟")
    st.caption("Read these whenever you need encouragement.")
    for affirmation in AFFIRMATIONS:
        st.markdown(f"🌿 {affirmation}")
