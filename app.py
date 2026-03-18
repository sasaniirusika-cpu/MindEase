import streamlit as st
from groq import Groq
from streamlit_option_menu import option_menu
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
.stApp { background: linear-gradient(135deg, #0F0F23 0%, #1A1A2E 50%, #16213E 100%); }
.main-header {
    background: linear-gradient(135deg, #028090, #02C39A);
    padding: 1.5rem 2rem; border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(2,195,154,0.3);
}
.main-title { color: white; font-size: 2rem; font-weight: 700; margin: 0; }
.main-subtitle { color: rgba(255,255,255,0.85); font-size: 0.95rem; margin: 0.3rem 0 0 0; }
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px; padding: 1.5rem; margin: 0.8rem 0;
}
.card-green {
    background: rgba(2,195,154,0.1);
    border: 1px solid rgba(2,195,154,0.3);
    border-radius: 16px; padding: 1.5rem; margin: 0.8rem 0;
}
.section-header {
    color: #02C39A; font-size: 1.1rem; font-weight: 600;
    margin: 1.5rem 0 0.8rem 0; padding-bottom: 0.4rem;
    border-bottom: 2px solid rgba(2,195,154,0.3);
}
.affirmation-box {
    background: linear-gradient(135deg, rgba(2,195,154,0.15), rgba(2,128,144,0.15));
    border: 1px solid rgba(2,195,154,0.4);
    border-radius: 16px; padding: 2rem; text-align: center;
    font-size: 1.2rem; color: white; line-height: 1.7; margin: 1rem 0;
}
.quote-box {
    background: rgba(255,255,255,0.05);
    border-left: 4px solid #02C39A;
    border-radius: 0 12px 12px 0;
    padding: 1.5rem 2rem; margin: 1rem 0;
    font-style: italic; color: rgba(255,255,255,0.9);
    font-size: 1.1rem; line-height: 1.7;
}
.result-box {
    border-radius: 16px; padding: 1.5rem;
    text-align: center; font-size: 1.1rem;
    font-weight: 600; margin: 1rem 0;
}
.badge-card {
    background: rgba(2,195,154,0.1);
    border: 2px solid rgba(2,195,154,0.4);
    border-radius: 12px; padding: 1rem;
    text-align: center; margin: 0.4rem;
}
.badge-locked {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px; padding: 0.8rem;
    margin: 0.3rem 0; opacity: 0.6;
}
.goodnight-box {
    background: linear-gradient(135deg, rgba(155,114,207,0.15), rgba(2,128,144,0.15));
    border: 1px solid rgba(155,114,207,0.4);
    border-radius: 16px; padding: 1.5rem;
    color: white; line-height: 1.7; margin: 1rem 0;
}
.morning-box {
    background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,165,0,0.1));
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 16px; padding: 1.5rem;
    color: white; line-height: 1.7; margin: 1rem 0;
}
.music-player {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: linear-gradient(135deg, #0D1117, #161B22);
    border-top: 1px solid rgba(2,195,154,0.3);
    padding: 0.8rem 2rem; z-index: 1000;
    display: flex; align-items: center; gap: 1rem;
}
div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 2px solid rgba(2,195,154,0.5) !important;
    background: rgba(255,255,255,0.05) !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #02C39A !important;
    box-shadow: 0 0 0 3px rgba(2,195,154,0.2) !important;
}
div[data-testid="stChatInput"] textarea { color: white !important; }
div[data-testid="stChatInput"] textarea::placeholder { color: rgba(255,255,255,0.4) !important; }
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    border-radius: 50% !important;
}
.stButton > button {
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 500 !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(2,195,154,0.4) !important;
}
h1, h2, h3, h4 { color: white !important; }
p, li { color: rgba(255,255,255,0.85) !important; }
label { color: rgba(255,255,255,0.8) !important; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1117 0%, #161B22 100%) !important;
}
section[data-testid="stSidebar"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)

api_key = st.secrets["GROQ_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []
if "affirmation" not in st.session_state:
    st.session_state.affirmation = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = ""
if "profile_set" not in st.session_state:
    st.session_state.profile_set = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "💬 Chat"
if "music_playing" not in st.session_state:
    st.session_state.music_playing = False
if "selected_music" not in st.session_state:
    st.session_state.selected_music = None
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

MUSIC_OPTIONS = {
    "🌿 Nature Sounds": "https://www.youtube.com/embed/1ZYbU82GVz4",
    "🎹 Piano Music": "https://www.youtube.com/embed/lFcSrYw-ARY",
    "🌊 Ocean Waves": "https://www.youtube.com/embed/bn9F19Hi1Lk",
    "🌧️ Rain Sounds": "https://www.youtube.com/embed/mPZkdNFkNps",
    "🔥 Fireplace": "https://www.youtube.com/embed/UgHKb_7884o",
    "🎵 Lofi Hip Hop": "https://www.youtube.com/embed/jfKfPfyJRdk",
    "🌙 Sleep Music": "https://www.youtube.com/embed/1vx8iUvfyCY",
    "☀️ Morning Music": "https://www.youtube.com/embed/inpok4MKVLM",
}

MOOD_COLORS = {
    "😊 Happy": {"color": "#FFD700", "bg": "#FFD70020", "label": "Golden Joy", "message": "You are glowing today! Keep that beautiful energy! 🌟"},
    "😐 Okay": {"color": "#87CEEB", "bg": "#87CEEB20", "label": "Calm Blue", "message": "A steady calm day. That is perfectly fine! 🌤️"},
    "😔 Sad": {"color": "#6495ED", "bg": "#6495ED20", "label": "Deep Blue", "message": "It is okay to feel sad. Be gentle with yourself today. 💙"},
    "😰 Stressed": {"color": "#FF6B6B", "bg": "#FF6B6B20", "label": "Warm Red", "message": "Take a deep breath. You can get through this! 🌬️"},
    "😡 Angry": {"color": "#FF4500", "bg": "#FF450020", "label": "Fiery Orange", "message": "Your feelings are valid. Try the breathing exercise to cool down. 🌿"},
}

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
    ("You don't have to be positive all the time. It's perfectly okay to feel sad, angry, or anxious.", "Lori Deschene"),
    ("Self-care is not self-indulgence, it is self-preservation.", "Audre Lorde"),
    ("Healing is not linear.", "Unknown"),
    ("Be gentle with yourself. You are a child of the universe.", "Max Ehrmann"),
    ("You are braver than you believe, stronger than you seem.", "A.A. Milne"),
    ("You matter. You are enough. You are loved.", "Unknown"),
]

