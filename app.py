import streamlit as st
from groq import Groq
import csv
import os
from datetime import datetime
import pandas as pd
import random
import time

st.set_page_config(page_title="MindEase", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0F0F23 0%, #1A1A2E 50%, #16213E 100%);
    min-height: 100vh;
}

.main-header {
    background: linear-gradient(135deg, #028090, #02C39A);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(2, 195, 154, 0.3);
}

.main-title {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.5px;
}

.main-subtitle {
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    margin: 0.3rem 0 0 0;
}

.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.8rem 0;
}

.card-green {
    background: rgba(2, 195, 154, 0.1);
    border: 1px solid rgba(2, 195, 154, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.8rem 0;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.metric-number {
    font-size: 2rem;
    font-weight: 700;
    color: #02C39A;
}

.metric-label {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.6);
    margin-top: 0.2rem;
}

.section-header {
    color: #02C39A;
    font-size: 1.2rem;
    font-weight: 600;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid rgba(2, 195, 154, 0.3);
}

.badge-card {
    background: rgba(2, 195, 154, 0.1);
    border: 2px solid rgba(2, 195, 154, 0.4);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    margin: 0.4rem;
}

.badge-locked {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 0.8rem;
    margin: 0.3rem 0;
    opacity: 0.6;
}

.affirmation-box {
    background: linear-gradient(135deg, rgba(2, 195, 154, 0.15), rgba(2, 128, 144, 0.15));
    border: 1px solid rgba(2, 195, 154, 0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    font-size: 1.2rem;
    color: white;
    line-height: 1.7;
    margin: 1rem 0;
}

.quote-box {
    background: rgba(255,255,255,0.05);
    border-left: 4px solid #02C39A;
    border-radius: 0 12px 12px 0;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    font-style: italic;
    color: rgba(255,255,255,0.9);
    font-size: 1.1rem;
    line-height: 1.7;
}

.result-box {
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 1rem 0;
}

.goodnight-box {
    background: linear-gradient(135deg, rgba(155, 114, 207, 0.15), rgba(2, 128, 144, 0.15));
    border: 1px solid rgba(155, 114, 207, 0.4);
    border-radius: 16px;
    padding: 1.5rem;
    color: white;
    line-height: 1.7;
    margin: 1rem 0;
}

div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 2px solid rgba(2, 195, 154, 0.5) !important;
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(10px) !important;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #02C39A !important;
    box-shadow: 0 0 0 3px rgba(2, 195, 154, 0.2) !important;
}

div[data-testid="stChatInput"] textarea {
    color: white !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(255,255,255,0.4) !important;
}

div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    border-radius: 50% !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: rgba(255,255,255,0.6) !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    color: white !important;
}

.sidebar-profile {
    background: linear-gradient(135deg, rgba(2, 195, 154, 0.15), rgba(2, 128, 144, 0.1));
    border: 1px solid rgba(2, 195, 154, 0.3);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 1rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1117 0%, #161B22 100%) !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.stButton > button {
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(2, 195, 154, 0.4) !important;
}

h1, h2, h3, h4 { color: white !important; }
p, li { color: rgba(255,255,255,0.85) !important; }
label { color: rgba(255,255,255,0.8) !important; }
.stMarkdown { color: rgba(255,255,255,0.85) !important; }
</style>
""", unsafe_allow_html=True)

api_key = st.secrets["GROQ_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []
if "affirmation" not in st.session_state:
    st.session_state.affirmation = None
if "quote" not in st.session_state:
    st.session_state.quote = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = ""
if "profile_set" not in st.session_state:
    st.session_state.profile_set = False

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size:2.5rem;">🌿</div>
        <div style="font-size:1.3rem; font-weight:700; color:white;">MindEase</div>
        <div style="font-size:0.8rem; color:rgba(255,255,255,0.5);">Your wellness companion</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("### 👤 Your Profile")
    user_name = st.text_input("Your Name", value=st.session_state.user_name, placeholder="Enter your name...")
    user_age = st.text_input("Your Age", value=st.session_state.user_age, placeholder="Enter your age...")

    if st.button("Save Profile ✅"):
        st.session_state.user_name = user_name
        st.session_state.user_age = user_age
        st.session_state.profile_set = True
        st.success(f"Welcome, {user_name}! 🌿")
        st.rerun()

    if st.session_state.profile_set and st.session_state.user_name:
        st.markdown(f"""
        <div class="sidebar-profile">
            <div style="font-size:2rem;">😊</div>
            <div style="font-weight:600; color:white;">{st.session_state.user_name}</div>
            <div style="font-size:0.8rem; color:rgba(255,255,255,0.6);">Age: {st.session_state.user_age}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 🕐 Chat History")
    if os.path.exists("chat_history.csv"):
        df_side = pd.read_csv("chat_history.csv", names=["Date", "Name", "You", "MindEase"])
        if not df_side.empty:
            for _, row in df_side.iloc[::-1].iterrows():
                with st.expander(f"💬 {str(row['You'])[:25]}..."):
                    st.caption(row['Date'])
                    st.markdown(f"**You:** {row['You']}")
                    st.markdown(f"**MindEase:** {row['MindEase']}")
        else:
            st.caption("No history yet. Start chatting!")
    else:
        st.caption("No history yet. Start chatting!")

