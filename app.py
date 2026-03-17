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

HAPPY_VIDEOS = [
    ("Relaxing Nature Sounds 🌿", "https://www.youtube.com/embed/1ZYbU82GVz4"),
    ("Calm Piano Music 🎵", "https://www.youtube.com/embed/lFcSrYw-ARY"),
    ("Funny Animals to Cheer You Up 😄", "https://www.youtube.com/embed/WYkiiGnOyBw"),
    ("Peaceful Ocean Waves 🌊", "https://www.youtube.com/embed/bn9F19Hi1Lk"),
    ("Uplifting Morning Music ☀️", "https://www.youtube.com/embed/inpok4MKVLM"),
]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
    "💬 Chat", "😊 Mood", "😴 Sleep", "📝 Journal",
    "🌬️ Breathe", "🎯 Affirmations", "📊 Weekly Report",
    "🧠 Assessment", "🎵 Music", "📅 Streak", "🏆 Wellness"
])

with tab1:
    st.divider()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown("Hi there! I am MindEase. How are you feeling today? 😊")
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
                    now = datetime.now().strftime("%Y-%m-%d %H:%M")
                    with open("chat_history.csv", "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([now, name, user_input, reply])
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
    st.markdown("### Guided Breathing Exercise")
    st.caption("This exercise will help you calm down and relax.")
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
    st.markdown("### 📊 Your Weekly Mood Report")
    st.caption("Summary of how you felt this week.")
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"])
            last_7 = df[df["Date"] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
            if last_7.empty:
                st.info("No mood logs in the last 7 days. Start logging your mood!")
            else:
                st.markdown("#### Mood Count This Week")
                mood_counts = last_7["Mood"].value_counts().reset_index()
                mood_counts.columns = ["Mood", "Count"]
                st.bar_chart(mood_counts.set_index("Mood"))
                st.divider()
                st.markdown("#### Weekly Summary")
                total = len(last_7)
                happy = len(last_7[last_7["Mood"] == "😊 Happy"])
                sad = len(last_7[last_7["Mood"] == "😔 Sad"])
                stressed = len(last_7[last_7["Mood"] == "😰 Stressed"])
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Logs", total)
                with col2:
                    st.metric("Happy Days", happy)
                with col3:
                    st.metric("Stressed Days", stressed)
                st.divider()
                st.markdown("#### AI says...")
                if happy > stressed and happy > sad:
                    st.success("You had a mostly happy week! Keep doing what makes you feel good! 🌿😊")
                elif stressed > happy:
                    st.warning("You felt stressed a lot this week. Remember to take breaks and breathe! 🌬️")
                elif sad > happy:
                    st.warning("You felt sad quite a bit this week. Talk to someone you trust or use the chat! 💙")
                else:
                    st.info("You had a mixed week. That is completely normal! Keep going! 🌿")
        else:
            st.info("No mood logs yet. Start logging your mood in the Mood tab!")
    else:
        st.info("No mood logs yet. Start logging your mood in the Mood tab!")

with tab8:
    st.divider()
    st.markdown("### 🧠 Mental Health Assessment")
    st.caption("Answer these simple questions honestly. This is not a medical diagnosis. It is just a self check tool to help you understand your feelings better.")
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
        st.markdown("### Your Results")
        if total_score <= 6:
            level = "Low"
            color = "#02C39A"
            emoji = "😊"
            reason = "Your answers show that you are generally feeling well. You have good emotional balance and are managing your feelings in a healthy way."
            suggestions = ["Keep doing what you are doing! 🌿", "Try to maintain a regular sleep schedule.", "Stay connected with friends and family.", "Keep exercising and eating well.", "Practice daily affirmations to stay positive."]
            videos = HAPPY_VIDEOS[:2]
        elif total_score <= 14:
            level = "Moderate"
            color = "#F4A261"
            emoji = "😐"
            reason = "Your answers show that you are experiencing some stress or emotional difficulty. This is completely normal and many people feel this way. With some self care you can feel much better."
            suggestions = ["Try the breathing exercise in the Breathe tab. 🌬️", "Write in your journal every day to release your feelings. 📝", "Log your mood daily to track your progress. 😊", "Take short breaks during the day.", "Talk to a friend or family member about how you feel.", "Try to get at least 7 to 8 hours of sleep every night."]
            videos = HAPPY_VIDEOS[:3]
        else:
            level = "High"
            color = "#E63946"
            emoji = "😔"
            reason = "Your answers show that you may be going through a really difficult time. Your feelings are valid and you are not alone. It is very important to reach out for help and support."
            suggestions = ["Please talk to someone you trust right away. 💙", "Use the Chat tab to talk to MindEase anytime. 💬", "Contact a mental health helpline: https://www.iasp.info/resources/Crisis_Centres/", "Try the breathing exercise when you feel overwhelmed. 🌬️", "Consider speaking to a professional counselor or doctor.", "Be kind to yourself. You deserve support and care. 🌿"]
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
        st.caption("Remember: This is not a medical diagnosis. If you are struggling, please speak to a doctor or mental health professional.")

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
            <iframe width="100%" height="200"
            src="{url}"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen>
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
                st.info("No streak yet. Log your mood today to start your streak! 😊")
            elif streak == 1:
                st.success("🔥 1 day streak! Great start! Keep going tomorrow!")
            elif streak < 7:
                st.success(f"🔥 {streak} day streak! You are building a great habit!")
            elif streak < 30:
                st.success(f"🔥🔥 {streak} day streak! Amazing! You are so consistent!")
            else:
                st.success(f"🔥🔥🔥 {streak} day streak! You are a MindEase champion!")
            st.markdown(f"""
            <div style="text-align:center; background-color:#16213E;
            border-radius:20px; padding:40px; margin:20px 0;">
                <div style="font-size:5rem;">🔥</div>
                <div style="font-size:3rem; font-weight:bold; color:#02C39A;">{streak}</div>
                <div style="font-size:1.2rem; color:#8FA3B1;">Day Streak</div>
            </div>
            """, unsafe_allow_html=True)
            st.divider()
            st.markdown("### Your Logging History")
            st.caption(f"You have logged your mood on {len(unique_days)} different days!")
            for day in unique_days[:10]:
                st.markdown(f"✅ {day}")
        else:
            st.info("No mood logs yet. Start logging your mood to build your streak!")
    else:
        st.info("No mood logs yet. Start logging your mood to build your streak!")

with tab11:
    st.divider()
    st.markdown("### 🏆 Your Wellness Score")
    st.caption("This score shows your overall mental wellness based on your logs.")
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
        message = "Good job! You are doing well. Keep building your healthy habits!"
    elif score >= 40:
        color = "#E9C46A"
        emoji = "😐"
        message = "Not bad! Try logging your mood and sleeping better to improve your score!"
    else:
        color = "#E63946"
        emoji = "💙"
        message = "You are just getting started! Log your mood daily to improve your wellness score!"
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