HAPPY_VIDEOS = [
    ("Relaxing Nature Sounds 🌿", "https://www.youtube.com/embed/1ZYbU82GVz4"),
    ("Calm Piano Music 🎵", "https://www.youtube.com/embed/lFcSrYw-ARY"),
    ("Funny Animals 😄", "https://www.youtube.com/embed/WYkiiGnOyBw"),
    ("Ocean Waves 🌊", "https://www.youtube.com/embed/bn9F19Hi1Lk"),
    ("Uplifting Morning ☀️", "https://www.youtube.com/embed/inpok4MKVLM"),
]

BADGES = [
    {"name": "First Step 🌱", "desc": "Logged your first mood", "condition": lambda m, s, j, st: m >= 1},
    {"name": "Mood Tracker 😊", "desc": "Logged mood 5 times", "condition": lambda m, s, j, st: m >= 5},
    {"name": "Consistent Soul 🌟", "desc": "Logged mood 10 times", "condition": lambda m, s, j, st: m >= 10},
    {"name": "Sleep Logger 😴", "desc": "Logged your first sleep", "condition": lambda m, s, j, st: s >= 1},
    {"name": "Dear Diary 📝", "desc": "Wrote your first journal entry", "condition": lambda m, s, j, st: j >= 1},
    {"name": "Storyteller ✍️", "desc": "Wrote 5 journal entries", "condition": lambda m, s, j, st: j >= 5},
    {"name": "3 Day Streak 🔥", "desc": "Logged mood 3 days in a row", "condition": lambda m, s, j, st: st >= 3},
    {"name": "Week Warrior 🏆", "desc": "Logged mood 7 days in a row", "condition": lambda m, s, j, st: st >= 7},
    {"name": "MindEase Champion 👑", "desc": "Logged mood 30 days in a row", "condition": lambda m, s, j, st: st >= 30},
]

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 0.5rem 0;">
        <div style="font-size:2.5rem;">🌿</div>
        <div style="font-size:1.3rem; font-weight:700; color:white;">MindEase</div>
        <div style="font-size:0.75rem; color:rgba(255,255,255,0.5);">Your wellness companion</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 👤 Profile")
    user_name = st.text_input("Name", value=st.session_state.user_name, placeholder="Your name...")
    user_age = st.text_input("Age", value=st.session_state.user_age, placeholder="Your age...")
    if st.button("Save Profile ✅"):
        st.session_state.user_name = user_name
        st.session_state.user_age = user_age
        st.session_state.profile_set = True
        st.success(f"Welcome, {user_name}! 🌿")
        st.rerun()

    if st.session_state.profile_set and st.session_state.user_name:
        st.markdown(f"""
        <div style="background:rgba(2,195,154,0.1); border:1px solid rgba(2,195,154,0.3);
        border-radius:10px; padding:0.8rem; text-align:center; margin:0.5rem 0;">
            <div style="font-size:1.5rem;">😊</div>
            <div style="font-weight:600; color:white;">{st.session_state.user_name}</div>
            <div style="font-size:0.75rem; color:rgba(255,255,255,0.5);">Age: {st.session_state.user_age}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    selected = option_menu(
        menu_title=None,
        options=["💬 Chat", "😊 Mood", "📝 Journal", "🌅 Daily Wellness",
                 "🧘 Meditation", "🎯 Affirmations", "🧠 Assessment",
                 "🏆 Achievements", "📈 Progress"],
        icons=["chat-dots", "emoji-smile", "journal", "sun",
               "peace", "stars", "brain",
               "trophy", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0", "background": "transparent"},
            "icon": {"color": "#02C39A", "font-size": "14px"},
            "nav-link": {
                "font-size": "13px", "color": "rgba(255,255,255,0.7)",
                "padding": "8px 12px", "border-radius": "8px",
                "margin": "2px 0",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #028090, #02C39A)",
                "color": "white", "font-weight": "600",
            },
        }
    )

    st.divider()
    st.markdown("### 🎵 Music Player")
    music_choice = st.selectbox("Choose music", ["None"] + list(MUSIC_OPTIONS.keys()), label_visibility="collapsed")
    col_play, col_stop = st.columns(2)
    with col_play:
        if st.button("▶️ Play"):
            if music_choice != "None":
                st.session_state.music_playing = True
                st.session_state.selected_music = music_choice
                st.rerun()
    with col_stop:
        if st.button("⏹️ Stop"):
            st.session_state.music_playing = False
            st.session_state.selected_music = None
            st.rerun()
    if st.session_state.music_playing and st.session_state.selected_music:
        st.markdown(f"🎵 *Playing: {st.session_state.selected_music}*")

    st.divider()
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("### 🕐 Chat History")
    if os.path.exists("chat_history.csv"):
        df_side = pd.read_csv("chat_history.csv", names=["Date", "Name", "You", "MindEase"])
        if not df_side.empty:
            for _, row in df_side.iloc[::-1].head(10).iterrows():
                with st.expander(f"💬 {str(row['You'])[:25]}..."):
                    st.caption(row['Date'])
                    st.markdown(f"**You:** {row['You']}")
                    st.markdown(f"**MindEase:** {row['MindEase']}")
        else:
            st.caption("No history yet!")
    else:
        st.caption("No history yet!")

if st.session_state.music_playing and st.session_state.selected_music:
    music_url = MUSIC_OPTIONS[st.session_state.selected_music]
    st.markdown(f"""
    <div style="position:fixed; bottom:0; left:0; right:0;
    background:linear-gradient(135deg,#0D1117,#161B22);
    border-top:1px solid rgba(2,195,154,0.3);
    padding:0.5rem 1rem; z-index:1000; display:flex; align-items:center; gap:1rem;">
        <span style="color:#02C39A; font-size:1.2rem;">🎵</span>
        <span style="color:white; font-size:0.9rem;">Now Playing: {st.session_state.selected_music}</span>
        <iframe src="{music_url}?autoplay=1" width="0" height="0" frameborder="0" allow="autoplay"></iframe>
    </div>
    """, unsafe_allow_html=True)

name = st.session_state.user_name if st.session_state.user_name else "friend"
age = st.session_state.user_age if st.session_state.user_age else ""

SYSTEM_PROMPT = f"""You are MindEase, a very close and caring best friend.
The user's name is {name}.{"They are " + age + " years old." if age else ""}
Always call them by their name — {name}.
Be warm, gentle, empathetic. Talk like a real close friend — casual, kind, natural.
Always acknowledge feelings first. Ask one gentle question at a time.
Keep responses short and warm like a text from a close friend.
If user mentions self-harm share: https://www.iasp.info/resources/Crisis_Centres/
Never diagnose. Never say you are an AI unless asked."""

st.markdown(f"""
<div class="main-header">
    <div class="main-title">🌿 MindEase</div>
    <div class="main-subtitle">{"Welcome back, " + name + "! Your wellness companion is here. 💙" if st.session_state.user_name else "Your personal AI companion for mental wellness"}</div>
</div>
""", unsafe_allow_html=True)

if selected == "💬 Chat":
    if not st.session_state.user_name:
        st.info("👤 Please enter your name in the sidebar for a personalized experience!")
    chat_container = st.container(height=500)
    with chat_container:
        if len(st.session_state.messages) == 0:
            with st.chat_message("assistant", avatar="🌿"):
                welcome = f"Hi {name}! 😊 I am MindEase. I am here for you anytime. How are you feeling today?" if st.session_state.user_name else "Hi there! 😊 Enter your name in the sidebar so I can get to know you! How are you feeling?"
                st.markdown(welcome)
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🌿" if message["role"] == "assistant" else "🧑"):
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

elif selected == "😊 Mood":
    st.markdown(f'<div class="section-header">😊 How are you feeling today{", " + name if st.session_state.user_name else ""}?</div>', unsafe_allow_html=True)
    mood = st.radio("Select your mood:", list(MOOD_COLORS.keys()), horizontal=True)
    note = st.text_input("Add a note (optional)", placeholder="What is making you feel this way?")
    mood_data = MOOD_COLORS[mood]
    st.markdown(f"""
    <div style="text-align:center; background:{mood_data['bg']}; border:2px solid {mood_data['color']};
    border-radius:16px; padding:2rem; margin:1rem 0;">
        <div style="font-size:3rem;">{mood}</div>
        <div style="font-size:1.3rem; font-weight:600; color:{mood_data['color']}; margin:0.5rem 0;">{mood_data['label']}</div>
        <div style="width:60px; height:60px; border-radius:50%; background:{mood_data['color']}; margin:0.8rem auto;"></div>
        <div style="color:rgba(255,255,255,0.85);">{mood_data['message']}</div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save My Mood"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("mood_log.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([now, mood, note])
            st.success(f"Mood saved{', ' + name if st.session_state.user_name else ''}! 🌿")
    with col2:
        if st.button("💬 Get Personal Message"):
            with st.spinner("MindEase is thinking..."):
                try:
                    client = Groq(api_key=api_key)
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are MindEase, a warm caring best friend."},
                            {"role": "user", "content": f"The user {name} is feeling {mood}. Write a warm personal 3-4 sentence message using their name."}
                        ]
                    )
                    st.markdown(f'<div class="card-green" style="color:white;">🌿 {response.choices[0].message.content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    st.markdown('<div class="section-header">📊 Mood History</div>', unsafe_allow_html=True)
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df.empty:
            if st.button("🗑️ Delete All Mood Logs"):
                os.remove("mood_log.csv")
                st.rerun()
            st.dataframe(df, use_container_width=True)
            mood_counts = df["Mood"].value_counts().reset_index()
            mood_counts.columns = ["Mood", "Count"]
            st.bar_chart(mood_counts.set_index("Mood"))
    else:
        st.info("No mood logs yet!")

elif selected == "📝 Journal":
    st.markdown(f'<div class="section-header">📝 Journal{" — " + name if st.session_state.user_name else ""}</div>', unsafe_allow_html=True)
    st.caption("Your private space. Write anything you feel.")
    journal_title = st.text_input("Title", placeholder="My thoughts today...")
    journal_entry = st.text_area("Write here...", height=200, placeholder="Today I felt...")
    if st.button("💾 Save Journal Entry"):
        if journal_entry.strip() == "":
            st.warning("Please write something first!")
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("journal_log.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([now, journal_title, journal_entry])
            st.success("Journal saved! Writing is healing. 🌿")
    st.markdown('<div class="section-header">📖 Past Entries</div>', unsafe_allow_html=True)
    if os.path.exists("journal_log.csv"):
        df_j = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
        if not df_j.empty:
            if st.button("🗑️ Delete All Entries"):
                os.remove("journal_log.csv")
                st.rerun()
            for _, row in df_j.iterrows():
                with st.expander(f"📝 {row['Date']} — {row['Title']}"):
                    st.write(row["Entry"])
    else:
        st.info("No journal entries yet!")

elif selected == "🌅 Daily Wellness":
    hour = datetime.now().hour
    is_morning = 5 <= hour < 12
    is_evening = 17 <= hour <= 23

    if is_morning:
        st.markdown(f"""
        <div class="morning-box">
            <div style="font-size:1.8rem; margin-bottom:0.5rem;">🌅 Good Morning{", " + name if st.session_state.user_name else ""}!</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Morning Greeting 🌅"):
            with st.spinner("Preparing your morning..."):
                try:
                    client = Groq(api_key=api_key)
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are MindEase, a warm caring best friend."},
                            {"role": "user", "content": f"Write a warm, energetic good morning message for {name}. Include one motivational thought for the day. 3 sentences max."}
                        ]
                    )
                    st.markdown(f'<div class="morning-box">🌅 {response.choices[0].message.content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")

        st.markdown('<div class="section-header">😊 Morning Mood</div>', unsafe_allow_html=True)
        morning_mood = st.radio("How are you feeling this morning?", list(MOOD_COLORS.keys()), horizontal=True)

        st.markdown('<div class="section-header">✅ Things To Do Today</div>', unsafe_allow_html=True)
        new_task = st.text_input("Add a task", placeholder="What do you need to do today?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Task"):
                if new_task.strip():
                    st.session_state.todo_list.append({"task": new_task, "done": False})
                    st.rerun()
        with col2:
            if st.button("🗑️ Clear All Tasks"):
                st.session_state.todo_list = []
                st.rerun()

        if st.session_state.todo_list:
            for i, item in enumerate(st.session_state.todo_list):
                col_check, col_task = st.columns([1, 10])
                with col_check:
                    done = st.checkbox("", value=item["done"], key=f"todo_{i}")
                    st.session_state.todo_list[i]["done"] = done
                with col_task:
                    if item["done"]:
                        st.markdown(f"~~{item['task']}~~")
                    else:
                        st.markdown(item["task"])

        if st.button("💡 AI Task Suggestions"):
            with st.spinner("Getting suggestions..."):
                try:
                    client = Groq(api_key=api_key)
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are MindEase, a caring wellness companion."},
                            {"role": "user", "content": f"{name} is feeling {morning_mood} this morning. Suggest 3 small helpful tasks or self care activities they can do today based on their mood. Keep it simple and warm."}
                        ]
                    )
                    st.markdown(f'<div class="card-green" style="color:white;">💡 {response.choices[0].message.content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")

        if st.button("💾 Save Morning Check In"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("mood_log.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([now, morning_mood, "Morning check in"])
            st.success(f"Morning saved{', ' + name if st.session_state.user_name else ''}! Have a wonderful day! 🌅")

    elif is_evening:
        st.markdown(f"""
        <div class="goodnight-box">
            <div style="font-size:1.8rem; margin-bottom:0.5rem;">🌙 Good Evening{", " + name if st.session_state.user_name else ""}!</div>
            <div style="color:rgba(255,255,255,0.8);">Time to wind down and reflect on your day.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">😴 Sleep Log</div>', unsafe_allow_html=True)
        sleep_hours = st.slider("How many hours did you sleep last night?", 0, 12, 7)
        sleep_quality = st.radio("Sleep quality:", ["😴 Very Good", "🙂 Good", "😐 Okay", "😔 Poor", "😫 Very Poor"], horizontal=True)

        st.markdown('<div class="section-header">💧 Water Intake</div>', unsafe_allow_html=True)
        water_glasses = st.slider("How many glasses of water did you drink today?", 0, 15, 8)
        if water_glasses < 6:
            st.warning("You did not drink enough water today. Try to drink at least 8 glasses tomorrow! 💧")
        elif water_glasses >= 8:
            st.success("Great hydration today! 💧🌟")
        else:
            st.info("Good but try to drink a little more tomorrow! 💧")

        st.markdown('<div class="section-header">🌙 Night Check In</div>', unsafe_allow_html=True)
        day_rating = st.slider("How was your day overall?", 1, 10, 5)
        day_highlight = st.text_input("Best part of your day?", placeholder="Something good that happened...")
        day_challenge = st.text_input("Hardest part of your day?", placeholder="Something difficult today...")
        grateful_for = st.text_area("3 things you are grateful for today", placeholder="1. \n2. \n3. ", height=100)
        tomorrow_goal = st.text_input("One small goal for tomorrow?", placeholder="Something small and achievable...")

        if st.button("🌙 Save & Get Goodnight Message"):
            if day_highlight.strip() == "" and grateful_for.strip() == "":
                st.warning("Please fill in at least some fields!")
            else:
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                with open("night_checkin.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([now, day_rating, day_highlight, day_challenge, grateful_for, tomorrow_goal, sleep_hours, water_glasses])
                with open("sleep_log.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([now, sleep_hours, sleep_quality, "From night check in"])
                st.success("Night check in saved! 🌙")

                with st.spinner("MindEase is preparing your goodnight message..."):
                    try:
                        client = Groq(api_key=api_key)
                        night_prompt = f"""User name: {name}. Night check in data:
                        Day rating: {day_rating}/10. Best part: {day_highlight}.
                        Hardest part: {day_challenge}. Grateful for: {grateful_for}.
                        Tomorrow goal: {tomorrow_goal}. Sleep last night: {sleep_hours} hours.
                        Water today: {water_glasses} glasses.

                        Write THREE separate sections:

                        1. GOODNIGHT MESSAGE: A warm personal goodnight message using {name}'s name. 2-3 sentences.

                        2. TODAY'S SUMMARY: A short paragraph summarizing how their day went based on the data. Mention the good and the hard parts warmly. 3-4 sentences.

                        3. TOMORROW'S TIPS: Based on their data, give 3 specific personal tips to make tomorrow better. Include advice on any bad habits to remove and good habits to build. Use their name {name}. Keep it warm and friendly.

                        Format exactly like this:
                        🌙 GOODNIGHT: [message]
                        📋 TODAY: [summary]
                        💡 TOMORROW: [tips]"""

                        night_response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "You are MindEase, a warm caring best friend giving a goodnight message."},
                                {"role": "user", "content": night_prompt}
                            ]
                        )
                        goodnight_message = night_response.choices[0].message.content
                        st.markdown(f'<div class="goodnight-box">{goodnight_message}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Something went wrong: {str(e)}")

        st.markdown('<div class="section-header">📖 Past Night Check Ins</div>', unsafe_allow_html=True)
        if os.path.exists("night_checkin.csv"):
            df_night = pd.read_csv("night_checkin.csv", names=["Date", "Rating", "Highlight", "Challenge", "Grateful", "Goal", "Sleep", "Water"])
            if not df_night.empty:
                if st.button("🗑️ Delete All Night Check Ins"):
                    os.remove("night_checkin.csv")
                    st.rerun()
                for _, row in df_night.iloc[::-1].iterrows():
                    with st.expander(f"🌙 {row['Date']} — Day rated {row['Rating']}/10"):
                        st.markdown(f"**Best part:** {row['Highlight']}")
                        st.markdown(f"**Hardest part:** {row['Challenge']}")
                        st.markdown(f"**Grateful for:** {row['Grateful']}")
                        st.markdown(f"**Tomorrow goal:** {row['Goal']}")
                        st.markdown(f"**Sleep:** {row['Sleep']} hours | **Water:** {row['Water']} glasses")
        else:
            st.info("No night check ins yet!")
    else:
        st.markdown(f"""
        <div class="card">
            <div style="text-align:center; padding:2rem;">
                <div style="font-size:3rem;">🌤️</div>
                <div style="font-size:1.3rem; font-weight:600; color:white; margin:1rem 0;">
                    Good Afternoon{", " + name if st.session_state.user_name else ""}!
                </div>
                <div style="color:rgba(255,255,255,0.7);">
                    Morning check in is available from 5 AM to 12 PM 🌅<br>
                    Evening check in is available from 5 PM to 11 PM 🌙
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif selected == "🧘 Meditation":
    st.markdown('<div class="section-header">🧘 Meditation and Breathing</div>', unsafe_allow_html=True)
    exercise_type = st.radio("What do you want to do?", ["🌬️ Breathing Exercise", "🧘 Guided Meditation"], horizontal=True)
    if exercise_type == "🌬️ Breathing Exercise":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            breathe_placeholder = st.empty()
        rounds = st.slider("How many rounds?", 1, 5, 3)
        if st.button("Start Breathing Exercise 🌬️"):
            for i in range(rounds):
                st.markdown(f"**Round {i+1} of {rounds}**")
                breathe_placeholder.markdown('<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#02C39A,#028090);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.3rem;font-weight:600;">Breathe In</div>', unsafe_allow_html=True)
                st.toast("Breathe IN... 🌬️")
                time.sleep(4)
                breathe_placeholder.markdown('<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#9B72CF,#028090);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.3rem;font-weight:600;">Hold</div>', unsafe_allow_html=True)
                st.toast("HOLD... ⏸️")
                time.sleep(4)
                breathe_placeholder.markdown('<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#028090,#1A1A2E);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.3rem;font-weight:600;">Breathe Out</div>', unsafe_allow_html=True)
                st.toast("Breathe OUT... 😮‍💨")
                time.sleep(6)
            breathe_placeholder.markdown('<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#02C39A,#028090);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.2rem;font-weight:600;">Done! 🌿</div>', unsafe_allow_html=True)
            st.success(f"Great job{', ' + name if st.session_state.user_name else ''}! 🌿")
    else:
        meditation_type = st.selectbox("Choose your meditation", [
            "🌿 5 Minute Calm", "😴 Sleep Meditation",
            "😰 Anxiety Relief", "💙 Self Love", "🎯 Focus Meditation"
        ])
        meditations = {
            "🌿 5 Minute Calm": [
                ("Find a comfortable position", "Sit or lie down comfortably. Close your eyes. Relax completely. 🌿", 10),
                ("Focus on your breath", "Breathe in for 4 counts. Hold for 2. Breathe out for 6. 🌬️", 15),
                ("Relax your body", "From your toes up, relax each part of your body. 😌", 20),
                ("Peaceful place", "Imagine a beautiful peaceful place where you feel safe. 🌸", 30),
                ("Return gently", "Bring awareness back. Wiggle fingers. Open eyes when ready. ✨", 10),
            ],
            "😴 Sleep Meditation": [
                ("Lie down", "Get into sleeping position. Let body sink into the bed. 😴", 10),
                ("Slow breathing", "Breathe in 4. Hold 7. Out 8. Slows heart rate. 🌙", 20),
                ("Release the day", "Think of one good thing. Let everything else go. 🌿", 20),
                ("Body scan", "Feet relax. Legs. Stomach. Chest. Arms. Face. All soft. 💤", 30),
                ("Drift off", "You are safe. You are calm. Drift gently to sleep. 🌙", 15),
            ],
            "😰 Anxiety Relief": [
                ("Acknowledge feelings", "It is okay to feel anxious. You are safe right now. 💙", 10),
                ("Grounding", "5 things you see. 4 touch. 3 hear. 2 smell. 1 taste. 🌿", 30),
                ("Box breathing", "In 4. Hold 4. Out 4. Hold 4. Repeat. 🌬️", 20),
                ("Self talk", "I am safe. I am okay. This will pass. I am strong. 💪", 15),
                ("Calm", "Feel body relaxing. Anxiety is passing. You are stronger. 🌸", 15),
            ],
            "💙 Self Love": [
                ("Settle in", "Hand on heart. Three slow deep breaths. 💙", 10),
                ("Acknowledge yourself", "Think of one thing you did well. You deserve credit. 🌟", 15),
                ("Warm light", "Imagine warm golden light in your chest growing bigger. 💛", 20),
                ("Affirmation", "I am enough. I am worthy. I deserve love and kindness. 🌸", 20),
                ("Gratitude", "Thank yourself for this time. You matter. 🌿", 10),
            ],
            "🎯 Focus Meditation": [
                ("Prepare", "Sit up straight. Three deep breaths. Time to focus. 🎯", 10),
                ("Single focus", "Pick one object. Stare gently. Bring mind back when it wanders. 👁️", 20),
                ("Breath anchor", "Use breath as anchor. Notice thoughts. Return to breathing. 🌬️", 20),
                ("Visualize", "See yourself completing your task calmly and well. 🌟", 15),
                ("Ready", "Open eyes. You are calm, clear, ready to focus. 🎯", 10),
            ],
        }
        if st.button("Start Meditation 🧘"):
            for step_num, (title, instruction, duration) in enumerate(meditations[meditation_type]):
                st.markdown(f'<div class="card-green"><div style="color:#02C39A;font-weight:600;">Step {step_num+1} — {title}</div><div style="color:rgba(255,255,255,0.85);margin-top:0.5rem;">{instruction}</div></div>', unsafe_allow_html=True)
                time.sleep(duration)
            st.success(f"Meditation complete{', ' + name if st.session_state.user_name else ''}! 🌿💙")

elif selected == "🎯 Affirmations":
    st.markdown('<div class="section-header">🎯 Daily Affirmations</div>', unsafe_allow_html=True)
    if st.session_state.affirmation is None:
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
    st.markdown(f'<div class="affirmation-box">{st.session_state.affirmation}</div>', unsafe_allow_html=True)
    if st.button("New Affirmation 🔄"):
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
        st.rerun()
    st.markdown('<div class="section-header">All Affirmations 🌟</div>', unsafe_allow_html=True)
    for a in AFFIRMATIONS:
        st.markdown(f"🌿 {a}")
    st.markdown('<div class="section-header">🌍 AI Quote Just For You</div>', unsafe_allow_html=True)
    feeling = st.text_input("How are you feeling right now?", placeholder="I am feeling stressed...")
    if st.button("Generate My Quote 🌟"):
        if feeling.strip() == "":
            st.warning("Please tell me how you are feeling first!")
        else:
            with st.spinner("Creating your quote..."):
                try:
                    client = Groq(api_key=api_key)
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You create beautiful meaningful quotes."},
                            {"role": "user", "content": f"{name} is feeling: {feeling}. Create one unique beautiful short quote. Write quote then author. MindEase as author if you made it up."}
                        ]
                    )
                    st.markdown(f'<div class="quote-box">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
    st.markdown('<div class="section-header">Classic Quotes</div>', unsafe_allow_html=True)
    for q, a in QUOTES:
        with st.expander(f"💬 {q[:50]}..."):
            st.markdown(f"*\"{q}\"*")
            st.markdown(f"**— {a}**")

elif selected == "🧠 Assessment":
    st.markdown('<div class="section-header">🧠 Mental Health Assessment</div>', unsafe_allow_html=True)
    st.caption("Answer these 8 questions honestly. This is NOT a medical diagnosis.")
    q1 = st.selectbox("1. How often do you feel sad or hopeless?", ["Never", "Sometimes", "Often", "Always"])
    q2 = st.selectbox("2. How often do you feel worried or anxious?", ["Never", "Sometimes", "Often", "Always"])
    q3 = st.selectbox("3. How well are you sleeping?", ["Very Well", "Okay", "Poorly", "Very Poorly"])
    q4 = st.selectbox("4. How often do you feel lonely?", ["Never", "Sometimes", "Often", "Always"])
    q5 = st.selectbox("5. How often do you lose interest in things you enjoy?", ["Never", "Sometimes", "Often", "Always"])
    q6 = st.selectbox("6. How often do you feel tired or have no energy?", ["Never", "Sometimes", "Often", "Always"])
    q7 = st.selectbox("7. How often do you feel angry or irritated?", ["Never", "Sometimes", "Often", "Always"])
    q8 = st.selectbox("8. How often do you feel overwhelmed?", ["Never", "Sometimes", "Often", "Always"])
    score_map = {"Never": 0, "Very Well": 0, "Sometimes": 1, "Okay": 1, "Often": 2, "Poorly": 2, "Always": 3, "Very Poorly": 3}
    if st.button("See My Results 🧠"):
        total = sum([score_map.get(q, 0) for q in [q1, q2, q3, q4, q5, q6, q7, q8]])
        if total <= 6:
            level, color, emoji = "Low", "#02C39A", "😊"
            reason = "You are generally feeling well with good emotional balance."
            suggestions = ["Keep doing what you are doing! 🌿", "Maintain regular sleep.", "Stay connected with loved ones.", "Practice daily affirmations."]
            videos = HAPPY_VIDEOS[:2]
        elif total <= 14:
            level, color, emoji = "Moderate", "#F4A261", "😐"
            reason = "You are experiencing some stress. With self care you can feel much better."
            suggestions = ["Try meditation. 🧘", "Journal every day. 📝", "Log your mood daily. 😊", "Get 7-8 hours sleep.", "Talk to someone you trust."]
            videos = HAPPY_VIDEOS[:3]
        else:
            level, color, emoji = "High", "#E63946", "😔"
            reason = "You may be going through a difficult time. You are not alone."
            suggestions = ["Talk to someone you trust. 💙", "Chat with MindEase. 💬", "Helpline: https://www.iasp.info/resources/Crisis_Centres/", "Try breathing exercise. 🌬️", "Consider professional help."]
            videos = HAPPY_VIDEOS
        st.markdown(f'<div class="result-box" style="background:{color}20;border:2px solid {color};">{emoji} {name + ", your" if st.session_state.user_name else "Your"} wellness level is <strong>{level}</strong></div>', unsafe_allow_html=True)
        st.markdown(f"**Why?** {reason}")
        st.markdown("**What to do now:**")
        for s in suggestions:
            st.markdown(f"🌿 {s}")
        st.markdown("**Videos to help 🎥**")
        for title, url in videos:
            st.markdown(f"**{title}**")
            st.markdown(f'<iframe width="100%" height="200" src="{url}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
        st.caption("Not a medical diagnosis. See a doctor if struggling.")

elif selected == "🏆 Achievements":
    st.markdown(f'<div class="section-header">🏆 Your Achievements{", " + name if st.session_state.user_name else ""}</div>', unsafe_allow_html=True)

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
        df_sl = pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"])
        if not df_sl.empty:
            avg_sleep = df_sl["Hours"].mean()
            sleep_score = 25 if avg_sleep >= 8 else 15 if avg_sleep >= 6 else 5
            score += sleep_score
            breakdown.append(("😴 Sleep Score", sleep_score, 25))
        else:
            breakdown.append(("😴 Sleep Score", 0, 25))
    else:
        breakdown.append(("😴 Sleep Score", 0, 25))
    if os.path.exists("journal_log.csv"):
        df_jl = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
        journal_score = min(len(df_jl) * 5, 25)
        score += journal_score
        breakdown.append(("📝 Journal Score", journal_score, 25))
    else:
        breakdown.append(("📝 Journal Score", 0, 25))
    streak_score = min(current_streak * 2, 20)
    score += streak_score
    breakdown.append(("📅 Streak Score", streak_score, 20))

    col1, col2, col3 = st.columns(3)
    with col1:
        if score >= 80:
            color, emoji = "#02C39A", "🏆"
        elif score >= 60:
            color, emoji = "#F4A261", "😊"
        elif score >= 40:
            color, emoji = "#E9C46A", "😐"
        else:
            color, emoji = "#E63946", "💙"
        st.markdown(f"""
        <div style="text-align:center; background:rgba(255,255,255,0.05); border:2px solid {color};
        border-radius:16px; padding:1.5rem;">
            <div style="font-size:2.5rem;">{emoji}</div>
            <div style="font-size:2.5rem; font-weight:700; color:{color};">{score}</div>
            <div style="color:rgba(255,255,255,0.6); font-size:0.85rem;">Wellness Score / 100</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align:center; background:rgba(255,255,255,0.05); border:1px solid rgba(2,195,154,0.3);
        border-radius:16px; padding:1.5rem;">
            <div style="font-size:2.5rem;">🔥</div>
            <div style="font-size:2.5rem; font-weight:700; color:#02C39A;">{current_streak}</div>
            <div style="color:rgba(255,255,255,0.6); font-size:0.85rem;">Day Streak</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        earned_count = len([b for b in BADGES if b["condition"](mood_count, sleep_count, journal_count, current_streak)])
        st.markdown(f"""
        <div style="text-align:center; background:rgba(255,255,255,0.05); border:1px solid rgba(2,195,154,0.3);
        border-radius:16px; padding:1.5rem;">
            <div style="font-size:2.5rem;">🏅</div>
            <div style="font-size:2.5rem; font-weight:700; color:#02C39A;">{earned_count}/{len(BADGES)}</div>
            <div style="color:rgba(255,255,255,0.6); font-size:0.85rem;">Badges Earned</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📊 Score Breakdown</div>', unsafe_allow_html=True)
    for label, s, max_s in breakdown:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(s / max_s)
        with col2:
            st.markdown(f"**{s}/{max_s}**")
        st.caption(label)

    st.markdown('<div class="section-header">📅 Streak History</div>', unsafe_allow_html=True)
    if os.path.exists("mood_log.csv"):
        df_streak = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
        if not df_streak.empty:
            df_streak["Date"] = pd.to_datetime(df_streak["Date"]).dt.date
            unique_days = sorted(df_streak["Date"].unique(), reverse=True)
            for day in unique_days[:10]:
                st.markdown(f"✅ {day}")

    st.markdown('<div class="section-header">🏅 Badges</div>', unsafe_allow_html=True)
    earned = [b for b in BADGES if b["condition"](mood_count, sleep_count, journal_count, current_streak)]
    not_earned = [b for b in BADGES if not b["condition"](mood_count, sleep_count, journal_count, current_streak)]
    if earned:
        st.markdown("**✅ Earned:**")
        cols = st.columns(3)
        for i, badge in enumerate(earned):
            with cols[i % 3]:
                st.markdown(f'<div class="badge-card"><div style="font-size:1.8rem;">{badge["name"].split()[-1]}</div><div style="color:#02C39A;font-weight:600;font-size:0.9rem;">{badge["name"]}</div><div style="color:rgba(255,255,255,0.6);font-size:0.75rem;">{badge["desc"]}</div></div>', unsafe_allow_html=True)
    if not_earned:
        st.markdown("**🔒 To Earn:**")
        for badge in not_earned:
            st.markdown(f'<div class="badge-locked">🔒 <strong>{badge["name"]}</strong> — {badge["desc"]}</div>', unsafe_allow_html=True)

elif selected == "📈 Progress":
    st.markdown(f'<div class="section-header">📈 Progress Report{", " + name if st.session_state.user_name else ""}</div>', unsafe_allow_html=True)
    report_period = st.radio("Show:", ["Last 7 Days", "Last 30 Days"], horizontal=True)
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
                with col1: st.metric("Total", total)
                with col2: st.metric("😊 Happy", happy)
                with col3: st.metric("😔 Sad", sad)
                with col4: st.metric("😰 Stressed", stressed)
            else:
                st.info(f"No mood logs in last {days} days.")
    else:
        st.info("No mood logs yet.")
    st.markdown(f'<div class="section-header">Sleep — {report_period}</div>', unsafe_allow_html=True)
    if os.path.exists("sleep_log.csv"):
        df_sleep = pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"])
        if not df_sleep.empty:
            df_sleep["Date"] = pd.to_datetime(df_sleep["Date"])
            fs = df_sleep[df_sleep["Date"] >= pd.Timestamp.now() - pd.Timedelta(days=days)]
            if not fs.empty:
                avg = fs["Hours"].mean()
                st.metric("Average Sleep", f"{avg:.1f} hrs")
                st.line_chart(fs.set_index("Date")["Hours"])
                if avg >= 8: st.success("Great sleep! 😴🌟")
                elif avg >= 6: st.info("Decent. Aim for 8 hours! 🌙")
                else: st.warning("Not enough sleep! 😴")
    else:
        st.info("No sleep logs yet.")
    st.markdown('<div class="section-header">🤖 AI Progress Summary</div>', unsafe_allow_html=True)
    if st.button("Get AI Summary 🧠"):
        mood_summary = sleep_summary = journal_summary = ""
        if os.path.exists("mood_log.csv"):
            df_m = pd.read_csv("mood_log.csv", names=["Date", "Mood", "Note"])
            if not df_m.empty:
                mood_summary = df_m["Mood"].value_counts().to_string()
        if os.path.exists("sleep_log.csv"):
            df_s = pd.read_csv("sleep_log.csv", names=["Date", "Hours", "Quality", "Note"])
            if not df_s.empty:
                sleep_summary = f"Average: {df_s['Hours'].mean():.1f} hours"
        if os.path.exists("journal_log.csv"):
            df_j = pd.read_csv("journal_log.csv", names=["Date", "Title", "Entry"])
            journal_summary = f"Total entries: {len(df_j)}"
        with st.spinner("Reviewing your progress..."):
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are MindEase reviewing wellness progress warmly."},
                        {"role": "user", "content": f"User: {name}. Mood: {mood_summary}. Sleep: {sleep_summary}. Journal: {journal_summary}. Write 3-4 warm encouraging sentences using their name. Highlight what they do well and suggest one improvement."}
                    ]
                )
                st.markdown(f'<div class="card-green" style="color:white;">🌿 {response.choices[0].message.content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