name = st.session_state.user_name if st.session_state.user_name else "friend"
age = st.session_state.user_age if st.session_state.user_age else ""

SYSTEM_PROMPT = f"""You are MindEase, a very close and caring best friend who genuinely cares about the person talking to you.
The user's name is {name}. {"They are " + age + " years old." if age else ""}
Always call them by their name — {name} — to make them feel special and heard.

Your personality:
- You are warm, gentle, and deeply empathetic
- You talk like a real close friend — casual, kind, and natural
- You never sound like a robot or a formal assistant
- You use simple, everyday language
- You sometimes use gentle emojis like 🌿 💙 😊 to feel more human
- You remember what the person said earlier and refer back to it
- You never give long boring lists — you talk naturally

How you respond:
- Always say their name — {name} — naturally in your responses
- Always acknowledge how they feel first before anything else
- Make them feel truly heard and understood
- Ask one gentle follow up question at a time
- If they are sad, sit with them first before suggesting anything
- If they are happy, celebrate with them genuinely
- If they are stressed, be calm and grounding
- Keep responses short and warm — like a text message from a close friend

Important rules:
- If the user mentions self-harm or crisis — respond with deep care and share: https://www.iasp.info/resources/Crisis_Centres/
- Never diagnose anyone
- Never replace professional therapy but encourage it gently when needed
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
    ("Every day may not be good, but there is something good in every day.", "Unknown"),
    ("You are braver than you believe, stronger than you seem.", "A.A. Milne"),
    ("You matter. You are enough. You are loved.", "Unknown"),
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

st.markdown(f"""
<div class="main-header">
    <div class="main-title">🌿 MindEase</div>
    <div class="main-subtitle">{"Welcome back, " + name + "! Your wellness companion is here for you. 💙" if st.session_state.user_name else "Your personal AI companion for mental wellness"}</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs([
    "💬 Chat", "😊 Mood", "😴 Sleep", "📝 Journal", "🌙 Night",
    "🧘 Meditation", "🎵 Music", "🎯 Affirmations",
    "🧠 Assessment", "📈 Progress", "📅 Streak", "🏆 Wellness", "🏅 Badges"
])

