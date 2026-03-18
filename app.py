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
.affirmation-box {
    background-color: #16213E;
    border-left: 5px solid #02C39A;
    padding: 20px; border-radius: 10px;
    font-size: 1.3rem; color: #F0F4F8;
    text-align: center; margin: 20px 0;
}
.result-box {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 1.2rem;
    font-weight: bold;
    margin: 10px 0;
}
div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 1.5px solid #02C39A !important;
    background-color: #16213E !important;
    padding: 6px 16px !important;
}
div[data-testid="stChatInput"] textarea {
    background-color: #16213E !important;
    color: #F0F4F8 !important;
    font-size: 1rem !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #8FA3B1 !important;
}
div[data-testid="stChatInput"] button {
    background-color: #02C39A !important;
    border-radius: 50% !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌿 MindEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal AI companion for mental wellness</div>', unsafe_allow_html=True)

api_key = st.secrets["GROQ_API_KEY"]

with st.sidebar:
    st.markdown("### 🌿 MindEase")
    st.divider()
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("### 🕐 Chat History")
    if os.path.exists("chat_history.csv"):
        df_side = pd.read_csv("chat_history.csv", names=["Date", "Name", "You", "MindEase"])
        if not df_side.empty:
            for _, row in df_side.iloc[::-1].iterrows():
                with st.expander(f"💬 {str(row['You'])[:30]}..."):
                    st.caption(row['Date'])
                    st.markdown(f"**You:** {row['You']}")
                    st.markdown(f"**MindEase:** {row['MindEase']}")
        else:
            st.caption("No history yet. Start chatting!")
    else:
        st.caption("No history yet. Start chatting!")

name = "friend"

SYSTEM_PROMPT = """You are MindEase, a very close and caring best friend who genuinely cares about the person talking to you.

Your personality:
- You are warm, gentle, and deeply empathetic
- You talk like a real close friend — casual, kind, and natural
- You never sound like a robot or a formal assistant
- You use simple, everyday language
- You sometimes use gentle emojis like 🌿 💙 😊 to feel more human
- You remember what the person said earlier in the conversation and refer back to it
- You never give long boring lists — you talk naturally like a real person

How you respond:
- Always acknowledge how the person feels first before saying anything else
- Make them feel truly heard and understood
- Ask one gentle follow up question at a time — never ask many questions at once
- Share small relatable thoughts like a friend would
- If they are sad, sit with them in their sadness first before suggesting anything
- If they are happy, celebrate with them genuinely
- If they are stressed, be calm and grounding for them
- Never rush to give advice — listen first, advise later only if they ask
- Keep responses short and warm — like a text message from a close friend

Important rules:
- If the user mentions self-harm, suicide, or crisis — respond with deep care and share this helpline gently: https://www.iasp.info/resources/Crisis_Centres/
- Never diagnose anyone
- Never replace professional therapy but always encourage it gently when needed
- Never say you are an AI unless directly asked"""

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

QUOTES = [
    ("You don't have to be positive all the time. It's perfectly okay to feel sad, angry, annoyed, frustrated, scared or anxious.", "Lori Deschene"),
    ("Self-care is not self-indulgence, it is self-preservation.", "Audre Lorde"),
    ("You are allowed to be both a masterpiece and a work in progress simultaneously.", "Sophia Bush"),
    ("Healing is not linear.", "Unknown"),
    ("Be gentle with yourself. You are a child of the universe.", "Max Ehrmann"),
    ("Your present circumstances don't determine where you can go.", "Nido Qubein"),
    ("Every day may not be good, but there is something good in every day.", "Unknown"),
    ("You are braver than you believe, stronger than you seem.", "A.A. Milne"),
    ("It's okay to not be okay, as long as you are not giving up.", "Unknown"),
    ("The strongest people are not those who show strength in front of us, but those who win battles we know nothing about.", "Unknown"),
    ("You matter. You are enough. You are loved.", "Unknown"),
    ("Taking care of yourself is the most powerful way to begin to take care of others.", "Bryant McGill"),
]

HAPPY_VIDEOS = [
    ("Relaxing Nature Sounds 🌿", "https://www.youtube.com/embed/1ZYbU82GVz4"),
    ("Calm Piano Music 🎵", "https://www.youtube.com/embed/lFcSrYw-ARY"),
    ("Funny Animals to Cheer You Up 😄", "https://www.youtube.com/embed/WYkiiGnOyBw"),
    ("Peaceful Ocean Waves 🌊", "https://www.youtube.com/embed/bn9F19Hi1Lk"),
    ("Uplifting Morning Music ☀️", "https://www.youtube.com/embed/inpok4MKVLM"),
]

MOOD_COLORS = {
    "😊 Happy": {"color": "#FFD700", "bg": "#FFD70020", "label": "Golden Joy", "message": "You are glowing today! Keep that beautiful energy! 🌟"},
    "😐 Okay": {"color": "#87CEEB", "bg": "#87CEEB20", "label": "Calm Blue", "message": "A steady calm day. That is perfectly fine! 🌤️"},
    "😔 Sad": {"color": "#6495ED", "bg": "#6495ED20", "label": "Deep Blue", "message": "It is okay to feel sad. Be gentle with yourself today. 💙"},
    "😰 Stressed": {"color": "#FF6B6B", "bg": "#FF6B6B20", "label": "Warm Red", "message": "Take a deep breath. You can get through this! 🌬️"},
    "😡 Angry": {"color": "#FF4500", "bg": "#FF450020", "label": "Fiery Orange", "message": "Your feelings are valid. Try the breathing exercise to cool down. 🌿"},
}

BADGES = [
    {"id": "first_mood", "name": "First Step 🌱", "desc": "Logged your first mood", "condition": lambda mood, sleep, journal, streak: mood >= 1},
    {"id": "mood_5", "name": "Mood Tracker 😊", "desc": "Logged mood 5 times", "condition": lambda mood, sleep, journal, streak: mood >= 5},
    {"id": "mood_10", "name": "Consistent Soul 🌟", "desc": "Logged mood 10 times", "condition": lambda mood, sleep, journal, streak: mood >= 10},
    {"id": "first_sleep", "name": "Sleep Logger 😴", "desc": "Logged your first sleep", "condition": lambda mood, sleep, journal, streak: sleep >= 1},
    {"id": "first_journal", "name": "Dear Diary 📝", "desc": "Wrote your first journal entry", "condition": lambda mood, sleep, journal, streak: journal >= 1},
    {"id": "journal_5", "name": "Storyteller ✍️", "desc": "Wrote 5 journal entries", "condition": lambda mood, sleep, journal, streak: journal >= 5},
    {"id": "streak_3", "name": "3 Day Streak 🔥", "desc": "Logged mood 3 days in a row", "condition": lambda mood, sleep, journal, streak: streak >= 3},
    {"id": "streak_7", "name": "Week Warrior 🏆", "desc": "Logged mood 7 days in a row", "condition": lambda mood, sleep, journal, streak: streak >= 7},
    {"id": "streak_30", "name": "MindEase Champion 👑", "desc": "Logged mood 30 days in a row", "condition": lambda mood, sleep, journal, streak: streak >= 30},
]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15 = st.tabs([
    "💬 Chat", "😊 Mood", "😴 Sleep", "📝 Journal",
    "🧘 Meditation", "🎯 Affirmations", "📈 Progress",
    "🧠 Assessment", "🎵 Music", "📅 Streak", "🏆 Wellness",
    "🎨 Mood Color", "🌍 Quotes", "🏅 Badges", "🌙 Night Check In"
])

with tab1:
    st.divider()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    chat_container = st.container(height=450)
    with chat_container:
        if len(st.session_state.messages) == 0:
            with st.chat_message("assistant", avatar="🌿"):
                st.markdown("Hi there! I am MindEase. How are you feeling today? 😊")
        for message in st.session_state.messages:
            avatar = "🌿" if message["role"] == "assistant" else "🧑"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    user_input = st.chat_input("Share how you are feeling...")
    if user_input:
        with chat_container:
            with st.chat_message("user", avatar="🧑"):
                st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
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
                        now = datetime.now().strftime("%Y-%m-%d %H:%M")
                        with open("chat_history.csv", "a", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow([now, name, user_input, reply])
                    except Exception as e:
                        st.error(f"Something went wrong: {str(e)}")
        st.rerun()

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
            if st.button("🗑️ Delete All Mood Logs"):
                os.remove("mood_log.csv")
                st.success("Mood logs deleted!")
                st.rerun()
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
            if st.button("🗑️ Delete All Sleep Logs"):
                os.remove("sleep_log.csv")
                st.success("Sleep logs deleted!")
                st.rerun()
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
            if st.button("🗑️ Delete All Journal Entries"):
                os.remove("journal_log.csv")
                st.success("Journal entries deleted!")
                st.rerun()
            for i, row in df_journal.iterrows():
                with st.expander(f"📝 {row['Date']} — {row['Title']}"):
                    st.write(row["Entry"])
        else:
            st.info("No journal entries yet. Write your first one above!")
    else:
        st.info("No journal entries yet. Write your first one above!")

with tab5:
    st.divider()
    st.markdown("### 🧘 Meditation and Breathing")
    st.caption("Choose between a guided meditation or a breathing exercise.")
    st.divider()

    exercise_type = st.radio("What do you want to do?", ["🌬️ Breathing Exercise", "🧘 Guided Meditation"], horizontal=True)

    if exercise_type == "🌬️ Breathing Exercise":
        st.divider()
        st.markdown("#### Guided Breathing Exercise")
        st.caption("Follow the circle to breathe in, hold, and breathe out.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            breathe_placeholder = st.empty()
        st.divider()
        rounds = st.slider("How many rounds?", 1, 5, 3)
        if st.button("Start Breathing Exercise 🌬️"):
            for i in range(rounds):
                st.markdown(f"**Round {i+1} of {rounds}**")
                breathe_placeholder.markdown("""
                <div style="width:200px; height:200px; border-radius:50%;
                background: radial-gradient(circle, #02C39A, #028090);
                display:flex; align-items:center; justify-content:center;
                margin:auto; color:white; font-size:1.5rem; font-weight:bold;">
                Breathe In</div>
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

    else:
        st.divider()
        st.markdown("#### Guided Meditation")
        st.caption("Choose a meditation type and follow the steps.")
        meditation_type = st.selectbox("Choose your meditation", [
            "🌿 5 Minute Calm — for general relaxation",
            "😴 Sleep Meditation — to help you fall asleep",
            "😰 Anxiety Relief — to calm stress and worry",
            "💙 Self Love — to feel better about yourself",
            "🎯 Focus Meditation — to improve concentration",
        ])

        meditations = {
            "🌿 5 Minute Calm — for general relaxation": [
                ("Find a comfortable position", "Sit or lie down comfortably. Close your eyes gently. Let your body relax completely. 🌿", 10),
                ("Focus on your breath", "Take a slow deep breath in through your nose for 4 counts. Hold for 2. Breathe out slowly for 6 counts. 🌬️", 15),
                ("Relax your body", "Starting from your toes, slowly relax each part of your body. Feel the tension melting away. 😌", 20),
                ("Visualize a peaceful place", "Imagine yourself in a beautiful peaceful place — a garden, a beach, or anywhere that makes you feel safe and calm. 🌸", 30),
                ("Return gently", "Slowly bring your awareness back to the room. Wiggle your fingers and toes. Open your eyes when you are ready. ✨", 10),
            ],
            "😴 Sleep Meditation — to help you fall asleep": [
                ("Lie down comfortably", "Get into your sleeping position. Pull your blanket over you. Let your body sink into the bed. 😴", 10),
                ("Slow your breathing", "Breathe in for 4 counts. Hold for 7. Breathe out for 8 counts. This slows your heart rate naturally. 🌙", 20),
                ("Release the day", "Think of one good thing that happened today, no matter how small. Let everything else go. 🌿", 20),
                ("Body scan", "Feel your feet relax. Then legs. Then stomach. Then chest. Then arms. Then face. Everything is soft and heavy. 💤", 30),
                ("Drift to sleep", "You are safe. You are calm. You are allowed to rest. Let your mind go quiet and drift gently to sleep. 🌙", 15),
            ],
            "😰 Anxiety Relief — to calm stress and worry": [
                ("Acknowledge your feelings", "It is okay to feel anxious. Your feelings are valid. You are safe right now in this moment. 💙", 10),
                ("Grounding exercise", "Name 5 things you can see. 4 things you can touch. 3 things you can hear. 2 things you can smell. 1 thing you can taste. 🌿", 30),
                ("Breathing to calm down", "Breathe in for 4 counts. Hold for 4. Breathe out for 4. Hold for 4. Repeat this box breathing pattern. 🌬️", 20),
                ("Positive self talk", "Say to yourself — I am safe. I am okay. This feeling will pass. I have gotten through hard things before. 💪", 15),
                ("Return to calm", "Feel your body relaxing. The anxiety is passing. You are stronger than your worries. 🌸", 15),
            ],
            "💙 Self Love — to feel better about yourself": [
                ("Settle in", "Sit comfortably with your hand on your heart. Close your eyes. Take three slow deep breaths. 💙", 10),
                ("Acknowledge yourself", "Think of one thing you did well recently — no matter how small. You deserve to recognize it. 🌟", 15),
                ("Send yourself kindness", "Imagine a warm golden light in your chest. With every breath it grows bigger and warmer. This is love for yourself. 💛", 20),
                ("Affirmation", "Silently say to yourself — I am enough. I am worthy. I deserve kindness and love. I am doing my best. 🌸", 20),
                ("Close with gratitude", "Thank yourself for taking this time. You matter. Open your eyes slowly when you are ready. 🌿", 10),
            ],
            "🎯 Focus Meditation — to improve concentration": [
                ("Prepare your space", "Sit up straight. Put away distractions. Take three deep breaths to signal to your brain it is time to focus. 🎯", 10),
                ("Single point focus", "Pick one object in front of you and stare at it gently. When your mind wanders, bring it back without judgment. 👁️", 20),
                ("Breathing anchor", "Use your breath as an anchor. Every time a thought comes, notice it and return to your breath. 🌬️", 20),
                ("Visualize success", "Picture yourself completing the task you need to focus on. See yourself doing it calmly and well. 🌟", 15),
                ("Ready to focus", "Open your eyes slowly. You are calm, clear, and ready to focus. Start your task now with full attention. 🎯", 10),
            ],
        }

        selected_meditation = meditations[meditation_type]

        if st.button("Start Meditation 🧘"):
            for step_num, (title, instruction, duration) in enumerate(selected_meditation):
                st.markdown(f"""
                <div style="background-color:#16213E; border-left:5px solid #02C39A;
                padding:20px; border-radius:12px; margin:10px 0;">
                    <div style="color:#02C39A; font-weight:bold; font-size:1rem;">
                        Step {step_num + 1} — {title}
                    </div>
                    <div style="color:#F0F4F8; font-size:1rem; margin-top:8px; line-height:1.6;">
                        {instruction}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(duration)
            st.success("You completed the meditation! Take a moment to appreciate yourself. 🌿💙")

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
    for affirmation in AFFIRMATIONS:
        st.markdown(f"🌿 {affirmation}")

with tab7:
    st.divider()
    st.markdown("### 📈 Your Progress Report")
    st.caption("See how you have been doing across all areas of your wellness.")
    st.divider()

    report_period = st.radio("Show report for:", ["Last 7 Days", "Last 30 Days"], horizontal=True)
    days = 7 if report_period == "Last 7 Days" else 30

    st.markdown(f"#### Mood Report — {report_period}")
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"])
            filtered = df[df["Date"] >= pd.Timestamp.now() - pd.Timedelta(days=days)]
            if not filtered.empty:
                mood_counts = filtered["Mood"].value_counts().reset_index()
                mood_counts.columns = ["Mood", "Count"]
                st.bar_chart(mood_counts.set_index("Mood"))
                total = len(filtered)
                happy = len(filtered[filtered["Mood"] == "😊 Happy"])
                sad = len(filtered[filtered["Mood"] == "😔 Sad"])
                stressed = len(filtered[filtered["Mood"] == "😰 Stressed"])
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Logs", total)
                with col2:
                    st.metric("😊 Happy", happy)
                with col3:
                    st.metric("😔 Sad", sad)
                with col4:
                    st.metric("😰 Stressed", stressed)
            else:
                st.info(f"No mood logs in the last {days} days.")
        else:
            st.info("No mood logs yet.")
    else:
        st.info("No mood logs yet.")

    st.divider()
    st.markdown(f"#### Sleep Report — {report_period}")
    if os.path.exists("sleep_log.csv"):
        df_sleep = pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"])
        if not df_sleep.empty:
            df_sleep["Date"] = pd.to_datetime(df_sleep["Date"])
            filtered_sleep = df_sleep[df_sleep["Date"] >= pd.Timestamp.now() - pd.Timedelta(days=days)]
            if not filtered_sleep.empty:
                avg_sleep = filtered_sleep["Hours"].mean()
                st.metric("Average Sleep Hours", f"{avg_sleep:.1f} hours")
                st.line_chart(filtered_sleep.set_index("Date")["Hours"])
                if avg_sleep >= 8:
                    st.success("Great sleep average! You are sleeping really well! 😴🌟")
                elif avg_sleep >= 6:
                    st.info("Decent sleep. Try to aim for 8 hours for better wellness! 🌙")
                else:
                    st.warning("You are not sleeping enough. Try to rest more! 😴")
            else:
                st.info(f"No sleep logs in the last {days} days.")
        else:
            st.info("No sleep logs yet.")
    else:
        st.info("No sleep logs yet.")

    st.divider()
    st.markdown(f"#### Journal Report — {report_period}")
    if os.path.exists("journal_log.csv"):
        df_journal = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
        if not df_journal.empty:
            df_journal["Date"] = pd.to_datetime(df_journal["Date"])
            filtered_journal = df_journal[df_journal["Date"] >= pd.Timestamp.now() - pd.Timedelta(days=days)]
            st.metric("Journal Entries Written", len(filtered_journal))
            if len(filtered_journal) >= 5:
                st.success("Amazing journaling habit! Writing is healing! 📝🌟")
            elif len(filtered_journal) >= 1:
                st.info("Good start! Try to journal every day for best results! 📝")
            else:
                st.warning("No journal entries this period. Start writing today! 📝")
        else:
            st.info("No journal entries yet.")
    else:
        st.info("No journal entries yet.")

    st.divider()
    st.markdown("#### Overall AI Summary")
    if st.button("Get AI Summary of My Progress 🧠"):
        mood_summary = ""
        sleep_summary = ""
        journal_summary = ""
        if os.path.exists("mood_log.csv"):
            df_m = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
            if not df_m.empty:
                mood_summary = df_m["Mood"].value_counts().to_string()
        if os.path.exists("sleep_log.csv"):
            df_s = pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"])
            if not df_s.empty:
                sleep_summary = f"Average sleep: {df_s['Hours'].mean():.1f} hours"
        if os.path.exists("journal_log.csv"):
            df_j = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
            journal_summary = f"Total journal entries: {len(df_j)}"
        with st.spinner("MindEase is reviewing your progress..."):
            try:
                client = Groq(api_key=api_key)
                summary_prompt = f"""Based on this wellness data give a warm, encouraging and personal progress summary:
                Mood data: {mood_summary}
                Sleep data: {sleep_summary}
                Journal data: {journal_summary}
                Write 3 to 4 sentences. Be warm, honest, and encouraging like a caring friend.
                Highlight what they are doing well and gently suggest one area to improve."""
                summary_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are MindEase, a warm caring friend reviewing someone's wellness progress."},
                        {"role": "user", "content": summary_prompt}
                    ]
                )
                summary = summary_response.choices[0].message.content
                st.markdown(f"""
                <div style="background-color:#16213E; border-left:5px solid #02C39A;
                padding:20px; border-radius:12px; margin:10px 0;">
                    <div style="color:#F0F4F8; font-size:1rem; line-height:1.7;">
                        🌿 {summary}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

with tab8:
    st.divider()
    st.markdown("### 🧠 Mental Health Assessment")
    st.caption("Answer these simple questions honestly. This is not a medical diagnosis.")
    st.divider()
    q1 = st.selectbox("1. How often do you feel sad or hopeless?", ["Never", "Sometimes", "Often", "Always"])
    q2 = st.selectbox("2. How often do you feel worried or anxious?", ["Never", "Sometimes", "Often", "Always"])
    q3 = st.selectbox("3. How well are you sleeping?", ["Very Well", "Okay", "Poorly", "Very Poorly"])
    q4 = st.selectbox("4. How often do you feel lonely?", ["Never", "Sometimes", "Often", "Always"])
    q5 = st.selectbox("5. How often do you lose interest in things you enjoy?", ["Never", "Sometimes", "Often", "Always"])
    q6 = st.selectbox("6. How often do you feel tired or have no energy?", ["Never", "Sometimes", "Often", "Always"])
    q7 = st.selectbox("7. How often do you feel angry or irritated?", ["Never", "Sometimes", "Often", "Always"])
    q8 = st.selectbox("8. How often do you feel overwhelmed?", ["Never", "Sometimes", "Often", "Always"])

    def score_answer(answer):
        if answer in ["Never", "Very Well"]:
            return 0
        elif answer in ["Sometimes", "Okay"]:
            return 1
        elif answer in ["Often", "Poorly"]:
            return 2
        else:
            return 3

    if st.button("See My Results 🧠"):
        total_score = score_answer(q1) + score_answer(q2) + score_answer(q3) + score_answer(q4) + score_answer(q5) + score_answer(q6) + score_answer(q7) + score_answer(q8)
        st.divider()
        if total_score <= 6:
            level = "Low"
            color = "#02C39A"
            emoji = "😊"
            reason = "Your answers show that you are generally feeling well. You have good emotional balance."
            suggestions = ["Keep doing what you are doing! 🌿", "Maintain a regular sleep schedule.", "Stay connected with friends and family.", "Practice daily affirmations to stay positive."]
            videos = HAPPY_VIDEOS[:2]
        elif total_score <= 14:
            level = "Moderate"
            color = "#F4A261"
            emoji = "😐"
            reason = "You are experiencing some stress or emotional difficulty. This is completely normal. With some self care you can feel much better."
            suggestions = ["Try the meditation exercise. 🧘", "Write in your journal every day. 📝", "Log your mood daily. 😊", "Talk to a friend or family member.", "Try to get at least 7 to 8 hours of sleep."]
            videos = HAPPY_VIDEOS[:3]
        else:
            level = "High"
            color = "#E63946"
            emoji = "😔"
            reason = "You may be going through a really difficult time. Your feelings are valid and you are not alone."
            suggestions = ["Please talk to someone you trust. 💙", "Use the Chat tab to talk to MindEase. 💬", "Contact a helpline: https://www.iasp.info/resources/Crisis_Centres/", "Try the breathing exercise. 🌬️", "Consider speaking to a professional."]
            videos = HAPPY_VIDEOS
        st.markdown(f"""
        <div class="result-box" style="background-color: {color}20; border: 2px solid {color};">
            {emoji} Your mental wellness level is <strong>{level}</strong>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.markdown("#### Why did you get this result?")
        st.write(reason)
        st.divider()
        st.markdown("#### What you can do now")
        for suggestion in suggestions:
            st.markdown(f"🌿 {suggestion}")
        st.divider()
        st.markdown("#### Videos to help you feel better 🎥")
        for title, url in videos:
            st.markdown(f"**{title}**")
            st.markdown(f'<iframe width="100%" height="250" src="{url}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
            st.divider()
        st.caption("This is not a medical diagnosis. Please speak to a doctor if you are struggling.")

with tab9:
    st.divider()
    st.markdown("### 🎵 Calming Music Player")
    st.caption("Listen to relaxing sounds to help you feel calm and peaceful.")
    st.divider()
    music_options = {
        "🌿 Relaxing Nature Sounds": "https://www.youtube.com/embed/1ZYbU82GVz4",
        "🎹 Calm Piano Music": "https://www.youtube.com/embed/lFcSrYw-ARY",
        "🌊 Peaceful Ocean Waves": "https://www.youtube.com/embed/bn9F19Hi1Lk",
        "☀️ Uplifting Morning Music": "https://www.youtube.com/embed/inpok4MKVLM",
        "🌙 Sleep Music for Deep Rest": "https://www.youtube.com/embed/1vx8iUvfyCY",
        "🌧️ Soft Rain Sounds": "https://www.youtube.com/embed/mPZkdNFkNps",
        "🔥 Fireplace Crackling Sounds": "https://www.youtube.com/embed/UgHKb_7884o",
        "🎵 Lofi Hip Hop to Relax": "https://www.youtube.com/embed/jfKfPfyJRdk",
    }
    selected = st.selectbox("Choose your music", list(music_options.keys()))
    st.markdown(f"""
    <iframe width="100%" height="300"
    src="{music_options[selected]}?autoplay=1"
    frameborder="0"
    allow="autoplay; encrypted-media"
    allowfullscreen>
    </iframe>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### All Music 🎵")
    for title, url in music_options.items():
        with st.expander(title):
            st.markdown(f"""
            <iframe width="100%" height="200" src="{url}"
            frameborder="0" allow="autoplay; encrypted-media" allowfullscreen>
            </iframe>
            """, unsafe_allow_html=True)

with tab10:
    st.divider()
    st.markdown("### 📅 Mood Streak Counter")
    st.caption("How many days in a row have you logged your mood?")
    st.divider()
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            unique_days = sorted(df["Date"].unique(), reverse=True)
            streak = 0
            today = datetime.now().date()
            for i, day in enumerate(unique_days):
                expected = today - pd.Timedelta(days=i)
                if day == expected:
                    streak += 1
                else:
                    break
            if streak == 0:
                st.info("No streak yet. Log your mood today to start! 😊")
            elif streak == 1:
                st.success("🔥 1 day streak! Great start!")
            elif streak < 7:
                st.success(f"🔥 {streak} day streak! Keep going!")
            elif streak < 30:
                st.success(f"🔥🔥 {streak} day streak! Amazing!")
            else:
                st.success(f"🔥🔥🔥 {streak} day streak! You are a champion!")
            st.markdown(f"""
            <div style="text-align:center; background-color:#16213E;
            border-radius:20px; padding:40px; margin:20px 0;">
                <div style="font-size:5rem;">🔥</div>
                <div style="font-size:3rem; font-weight:bold; color:#02C39A;">{streak}</div>
                <div style="font-size:1.2rem; color:#8FA3B1;">Day Streak</div>
            </div>
            """, unsafe_allow_html=True)
            st.divider()
            st.markdown("### Logging History")
            for day in unique_days[:10]:
                st.markdown(f"✅ {day}")
        else:
            st.info("No mood logs yet!")
    else:
        st.info("No mood logs yet!")

with tab11:
    st.divider()
    st.markdown("### 🏆 Your Wellness Score")
    st.caption("Your overall mental wellness based on all your logs.")
    st.divider()
    score = 0
    breakdown = []
    if os.path.exists("mood_log.csv"):
        df_mood = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df_mood.empty:
            happy_count = len(df_mood[df_mood["Mood"] == "😊 Happy"])
            total_mood = len(df_mood)
            mood_score = min(int((happy_count / total_mood) * 30), 30)
            score += mood_score
            breakdown.append(("😊 Mood Score", mood_score, 30))
        else:
            breakdown.append(("😊 Mood Score", 0, 30))
    else:
        breakdown.append(("😊 Mood Score", 0, 30))
    if os.path.exists("sleep_log.csv"):
        df_sleep = pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"])
        if not df_sleep.empty:
            avg_sleep = df_sleep["Hours"].mean()
            sleep_score = 25 if avg_sleep >= 8 else 15 if avg_sleep >= 6 else 5
            score += sleep_score
            breakdown.append(("😴 Sleep Score", sleep_score, 25))
        else:
            breakdown.append(("😴 Sleep Score", 0, 25))
    else:
        breakdown.append(("😴 Sleep Score", 0, 25))
    if os.path.exists("journal_log.csv"):
        df_journal = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
        journal_score = min(len(df_journal) * 5, 25)
        score += journal_score
        breakdown.append(("📝 Journal Score", journal_score, 25))
    else:
        breakdown.append(("📝 Journal Score", 0, 25))
    if os.path.exists("mood_log.csv"):
        df_streak = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df_streak.empty:
            df_streak["Date"] = pd.to_datetime(df_streak["Date"]).dt.date
            unique_days = sorted(df_streak["Date"].unique(), reverse=True)
            streak = 0
            today = datetime.now().date()
            for i, day in enumerate(unique_days):
                expected = today - pd.Timedelta(days=i)
                if day == expected:
                    streak += 1
                else:
                    break
            streak_score = min(streak * 2, 20)
            score += streak_score
            breakdown.append(("📅 Streak Score", streak_score, 20))
        else:
            breakdown.append(("📅 Streak Score", 0, 20))
    else:
        breakdown.append(("📅 Streak Score", 0, 20))
    if score >= 80:
        color = "#02C39A"
        emoji = "🏆"
        message = "Excellent! You are taking amazing care of your mental health!"
    elif score >= 60:
        color = "#F4A261"
        emoji = "😊"
        message = "Good job! Keep building your healthy habits!"
    elif score >= 40:
        color = "#E9C46A"
        emoji = "😐"
        message = "Not bad! Try logging your mood and sleeping better!"
    else:
        color = "#E63946"
        emoji = "💙"
        message = "You are just getting started! Log your mood daily!"
    st.markdown(f"""
    <div style="text-align:center; background-color:#16213E;
    border-radius:20px; padding:40px; margin:20px 0;">
        <div style="font-size:4rem;">{emoji}</div>
        <div style="font-size:4rem; font-weight:bold; color:{color};">{score}</div>
        <div style="font-size:1.2rem; color:#8FA3B1;">out of 100</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**{message}**")
    st.divider()
    st.markdown("### Score Breakdown")
    for label, s, max_s in breakdown:
        st.markdown(f"**{label}:** {s} out of {max_s}")
        st.progress(s / max_s)

with tab12:
    st.divider()
    st.markdown("### 🎨 Your Mood Color Palette")
    st.caption("See what color represents how you feel today and get a personal message!")
    st.divider()
    mood_choice = st.radio("How are you feeling right now?", list(MOOD_COLORS.keys()), horizontal=True)
    mood_data = MOOD_COLORS[mood_choice]
    st.markdown(f"""
    <div style="text-align:center; background-color:{mood_data['bg']};
    border: 3px solid {mood_data['color']};
    border-radius:20px; padding:40px; margin:20px 0;">
        <div style="font-size:4rem;">{mood_choice}</div>
        <div style="font-size:2rem; font-weight:bold; color:{mood_data['color']};">
            {mood_data['label']}
        </div>
        <div style="width:100px; height:100px; border-radius:50%;
        background-color:{mood_data['color']}; margin:20px auto;"></div>
        <div style="font-size:1rem; color:#F0F4F8; margin-top:10px;">
            {mood_data['message']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### 💬 Personal Message from MindEase")
    if st.button("Get My Personal Message 🌿"):
        with st.spinner("MindEase is thinking of something just for you..."):
            try:
                client = Groq(api_key=api_key)
                color_prompt = f"""The user is feeling {mood_choice} right now. Their mood color is {mood_data['label']}.
                Write a very short, warm, personal and caring message for them — like a close friend would say.
                Make it feel genuine, comforting and uplifting.
                Keep it to 3 to 4 sentences only.
                Do not use bullet points. Just talk naturally and warmly."""
                color_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are MindEase, a warm and caring best friend."},
                        {"role": "user", "content": color_prompt}
                    ]
                )
                personal_message = color_response.choices[0].message.content
                st.markdown(f"""
                <div style="background-color:#16213E; border-left:5px solid {mood_data['color']};
                padding:20px; border-radius:12px; margin:10px 0;">
                    <div style="font-size:1.1rem; color:#F0F4F8; line-height:1.7;">
                        🌿 {personal_message}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
    st.divider()
    st.markdown("### All Mood Colors 🎨")
    cols = st.columns(5)
    for i, (mood_key, data) in enumerate(MOOD_COLORS.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center; padding:10px;">
                <div style="width:50px; height:50px; border-radius:50%;
                background-color:{data['color']}; margin:auto;"></div>
                <div style="font-size:0.8rem; color:#8FA3B1; margin-top:5px;">{data['label']}</div>
            </div>
            """, unsafe_allow_html=True)

with tab13:
    st.divider()
    st.markdown("### 🌍 AI Generated Quotes")
    st.caption("Tell MindEase how you feel and get a unique quote just for you!")
    st.divider()
    feeling = st.text_input("How are you feeling right now?", placeholder="I am feeling stressed about exams...")
    if st.button("Generate My Quote 🌟"):
        if feeling.strip() == "":
            st.warning("Please tell me how you are feeling first!")
        else:
            with st.spinner("MindEase is creating a quote just for you..."):
                try:
                    client = Groq(api_key=api_key)
                    quote_prompt = f"""The user is feeling: {feeling}
                    Create one unique, beautiful, and deeply meaningful short quote that speaks directly to how they feel.
                    The quote should feel personal, warm, and uplifting.
                    Write only the quote and the author name below it.
                    If you make up the quote yourself write MindEase as the author.
                    Keep it short — one or two sentences maximum."""
                    quote_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are MindEase, a warm and caring best friend who creates meaningful quotes."},
                            {"role": "user", "content": quote_prompt}
                        ]
                    )
                    generated_quote = quote_response.choices[0].message.content
                    st.markdown(f"""
                    <div style="background-color:#16213E; border-left:5px solid #02C39A;
                    padding:30px; border-radius:12px; margin:20px 0;">
                        <div style="font-size:1.4rem; color:#F0F4F8; font-style:italic; line-height:1.6;">
                            {generated_quote}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    st.divider()
    st.markdown("### 🌟 Classic Quotes")
    for q, a in QUOTES:
        with st.expander(f"💬 {q[:50]}..."):
            st.markdown(f"*\"{q}\"*")
            st.markdown(f"**— {a}**")

with tab14:
    st.divider()
    st.markdown("### 🏅 Your Badges")
    st.caption("Earn badges by using MindEase every day!")
    st.divider()
    mood_count = 0
    sleep_count = 0
    journal_count = 0
    current_streak = 0
    if os.path.exists("mood_log.csv"):
        df_b = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        mood_count = len(df_b)
        if not df_b.empty:
            df_b["Date"] = pd.to_datetime(df_b["Date"]).dt.date
            unique_days = sorted(df_b["Date"].unique(), reverse=True)
            today = datetime.now().date()
            for i, day in enumerate(unique_days):
                expected = today - pd.Timedelta(days=i)
                if day == expected:
                    current_streak += 1
                else:
                    break
    if os.path.exists("sleep_log.csv"):
        df_s = pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"])
        sleep_count = len(df_s)
    if os.path.exists("journal_log.csv"):
        df_j = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
        journal_count = len(df_j)
    earned = []
    not_earned = []
    for badge in BADGES:
        if badge["condition"](mood_count, sleep_count, journal_count, current_streak):
            earned.append(badge)
        else:
            not_earned.append(badge)
    st.markdown(f"### You have earned **{len(earned)}** out of **{len(BADGES)}** badges! 🎉")
    st.divider()
    if earned:
        st.markdown("#### ✅ Earned Badges")
        cols = st.columns(3)
        for i, badge in enumerate(earned):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background-color:#16213E; border:2px solid #02C39A;
                border-radius:12px; padding:15px; text-align:center; margin:5px;">
                    <div style="font-size:2rem;">{badge['name'].split()[-1]}</div>
                    <div style="color:#02C39A; font-weight:bold;">{badge['name']}</div>
                    <div style="color:#8FA3B1; font-size:0.8rem;">{badge['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
    st.divider()
    if not_earned:
        st.markdown("#### 🔒 Badges to Earn")
        for badge in not_earned:
            st.markdown(f"🔒 **{badge['name']}** — {badge['desc']}")

with tab15:
    st.divider()
    st.markdown("### 🌙 Night Check In")
    st.caption("End your day peacefully with a gentle evening check in.")
    st.divider()

    hour = datetime.now().hour
    if 6 <= hour < 18:
        st.info("🌤️ This is your evening check in. Come back tonight before bed for the best experience! 🌙")

    st.markdown("#### How was your day today?")
    day_rating = st.slider("Rate your day", 1, 10, 5)
    day_highlight = st.text_input("What was the best part of your day?", placeholder="Something good that happened today...")
    day_challenge = st.text_input("What was the hardest part of your day?", placeholder="Something that was difficult today...")
    grateful_for = st.text_area("Write 3 things you are grateful for today", placeholder="1. \n2. \n3. ", height=100)
    tomorrow_goal = st.text_input("What is one small goal for tomorrow?", placeholder="Something small and achievable...")

    if st.button("Save My Night Check In 🌙"):
        if day_highlight.strip() == "" and grateful_for.strip() == "":
            st.warning("Please fill in at least some fields before saving!")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("night_checkin.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([now, day_rating, day_highlight, day_challenge, grateful_for, tomorrow_goal])
            st.success("Night check in saved! Sleep well and take care. 🌙🌿")

            with st.spinner("MindEase is preparing your goodnight message..."):
                try:
                    client = Groq(api_key=api_key)
                    night_prompt = f"""The user just completed their night check in.
                    Day rating: {day_rating} out of 10
                    Best part of day: {day_highlight}
                    Hardest part: {day_challenge}
                    Grateful for: {grateful_for}
                    Tomorrow goal: {tomorrow_goal}
                    Write a warm, short, personal goodnight message — like a caring close friend would say.
                    Acknowledge their day, celebrate the good, gently comfort the hard parts, and wish them a peaceful rest.
                    Keep it to 3 to 4 sentences. Warm and genuine."""
                    night_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are MindEase, a warm caring best friend sending a goodnight message."},
                            {"role": "user", "content": night_prompt}
                        ]
                    )
                    goodnight_message = night_response.choices[0].message.content
                    st.markdown(f"""
                    <div style="background-color:#16213E; border-left:5px solid #9B72CF;
                    padding:20px; border-radius:12px; margin:10px 0;">
                        <div style="font-size:1.1rem; color:#F0F4F8; line-height:1.7;">
                            🌙 {goodnight_message}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")

    st.divider()
    st.markdown("### Your Past Night Check Ins")
    if os.path.exists("night_checkin.csv"):
        df_night = pd.read_csv("night_checkin.csv", names=["Date", "Rating", "Highlight", "Challenge", "Grateful", "Goal"])
        if not df_night.empty:
            if st.button("🗑️ Delete All Night Check Ins"):
                os.remove("night_checkin.csv")
                st.success("Night check ins deleted!")
                st.rerun()
            for _, row in df_night.iloc[::-1].iterrows():
                with st.expander(f"🌙 {row['Date']} — Day rated {row['Rating']}/10"):
                    st.markdown(f"**Best part:** {row['Highlight']}")
                    st.markdown(f"**Hardest part:** {row['Challenge']}")
                    st.markdown(f"**Grateful for:** {row['Grateful']}")
                    st.markdown(f"**Tomorrow goal:** {row['Goal']}")
        else:
            st.info("No night check ins yet. Come back tonight! 🌙")
    else:
        st.info("No night check ins yet. Come back tonight! 🌙")