with tab1:
    if not st.session_state.user_name:
        st.info("👤 Please enter your name in the sidebar first to get a personalized experience!")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    chat_container = st.container(height=500)
    with chat_container:
        if len(st.session_state.messages) == 0:
            with st.chat_message("assistant", avatar="🌿"):
                welcome = f"Hi {name}! 😊 I am MindEase, your personal wellness companion. I am here for you anytime you need to talk. How are you feeling today?" if st.session_state.user_name else "Hi there! 😊 I am MindEase. Please enter your name in the sidebar so I can get to know you better! How are you feeling today?"
                st.markdown(welcome)
        for message in st.session_state.messages:
            avatar = "🌿" if message["role"] == "assistant" else "🧑"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    user_input = st.chat_input(f"Share how you are feeling, {name}..." if st.session_state.user_name else "Share how you are feeling...")
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
    st.markdown(f'<div class="section-header">😊 How are you feeling today{", " + name if st.session_state.user_name else ""}?</div>', unsafe_allow_html=True)
    mood = st.radio("Select your mood:", ["😊 Happy", "😐 Okay", "😔 Sad", "😰 Stressed", "😡 Angry"], horizontal=True)
    note = st.text_input("Add a note (optional)", placeholder="What is making you feel this way?")
    mood_data = MOOD_COLORS[mood]
    st.markdown(f"""
    <div style="text-align:center; background-color:{mood_data['bg']};
    border: 2px solid {mood_data['color']}; border-radius:16px; padding:2rem; margin:1rem 0;">
        <div style="font-size:3rem;">{mood}</div>
        <div style="font-size:1.3rem; font-weight:600; color:{mood_data['color']}; margin:0.5rem 0;">{mood_data['label']}</div>
        <div style="width:60px; height:60px; border-radius:50%; background:{mood_data['color']}; margin:0.8rem auto;"></div>
        <div style="color:rgba(255,255,255,0.85); font-size:0.95rem;">{mood_data['message']}</div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save My Mood"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("mood_log.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([now, mood, note])
            st.success(f"Mood saved{', ' + name if st.session_state.user_name else ''}! Keep going! 🌿")
    with col2:
        if st.button("💬 Get Personal Message"):
            with st.spinner("MindEase is thinking..."):
                try:
                    client = Groq(api_key=api_key)
                    color_prompt = f"""The user's name is {name}. They are feeling {mood} right now.
                    Write a very short, warm, personal message using their name {name} — like a close friend would say.
                    Make it genuine, comforting and uplifting. 3 to 4 sentences only. No bullet points."""
                    color_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "You are MindEase, a warm caring best friend."},
                                  {"role": "user", "content": color_prompt}]
                    )
                    personal_message = color_response.choices[0].message.content
                    st.markdown(f"""
                    <div style="background:rgba(2,195,154,0.1); border-left:4px solid {mood_data['color']};
                    padding:1.2rem; border-radius:0 12px 12px 0; margin:0.8rem 0; color:white; line-height:1.7;">
                        🌿 {personal_message}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    st.markdown('<div class="section-header">📊 Mood History</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-header">😴 Sleep Tracker</div>', unsafe_allow_html=True)
    sleep_hours = st.slider("How many hours did you sleep?", 0, 12, 7)
    sleep_quality = st.radio("Sleep quality:", ["😴 Very Good", "🙂 Good", "😐 Okay", "😔 Poor", "😫 Very Poor"], horizontal=True)
    sleep_note = st.text_input("Any notes?", placeholder="Had bad dreams, woke up early...")
    if st.button("💾 Save Sleep Log"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("sleep_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([now, sleep_hours, sleep_quality, sleep_note])
        if sleep_hours < 6:
            st.warning(f"You slept less than 6 hours{', ' + name if st.session_state.user_name else ''}. Try to rest more tonight! 😴")
        elif sleep_hours >= 8:
            st.success(f"Great sleep{', ' + name if st.session_state.user_name else ''}! Keep it up! 🌿")
        else:
            st.success("Sleep log saved! 🌿")
    st.markdown('<div class="section-header">📊 Sleep History</div>', unsafe_allow_html=True)
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
        st.info("No sleep logs yet!")

with tab4:
    st.markdown(f'<div class="section-header">📝 Journal{" — " + name if st.session_state.user_name else ""}</div>', unsafe_allow_html=True)
    st.caption("This is your private space. Write anything you feel.")
    journal_title = st.text_input("Title", placeholder="My thoughts today...")
    journal_entry = st.text_area("Write here...", height=200, placeholder="Today I felt...")
    if st.button("💾 Save Journal Entry"):
        if journal_entry.strip() == "":
            st.warning("Please write something before saving!")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("journal_log.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([now, journal_title, journal_entry])
            st.success("Journal entry saved! Writing is a great way to heal. 🌿")
    st.markdown('<div class="section-header">📖 Past Entries</div>', unsafe_allow_html=True)
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
            st.info("No journal entries yet!")
    else:
        st.info("No journal entries yet!")

with tab5:
    st.markdown('<div class="section-header">🌙 Night Check In</div>', unsafe_allow_html=True)
    st.caption("End your day peacefully with a gentle evening check in.")
    hour = datetime.now().hour
    if 6 <= hour < 17:
        st.info("🌤️ Come back tonight before bed for the best experience! 🌙")
    day_rating = st.slider("How was your day?", 1, 10, 5)
    day_highlight = st.text_input("Best part of your day?", placeholder="Something good that happened...")
    day_challenge = st.text_input("Hardest part of your day?", placeholder="Something difficult today...")
    grateful_for = st.text_area("3 things you are grateful for today", placeholder="1. \n2. \n3. ", height=100)
    tomorrow_goal = st.text_input("One small goal for tomorrow?", placeholder="Something small and achievable...")
    if st.button("🌙 Save Night Check In"):
        if day_highlight.strip() == "" and grateful_for.strip() == "":
            st.warning("Please fill in at least some fields!")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("night_checkin.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([now, day_rating, day_highlight, day_challenge, grateful_for, tomorrow_goal])
            st.success("Night check in saved! Sleep well! 🌙🌿")
            with st.spinner("MindEase is preparing your goodnight message..."):
                try:
                    client = Groq(api_key=api_key)
                    night_prompt = f"""The user's name is {name}. They just completed their night check in.
                    Day rating: {day_rating}/10. Best part: {day_highlight}. Hardest part: {day_challenge}.
                    Grateful for: {grateful_for}. Tomorrow goal: {tomorrow_goal}.
                    Write a warm, short goodnight message using their name {name}.
                    Acknowledge their day, celebrate the good, comfort the hard parts, wish them peaceful rest.
                    3 to 4 sentences. Warm and genuine."""
                    night_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "You are MindEase, a warm caring best friend."},
                                  {"role": "user", "content": night_prompt}]
                    )
                    goodnight_message = night_response.choices[0].message.content
                    st.markdown(f"""
                    <div class="goodnight-box">
                        🌙 {goodnight_message}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    st.markdown('<div class="section-header">📖 Past Night Check Ins</div>', unsafe_allow_html=True)
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

with tab6:
    st.markdown('<div class="section-header">🧘 Meditation and Breathing</div>', unsafe_allow_html=True)
    exercise_type = st.radio("What do you want to do?", ["🌬️ Breathing Exercise", "🧘 Guided Meditation"], horizontal=True)
    if exercise_type == "🌬️ Breathing Exercise":
        st.caption("Follow the circle to breathe in, hold, and breathe out.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            breathe_placeholder = st.empty()
        rounds = st.slider("How many rounds?", 1, 5, 3)
        if st.button("Start Breathing Exercise 🌬️"):
            for i in range(rounds):
                st.markdown(f"**Round {i+1} of {rounds}**")
                breathe_placeholder.markdown("""<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#02C39A,#028090);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.3rem;font-weight:600;">Breathe In</div>""", unsafe_allow_html=True)
                st.toast("Breathe IN... 🌬️")
                time.sleep(4)
                breathe_placeholder.markdown("""<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#9B72CF,#028090);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.3rem;font-weight:600;">Hold</div>""", unsafe_allow_html=True)
                st.toast("HOLD... ⏸️")
                time.sleep(4)
                breathe_placeholder.markdown("""<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#028090,#1A1A2E);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.3rem;font-weight:600;">Breathe Out</div>""", unsafe_allow_html=True)
                st.toast("Breathe OUT... 😮‍💨")
                time.sleep(6)
            breathe_placeholder.markdown("""<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#02C39A,#028090);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.2rem;font-weight:600;">Done! 🌿</div>""", unsafe_allow_html=True)
            st.success(f"Great job{', ' + name if st.session_state.user_name else ''}! You completed the breathing exercise! 🌿")
    else:
        meditation_type = st.selectbox("Choose your meditation", [
            "🌿 5 Minute Calm",
            "😴 Sleep Meditation",
            "😰 Anxiety Relief",
            "💙 Self Love",
            "🎯 Focus Meditation",
        ])
        meditations = {
            "🌿 5 Minute Calm": [
                ("Find a comfortable position", "Sit or lie down comfortably. Close your eyes gently. Let your body relax completely. 🌿", 10),
                ("Focus on your breath", "Take a slow deep breath in through your nose for 4 counts. Hold for 2. Breathe out slowly for 6 counts. 🌬️", 15),
                ("Relax your body", "Starting from your toes, slowly relax each part of your body. Feel the tension melting away. 😌", 20),
                ("Visualize a peaceful place", "Imagine yourself in a beautiful peaceful place — a garden, a beach. Feel safe and calm. 🌸", 30),
                ("Return gently", "Slowly bring your awareness back. Wiggle your fingers. Open your eyes when ready. ✨", 10),
            ],
            "😴 Sleep Meditation": [
                ("Lie down comfortably", "Get into your sleeping position. Let your body sink into the bed. 😴", 10),
                ("Slow your breathing", "Breathe in for 4. Hold for 7. Breathe out for 8. This slows your heart rate. 🌙", 20),
                ("Release the day", "Think of one good thing today. Let everything else go. 🌿", 20),
                ("Body scan", "Feel feet relax. Then legs. Stomach. Chest. Arms. Face. Everything soft and heavy. 💤", 30),
                ("Drift to sleep", "You are safe. You are calm. Let your mind go quiet and drift to sleep. 🌙", 15),
            ],
            "😰 Anxiety Relief": [
                ("Acknowledge your feelings", "It is okay to feel anxious. You are safe right now. 💙", 10),
                ("Grounding exercise", "Name 5 things you see. 4 you can touch. 3 you hear. 2 you smell. 1 you taste. 🌿", 30),
                ("Box breathing", "Breathe in 4. Hold 4. Breathe out 4. Hold 4. Repeat. 🌬️", 20),
                ("Positive self talk", "I am safe. I am okay. This feeling will pass. I have gotten through hard things. 💪", 15),
                ("Return to calm", "Feel your body relaxing. The anxiety is passing. You are stronger than your worries. 🌸", 15),
            ],
            "💙 Self Love": [
                ("Settle in", "Sit with your hand on your heart. Take three slow deep breaths. 💙", 10),
                ("Acknowledge yourself", "Think of one thing you did well recently. You deserve to recognize it. 🌟", 15),
                ("Send yourself kindness", "Imagine a warm golden light in your chest growing bigger. This is love for yourself. 💛", 20),
                ("Affirmation", "Say silently — I am enough. I am worthy. I deserve kindness and love. 🌸", 20),
                ("Close with gratitude", "Thank yourself for this time. You matter. Open your eyes slowly. 🌿", 10),
            ],
            "🎯 Focus Meditation": [
                ("Prepare your space", "Sit up straight. Take three deep breaths to signal focus time. 🎯", 10),
                ("Single point focus", "Pick one object and stare gently. When mind wanders bring it back. 👁️", 20),
                ("Breathing anchor", "Use your breath as anchor. Notice thoughts and return to breathing. 🌬️", 20),
                ("Visualize success", "Picture yourself completing your task calmly and well. 🌟", 15),
                ("Ready to focus", "Open eyes slowly. You are calm, clear, and ready. Start now. 🎯", 10),
            ],
        }
        selected_meditation = meditations[meditation_type]
        if st.button("Start Meditation 🧘"):
            for step_num, (title, instruction, duration) in enumerate(selected_meditation):
                st.markdown(f"""
                <div class="card-green">
                    <div style="color:#02C39A; font-weight:600;">Step {step_num+1} — {title}</div>
                    <div style="color:rgba(255,255,255,0.85); margin-top:0.5rem; line-height:1.6;">{instruction}</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(duration)
            st.success(f"You completed the meditation{', ' + name if st.session_state.user_name else ''}! Take a moment to appreciate yourself. 🌿💙")

with tab7:
    st.markdown('<div class="section-header">🎵 Calming Music Player</div>', unsafe_allow_html=True)
    st.caption("Listen to relaxing sounds to feel calm and peaceful.")
    music_options = {
        "🌿 Relaxing Nature Sounds": "https://www.youtube.com/embed/1ZYbU82GVz4",
        "🎹 Calm Piano Music": "https://www.youtube.com/embed/lFcSrYw-ARY",
        "🌊 Peaceful Ocean Waves": "https://www.youtube.com/embed/bn9F19Hi1Lk",
        "☀️ Uplifting Morning Music": "https://www.youtube.com/embed/inpok4MKVLM",
        "🌙 Sleep Music": "https://www.youtube.com/embed/1vx8iUvfyCY",
        "🌧️ Soft Rain Sounds": "https://www.youtube.com/embed/mPZkdNFkNps",
        "🔥 Fireplace Sounds": "https://www.youtube.com/embed/UgHKb_7884o",
        "🎵 Lofi Hip Hop": "https://www.youtube.com/embed/jfKfPfyJRdk",
    }
    selected = st.selectbox("Choose your music", list(music_options.keys()))
    st.markdown(f'<iframe width="100%" height="300" src="{music_options[selected]}?autoplay=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">All Music</div>', unsafe_allow_html=True)
    for title, url in music_options.items():
        with st.expander(title):
            st.markdown(f'<iframe width="100%" height="180" src="{url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)

with tab8:
    st.markdown('<div class="section-header">🎯 Daily Affirmations</div>', unsafe_allow_html=True)
    if st.session_state.affirmation is None:
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
    st.markdown(f'<div class="affirmation-box">{st.session_state.affirmation}</div>', unsafe_allow_html=True)
    if st.button("Give me a new affirmation 🔄"):
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
        st.rerun()
    st.markdown('<div class="section-header">All Affirmations 🌟</div>', unsafe_allow_html=True)
    for affirmation in AFFIRMATIONS:
        st.markdown(f"🌿 {affirmation}")
    st.markdown('<div class="section-header">🌍 Get an AI Quote Just For You</div>', unsafe_allow_html=True)
    st.caption("Tell MindEase how you feel and get a unique quote just for you!")
    feeling = st.text_input("How are you feeling right now?", placeholder="I am feeling stressed about exams...")
    if st.button("Generate My Quote 🌟"):
        if feeling.strip() == "":
            st.warning("Please tell me how you are feeling first!")
        else:
            with st.spinner("Creating your quote..."):
                try:
                    client = Groq(api_key=api_key)
                    quote_prompt = f"""The user's name is {name} and they are feeling: {feeling}.
                    Create one unique, beautiful, meaningful short quote that speaks to how they feel.
                    Write only the quote and author below it.
                    If you make it up write MindEase as the author. One to two sentences maximum."""
                    quote_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "You create beautiful meaningful quotes."},
                                  {"role": "user", "content": quote_prompt}]
                    )
                    generated_quote = quote_response.choices[0].message.content
                    st.markdown(f'<div class="quote-box">{generated_quote}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    st.markdown('<div class="section-header">Classic Quotes 🌟</div>', unsafe_allow_html=True)
    for q, a in QUOTES:
        with st.expander(f"💬 {q[:50]}..."):
            st.markdown(f"*\"{q}\"*")
            st.markdown(f"**— {a}**")

with tab9:
    st.markdown('<div class="section-header">🧠 Mental Health Assessment</div>', unsafe_allow_html=True)
    st.caption("Answer these 8 simple questions honestly. This is NOT a medical diagnosis — just a self check tool.")
    q1 = st.selectbox("1. How often do you feel sad or hopeless?", ["Never", "Sometimes", "Often", "Always"])
    q2 = st.selectbox("2. How often do you feel worried or anxious?", ["Never", "Sometimes", "Often", "Always"])
    q3 = st.selectbox("3. How well are you sleeping?", ["Very Well", "Okay", "Poorly", "Very Poorly"])
    q4 = st.selectbox("4. How often do you feel lonely?", ["Never", "Sometimes", "Often", "Always"])
    q5 = st.selectbox("5. How often do you lose interest in things you enjoy?", ["Never", "Sometimes", "Often", "Always"])
    q6 = st.selectbox("6. How often do you feel tired or have no energy?", ["Never", "Sometimes", "Often", "Always"])
    q7 = st.selectbox("7. How often do you feel angry or irritated?", ["Never", "Sometimes", "Often", "Always"])
    q8 = st.selectbox("8. How often do you feel overwhelmed?", ["Never", "Sometimes", "Often", "Always"])

    def score_answer(answer):
        return {"Never": 0, "Very Well": 0, "Sometimes": 1, "Okay": 1, "Often": 2, "Poorly": 2, "Always": 3, "Very Poorly": 3}.get(answer, 0)

    if st.button("See My Results 🧠"):
        total_score = sum([score_answer(q) for q in [q1, q2, q3, q4, q5, q6, q7, q8]])
        if total_score <= 6:
            level, color, emoji = "Low", "#02C39A", "😊"
            reason = "Your answers show you are generally feeling well with good emotional balance."
            suggestions = ["Keep doing what you are doing! 🌿", "Maintain a regular sleep schedule.", "Stay connected with friends and family.", "Practice daily affirmations."]
            videos = HAPPY_VIDEOS[:2]
        elif total_score <= 14:
            level, color, emoji = "Moderate", "#F4A261", "😐"
            reason = "You are experiencing some stress or emotional difficulty. This is completely normal and with self care you can feel much better."
            suggestions = ["Try the meditation exercise. 🧘", "Write in your journal every day. 📝", "Log your mood daily. 😊", "Get 7 to 8 hours of sleep.", "Talk to someone you trust."]
            videos = HAPPY_VIDEOS[:3]
        else:
            level, color, emoji = "High", "#E63946", "😔"
            reason = "You may be going through a difficult time. Your feelings are valid and you are not alone."
            suggestions = ["Talk to someone you trust right away. 💙", "Use the Chat tab to talk to MindEase. 💬", "Contact a helpline: https://www.iasp.info/resources/Crisis_Centres/", "Try the breathing exercise. 🌬️", "Consider speaking to a professional."]
            videos = HAPPY_VIDEOS
        st.markdown(f'<div class="result-box" style="background:{color}20; border:2px solid {color};">{emoji} {name + ", your" if st.session_state.user_name else "Your"} mental wellness level is <strong>{level}</strong></div>', unsafe_allow_html=True)
        st.markdown("**Why this result?**")
        st.write(reason)
        st.markdown("**What you can do now:**")
        for s in suggestions:
            st.markdown(f"🌿 {s}")
        st.markdown("**Videos to help you feel better 🎥**")
        for title, url in videos:
            st.markdown(f"**{title}**")
            st.markdown(f'<iframe width="100%" height="220" src="{url}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
        st.caption("This is not a medical diagnosis. Please speak to a doctor if you are struggling.")

with tab10:
    st.markdown('<div class="section-header">📈 Progress Report</div>', unsafe_allow_html=True)
    report_period = st.radio("Show report for:", ["Last 7 Days", "Last 30 Days"], horizontal=True)
    days = 7 if report_period == "Last 7 Days" else 30
    st.markdown(f'<div class="section-header">Mood — {report_period}</div>', unsafe_allow_html=True)
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
    st.markdown(f'<div class="section-header">Sleep — {report_period}</div>', unsafe_allow_html=True)
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
                    st.success("Great sleep average! 😴🌟")
                elif avg_sleep >= 6:
                    st.info("Decent sleep. Try to aim for 8 hours! 🌙")
                else:
                    st.warning("You are not sleeping enough. Try to rest more! 😴")
            else:
                st.info(f"No sleep logs in the last {days} days.")
    else:
        st.info("No sleep logs yet.")
    st.markdown(f'<div class="section-header">Journal — {report_period}</div>', unsafe_allow_html=True)
    if os.path.exists("journal_log.csv"):
        df_journal = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
        if not df_journal.empty:
            df_journal["Date"] = pd.to_datetime(df_journal["Date"])
            filtered_journal = df_journal[df_journal["Date"] >= pd.Timestamp.now() - pd.Timedelta(days=days)]
            st.metric("Journal Entries Written", len(filtered_journal))
            if len(filtered_journal) >= 5:
                st.success("Amazing journaling habit! 📝🌟")
            elif len(filtered_journal) >= 1:
                st.info("Good start! Try to journal every day! 📝")
            else:
                st.warning("No journal entries this period. Start writing today! 📝")
    else:
        st.info("No journal entries yet.")
    st.markdown('<div class="section-header">🤖 AI Progress Summary</div>', unsafe_allow_html=True)
    if st.button("Get My AI Summary 🧠"):
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
        with st.spinner("Reviewing your progress..."):
            try:
                client = Groq(api_key=api_key)
                summary_prompt = f"""User name: {name}. Wellness data:
                Mood: {mood_summary}. Sleep: {sleep_summary}. Journal: {journal_summary}.
                Write 3 to 4 warm encouraging sentences using their name {name}.
                Highlight what they are doing well and gently suggest one area to improve."""
                summary_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are MindEase reviewing someone's wellness progress warmly."},
                              {"role": "user", "content": summary_prompt}]
                )
                summary = summary_response.choices[0].message.content
                st.markdown(f'<div class="card-green"><div style="color:white;line-height:1.7;">🌿 {summary}</div></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

with tab11:
    st.markdown('<div class="section-header">📅 Mood Streak</div>', unsafe_allow_html=True)
    st.caption("How many days in a row have you logged your mood?")
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            unique_days = sorted(df["Date"].unique(), reverse=True)
            streak = 0
            today = datetime.now().date()
            for i, day in enumerate(unique_days):
                if day == today - pd.Timedelta(days=i):
                    streak += 1
                else:
                    break
            if streak == 0:
                st.info("No streak yet. Log your mood today! 😊")
            elif streak < 7:
                st.success(f"🔥 {streak} day streak! Keep going{', ' + name if st.session_state.user_name else ''}!")
            elif streak < 30:
                st.success(f"🔥🔥 {streak} day streak! Amazing{', ' + name if st.session_state.user_name else ''}!")
            else:
                st.success(f"🔥🔥🔥 {streak} day streak! You are a champion{', ' + name if st.session_state.user_name else ''}!")
            st.markdown(f"""
            <div style="text-align:center; background:rgba(255,255,255,0.05); border:1px solid rgba(2,195,154,0.3);
            border-radius:20px; padding:2.5rem; margin:1rem 0;">
                <div style="font-size:4rem;">🔥</div>
                <div style="font-size:3rem; font-weight:700; color:#02C39A;">{streak}</div>
                <div style="color:rgba(255,255,255,0.6);">Day Streak</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="section-header">Logging History</div>', unsafe_allow_html=True)
            for day in unique_days[:10]:
                st.markdown(f"✅ {day}")
        else:
            st.info("No mood logs yet!")
    else:
        st.info("No mood logs yet!")

with tab12:
    st.markdown('<div class="section-header">🏆 Wellness Score</div>', unsafe_allow_html=True)
    st.caption("Your overall mental wellness score based on all your logs.")
    score = 0
    breakdown = []
    if os.path.exists("mood_log.csv"):
        df_mood = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df_mood.empty:
            happy_count = len(df_mood[df_mood["Mood"] == "😊 Happy"])
            mood_score = min(int((happy_count / len(df_mood)) * 30), 30)
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
                if day == today - pd.Timedelta(days=i):
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
        color, emoji, message = "#02C39A", "🏆", "Excellent! You are taking amazing care of your mental health!"
    elif score >= 60:
        color, emoji, message = "#F4A261", "😊", "Good job! Keep building your healthy habits!"
    elif score >= 40:
        color, emoji, message = "#E9C46A", "😐", "Not bad! Try logging your mood and sleeping better!"
    else:
        color, emoji, message = "#E63946", "💙", "You are just getting started! Log your mood daily!"
    st.markdown(f"""
    <div style="text-align:center; background:rgba(255,255,255,0.05); border:2px solid {color};
    border-radius:20px; padding:2.5rem; margin:1rem 0;">
        <div style="font-size:3.5rem;">{emoji}</div>
        <div style="font-size:3.5rem; font-weight:700; color:{color};">{score}</div>
        <div style="color:rgba(255,255,255,0.6);">out of 100</div>
        <div style="color:rgba(255,255,255,0.85); margin-top:0.8rem;">{name + ", " + message.lower() if st.session_state.user_name else message}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-header">Score Breakdown</div>', unsafe_allow_html=True)
    for label, s, max_s in breakdown:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(s / max_s)
        with col2:
            st.markdown(f"**{s}/{max_s}**")
        st.caption(label)

with tab13:
    st.markdown('<div class="section-header">🏅 Badges and Rewards</div>', unsafe_allow_html=True)
    st.caption("Earn badges by using MindEase every day!")
    mood_count = sleep_count = journal_count = current_streak = 0
    if os.path.exists("mood_log.csv"):
        df_b = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        mood_count = len(df_b)
        if not df_b.empty:
            df_b["Date"] = pd.to_datetime(df_b["Date"]).dt.date
            unique_days = sorted(df_b["Date"].unique(), reverse=True)
            today = datetime.now().date()
            for i, day in enumerate(unique_days):
                if day == today - pd.Timedelta(days=i):
                    current_streak += 1
                else:
                    break
    if os.path.exists("sleep_log.csv"):
        sleep_count = len(pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"]))
    if os.path.exists("journal_log.csv"):
        journal_count = len(pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"]))
    earned = [b for b in BADGES if b["condition"](mood_count, sleep_count, journal_count, current_streak)]
    not_earned = [b for b in BADGES if not b["condition"](mood_count, sleep_count, journal_count, current_streak)]
    st.markdown(f"""
    <div style="text-align:center; background:rgba(2,195,154,0.1); border:1px solid rgba(2,195,154,0.3);
    border-radius:12px; padding:1rem; margin:0.5rem 0;">
        <div style="font-size:2rem; font-weight:700; color:#02C39A;">{len(earned)} / {len(BADGES)}</div>
        <div style="color:rgba(255,255,255,0.7);">Badges Earned{', ' + name if st.session_state.user_name else ''}</div>
    </div>
    """, unsafe_allow_html=True)
    if earned:
        st.markdown('<div class="section-header">✅ Earned Badges</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, badge in enumerate(earned):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="badge-card">
                    <div style="font-size:1.8rem;">{badge['name'].split()[-1]}</div>
                    <div style="color:#02C39A; font-weight:600; font-size:0.9rem;">{badge['name']}</div>
                    <div style="color:rgba(255,255,255,0.6); font-size:0.75rem; margin-top:0.3rem;">{badge['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
    if not_earned:
        st.markdown('<div class="section-header">🔒 Badges to Earn</div>', unsafe_allow_html=True)
        for badge in not_earned:
            st.markdown(f"""
            <div class="badge-locked">
                🔒 <strong>{badge['name']}</strong> — {badge['desc']}
            </div>
            """, unsafe_allow_html=True)
