import streamlit as st
from groq import Groq
import csv
import os
from datetime import datetime
import pandas as pd
import random
import time
import json

st.set_page_config(page_title="MindEase", page_icon="🌿", layout="wide")

st.markdown("""
<style>
:root {
    --primary: #02C39A;
    --primary-dark: #028090;
    --primary-light: rgba(2, 195, 154, 0.15);
    --primary-border: rgba(2, 195, 154, 0.35);
}

.mcard {
    background: var(--primary-light);
    border: 1px solid var(--primary-border);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin: 0.7rem 0;
}

.mcard-plain {
    background: rgba(128,128,128,0.08);
    border: 1px solid rgba(128,128,128,0.15);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin: 0.7rem 0;
}

.section-title {
    color: var(--primary);
    font-size: 1.15rem;
    font-weight: 700;
    margin: 1.4rem 0 0.6rem 0;
    padding-bottom: 0.35rem;
    border-bottom: 2px solid var(--primary-border);
}

.main-header {
    background: linear-gradient(135deg, #028090, #02C39A);
    padding: 1.8rem 2rem;
    border-radius: 18px;
    margin-bottom: 1.2rem;
    text-align: center;
    box-shadow: 0 6px 24px rgba(2,195,154,0.25);
}

.main-header h1 { color: white !important; font-size: 2.2rem; font-weight: 800; margin: 0; }
.main-header p { color: rgba(255,255,255,0.88) !important; margin: 0.3rem 0 0 0; font-size: 1rem; }

.affirmation-box {
    background: linear-gradient(135deg, rgba(2,195,154,0.18), rgba(2,128,144,0.12));
    border: 1px solid var(--primary-border);
    border-radius: 16px;
    padding: 1.8rem;
    text-align: center;
    font-size: 1.15rem;
    line-height: 1.75;
    margin: 0.8rem 0;
}

.quote-box {
    border-left: 4px solid var(--primary);
    border-radius: 0 12px 12px 0;
    padding: 1.3rem 1.8rem;
    margin: 0.8rem 0;
    font-style: italic;
    font-size: 1.05rem;
    line-height: 1.75;
    background: rgba(128,128,128,0.07);
}

.result-box {
    border-radius: 14px;
    padding: 1.3rem;
    text-align: center;
    font-size: 1.05rem;
    font-weight: 600;
    margin: 0.8rem 0;
}

.badge-earned {
    background: rgba(2,195,154,0.12);
    border: 2px solid var(--primary-border);
    border-radius: 12px;
    padding: 0.9rem;
    text-align: center;
    margin: 0.3rem;
}

.badge-locked {
    background: rgba(128,128,128,0.06);
    border: 1px solid rgba(128,128,128,0.15);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin: 0.25rem 0;
    opacity: 0.65;
}

.score-box {
    text-align: center;
    border-radius: 20px;
    padding: 2rem;
    margin: 0.8rem 0;
    border: 2px solid var(--primary-border);
    background: rgba(128,128,128,0.06);
}

.chat-history-item {
    background: rgba(128,128,128,0.07);
    border: 1px solid rgba(128,128,128,0.15);
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
    margin: 0.3rem 0;
    font-size: 0.88rem;
}

div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 2px solid var(--primary-border) !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(2,195,154,0.18) !important;
}
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    border-radius: 50% !important;
}

.stButton > button {
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 14px rgba(2,195,154,0.38) !important;
}

/* Nav buttons — invisible overlay on top of styled div */
section[data-testid="stSidebar"] .stButton > button {
    opacity: 0 !important;
    position: absolute !important;
    height: 36px !important;
    margin-top: -40px !important;
    width: 85% !important;
    cursor: pointer !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    transform: none !important;
}

/* Keep music, chat and profile buttons visible */
section[data-testid="stSidebar"] [data-testid="stButton-music_play"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-music_stop"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-new_chat"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-delete_history"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-save_profile"] > button {
    opacity: 1 !important;
    position: relative !important;
    height: auto !important;
    margin-top: 0 !important;
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transform: none !important;
}

section[data-testid="stSidebar"] [data-testid="stButton-music_play"] > button:hover,
section[data-testid="stSidebar"] [data-testid="stButton-music_stop"] > button:hover,
section[data-testid="stSidebar"] [data-testid="stButton-new_chat"] > button:hover,
section[data-testid="stSidebar"] [data-testid="stButton-delete_history"] > button:hover,
section[data-testid="stSidebar"] [data-testid="stButton-save_profile"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 10px rgba(2,195,154,0.35) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────
for key, default in {
    "messages": [],
    "affirmation": None,
    "user_name": "",
    "user_age": "",
    "profile_set": False,
    "music_playing": False,
    "selected_music": None,
    "current_conversation": [],
    "conversations": [],
    "page": "💬 Chat",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

api_key = st.secrets["GROQ_API_KEY"]

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
    ("You don't have to be positive all the time.", "Lori Deschene"),
    ("Self-care is not self-indulgence, it is self-preservation.", "Audre Lorde"),
    ("Healing is not linear.", "Unknown"),
    ("Be gentle with yourself.", "Max Ehrmann"),
    ("You are braver than you believe, stronger than you seem.", "A.A. Milne"),
    ("You matter. You are enough. You are loved.", "Unknown"),
]

HAPPY_VIDEOS = [
    ("Relaxing Nature Sounds 🌿", "https://www.youtube.com/embed/1ZYbU82GVz4"),
    ("Calm Piano Music 🎵", "https://www.youtube.com/embed/lFcSrYw-ARY"),
    ("Funny Animals 😄", "https://www.youtube.com/embed/WYkiiGnOyBw"),
    ("Peaceful Ocean Waves 🌊", "https://www.youtube.com/embed/bn9F19Hi1Lk"),
    ("Uplifting Morning Music ☀️", "https://www.youtube.com/embed/inpok4MKVLM"),
]

MOOD_COLORS = {
    "😊 Happy":    {"color": "#FFD700", "bg": "rgba(255,215,0,0.12)",   "label": "Golden Joy",   "message": "You are glowing today! Keep that beautiful energy! 🌟"},
    "😐 Okay":     {"color": "#87CEEB", "bg": "rgba(135,206,235,0.12)", "label": "Calm Blue",    "message": "A steady calm day. That is perfectly fine! 🌤️"},
    "😔 Sad":      {"color": "#6495ED", "bg": "rgba(100,149,237,0.12)", "label": "Deep Blue",    "message": "It is okay to feel sad. Be gentle with yourself today. 💙"},
    "😰 Stressed": {"color": "#FF6B6B", "bg": "rgba(255,107,107,0.12)", "label": "Warm Red",     "message": "Take a deep breath. You can get through this! 🌬️"},
    "😡 Angry":    {"color": "#FF4500", "bg": "rgba(255,69,0,0.12)",    "label": "Fiery Orange", "message": "Your feelings are valid. Try the breathing exercise. 🌿"},
}

MUSIC_OPTIONS = {
    "🌿 Relaxing Nature": "https://www.youtube.com/embed/1ZYbU82GVz4",
    "🎹 Calm Piano":      "https://www.youtube.com/embed/lFcSrYw-ARY",
    "🌊 Ocean Waves":     "https://www.youtube.com/embed/bn9F19Hi1Lk",
    "🌙 Sleep Music":     "https://www.youtube.com/embed/1vx8iUvfyCY",
    "🌧️ Rain Sounds":    "https://www.youtube.com/embed/mPZkdNFkNps",
    "🔥 Fireplace":       "https://www.youtube.com/embed/UgHKb_7884o",
    "🎵 Lofi Hip Hop":    "https://www.youtube.com/embed/jfKfPfyJRdk",
    "☀️ Morning Music":  "https://www.youtube.com/embed/inpok4MKVLM",
}

BADGES = [
    {"name": "First Step 🌱",      "desc": "Logged your first mood",         "fn": lambda m,s,j,st: m>=1},
    {"name": "Mood Tracker 😊",    "desc": "Logged mood 5 times",            "fn": lambda m,s,j,st: m>=5},
    {"name": "Consistent Soul 🌟", "desc": "Logged mood 10 times",           "fn": lambda m,s,j,st: m>=10},
    {"name": "Sleep Logger 😴",    "desc": "Logged your first sleep",        "fn": lambda m,s,j,st: s>=1},
    {"name": "Dear Diary 📝",      "desc": "Wrote your first journal entry", "fn": lambda m,s,j,st: j>=1},
    {"name": "Storyteller ✍️",    "desc": "Wrote 5 journal entries",        "fn": lambda m,s,j,st: j>=5},
    {"name": "3 Day Streak 🔥",    "desc": "Logged mood 3 days in a row",    "fn": lambda m,s,j,st: st>=3},
    {"name": "Week Warrior 🏆",    "desc": "Logged mood 7 days in a row",    "fn": lambda m,s,j,st: st>=7},
    {"name": "Champion 👑",        "desc": "Logged mood 30 days in a row",   "fn": lambda m,s,j,st: st>=30},
]

name = st.session_state.user_name if st.session_state.user_name else "friend"
age  = st.session_state.user_age  if st.session_state.user_age  else ""

SYSTEM_PROMPT = f"""You are MindEase, a very close and caring best friend.
The user's name is {name}.{"They are " + age + " years old." if age else ""}
Always call them by their name — {name}.
Be warm, gentle, empathetic. Talk casually like a real close friend.
Never sound robotic. Use simple language and gentle emojis 🌿 💙 😊.
Always acknowledge feelings first. Ask one gentle question at a time.
Keep responses short and warm like a text message from a close friend.
If user mentions self-harm share: https://www.iasp.info/resources/Crisis_Centres/
Never diagnose. Encourage professional help gently when needed."""

def groq_call(messages, system=SYSTEM_PROMPT):
    client = Groq(api_key=api_key)
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + messages
    ).choices[0].message.content

def save_conversation():
    if st.session_state.current_conversation:
        conv = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "preview": st.session_state.current_conversation[0]["content"][:40] + "...",
            "messages": st.session_state.current_conversation
        }
        existing = []
        if os.path.exists("conversations.json"):
            with open("conversations.json", "r") as f:
                existing = json.load(f)
        existing.insert(0, conv)
        with open("conversations.json", "w") as f:
            json.dump(existing, f)

def load_conversations():
    if os.path.exists("conversations.json"):
        with open("conversations.json", "r") as f:
            return json.load(f)
    return []

def get_streak():
    if not os.path.exists("mood_log.csv"):
        return 0
    df = pd.read_csv("mood_log.csv", names=["Date","Mood","Note"])
    if df.empty:
        return 0
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    days = sorted(df["Date"].unique(), reverse=True)
    streak, today = 0, datetime.now().date()
    for i, d in enumerate(days):
        if d == today - pd.Timedelta(days=i):
            streak += 1
        else:
            break
    return streak

# ── Nav items ──────────────────────────────────────────────────
NAV_ITEMS = [
    ("💬 Chat",           "Chat",           "M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 16H5.83l-.83.83V4h15v14z"),
    ("😊 Mood",           "Mood",           "M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"),
    ("📝 Journal",        "Journal",        "M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm4 18H6V4h7v5h5v11zM8 15h8v2H8zm0-4h8v2H8zm0-4h5v2H8z"),
    ("🌅 Daily Wellness", "Daily Wellness", "M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 16.95h2V19.5h-2v2.95zm-7.45-3.91l1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z"),
    ("🧘 Meditation",     "Meditation",     "M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 16c-3.86 0-7-3.14-7-7s3.14-7 7-7 7 3.14 7 7-3.14 7-7 7zm-1-11h2v6h-2zm0 8h2v2h-2z"),
    ("🎯 Affirmations",   "Affirmations",   "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm4.59-12.42L10 14.17l-2.59-2.58L6 13l4 4 8-8-1.41-1.42z"),
    ("🧠 Assessment",     "Assessment",     "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 10h2v7H7zm4-3h2v10h-2zm4 6h2v4h-2z"),
    ("🏆 Achievements",   "Achievements",   "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12V11c0 4.52-3.13 8.74-7 9.93-3.87-1.19-7-5.41-7-9.93V6.3l7-3.12z"),
    ("📈 Progress",       "Progress",       "M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"),
]

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1rem 0 0.5rem;'>
        <span style='font-size:2.2rem;'>🌿</span>
        <div style='font-size:1.25rem; font-weight:800;'>MindEase</div>
        <div style='font-size:0.78rem; opacity:0.6;'>Your wellness companion</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    with st.expander("👤 My Profile", expanded=not st.session_state.profile_set):
        uname = st.text_input("Name", value=st.session_state.user_name, placeholder="Your name...")
        uage  = st.text_input("Age",  value=st.session_state.user_age,  placeholder="Your age...")
        if st.button("Save Profile ✅", key="save_profile"):
            st.session_state.user_name = uname
            st.session_state.user_age  = uage
            st.session_state.profile_set = True
            st.success(f"Welcome, {uname}! 🌿")
            st.rerun()

    if st.session_state.profile_set:
        st.markdown(f"""
        <div class='mcard' style='text-align:center; padding:0.8rem;'>
            <div style='font-size:1.6rem;'>😊</div>
            <div style='font-weight:700;'>{st.session_state.user_name}</div>
            <div style='font-size:0.8rem; opacity:0.65;'>Age {st.session_state.user_age}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**🎵 Music Player**")
    selected_music = st.selectbox("Choose", list(MUSIC_OPTIONS.keys()), label_visibility="collapsed")
   if st.button("▶️ Play Music", key="music_play", use_container_width=True):
        st.session_state.music_playing = True
        st.session_state.selected_music = selected_music
        st.rerun()
    if st.button("⏹ Stop Music", key="music_stop", use_container_width=True):
        st.session_state.music_playing = False
        st.session_state.selected_music = None
        st.rerun()

    if st.session_state.music_playing and st.session_state.selected_music:
        url = MUSIC_OPTIONS[st.session_state.selected_music]
        st.markdown(f"""
        <div style='border-radius:10px; overflow:hidden; margin-top:0.5rem;'>
        <iframe width="100%" height="80" src="{url}?autoplay=1"
        frameborder="0" allow="autoplay; encrypted-media"></iframe>
        </div>
        <div style='font-size:0.78rem; opacity:0.65; margin-top:0.3rem;'>
        🎵 {st.session_state.selected_music}
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**🕐 Chat History**")
    if st.button("➕ New Chat", key="new_chat", use_container_width=True):
        save_conversation()
        st.session_state.messages = []
        st.session_state.current_conversation = []
        st.rerun()

    convs = load_conversations()
    if convs:
        if st.button("🗑️ Delete History", key="delete_history", use_container_width=True):
            os.remove("conversations.json")
            st.success("History deleted!")
            st.rerun()
        for conv in convs[:8]:
            st.markdown(f"""
            <div class='chat-history-item'>
                <div style='font-weight:600; font-size:0.82rem;'>💬 {conv['date']}</div>
                <div style='opacity:0.7; font-size:0.78rem;'>{conv['preview']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No history yet. Start chatting!")

    st.divider()
    st.markdown("**Menu**")
    for key, label, icon_path in NAV_ITEMS:
        is_active = st.session_state.page == key
        active_style = "background:rgba(2,195,154,0.15); border:1px solid rgba(2,195,154,0.4);" if is_active else "border:1px solid transparent;"
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:8px; padding:0.42rem 0.85rem;
        border-radius:9px; margin:0.06rem 0; cursor:pointer; {active_style}
        transition: all 0.2s ease;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="#02C39A" stroke-width="1.8" stroke-linecap="round"
            stroke-linejoin="round">
                <path d="{icon_path}"/>
            </svg>
            <span style="font-size:0.88rem; font-weight:500;">{label}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

page = st.session_state.page

# ── Header ─────────────────────────────────────────────────────
st.markdown(f"""
<div class='main-header'>
    <h1>🌿 MindEase</h1>
    <p>{"Welcome back, " + name + "! So glad you are here. 💙" if st.session_state.user_name else "Your personal AI companion for mental wellness"}</p>
</div>
""", unsafe_allow_html=True)

# ══ PAGE 1 — CHAT ══════════════════════════════════════════════
if page == "💬 Chat":
    if not st.session_state.user_name:
        st.info("👤 Enter your name in the sidebar for a personalised experience!")
    chat_container = st.container(height=480)
    with chat_container:
        if not st.session_state.messages:
            with st.chat_message("assistant", avatar="🌿"):
                welcome = f"Hi {name}! 😊 I am MindEase, your personal wellness companion. How are you feeling today?" if st.session_state.user_name else "Hi there! 😊 I am MindEase. Enter your name in the sidebar and let us get started! How are you feeling?"
                st.markdown(welcome)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🌿" if msg["role"]=="assistant" else "🧑"):
                st.markdown(msg["content"])
    user_input = st.chat_input(f"Share how you are feeling, {name}..." if st.session_state.user_name else "Share how you are feeling...")
    if user_input:
        with chat_container:
            with st.chat_message("user", avatar="🧑"):
                st.markdown(user_input)
        st.session_state.messages.append({"role":"user","content":user_input})
        st.session_state.current_conversation.append({"role":"user","content":user_input})
        with chat_container:
            with st.chat_message("assistant", avatar="🌿"):
                with st.spinner("MindEase is listening..."):
                    try:
                        reply = groq_call(st.session_state.messages)
                        st.markdown(reply)
                        st.session_state.messages.append({"role":"assistant","content":reply})
                        st.session_state.current_conversation.append({"role":"assistant","content":reply})
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")
        st.rerun()

# ══ PAGE 2 — MOOD ══════════════════════════════════════════════
if page == "😊 Mood":
    st.markdown(f'<div class="section-title">😊 How are you feeling{", " + name if st.session_state.user_name else ""}?</div>', unsafe_allow_html=True)
    mood = st.radio("", ["😊 Happy","😐 Okay","😔 Sad","😰 Stressed","😡 Angry"], horizontal=True)
    note = st.text_input("Add a note (optional)", placeholder="What is making you feel this way?")
    md = MOOD_COLORS[mood]
    st.markdown(f"""
    <div style='text-align:center; background:{md["bg"]}; border:2px solid {md["color"]};
    border-radius:16px; padding:1.8rem; margin:0.8rem 0;'>
        <div style='font-size:2.8rem;'>{mood}</div>
        <div style='font-size:1.2rem; font-weight:700; color:{md["color"]}; margin:0.4rem 0;'>{md["label"]}</div>
        <div style='width:55px;height:55px;border-radius:50%;background:{md["color"]};margin:0.7rem auto;'></div>
        <div style='font-size:0.95rem;'>{md["message"]}</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save My Mood"):
            with open("mood_log.csv","a",newline="") as f:
                csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), mood, note])
            st.success(f"Mood saved{', '+name if st.session_state.user_name else ''}! 🌿")
    with c2:
        if st.button("💬 Get Personal Message"):
            with st.spinner("Thinking..."):
                try:
                    msg = groq_call([{"role":"user","content":f"I am feeling {mood}. Write me a warm short personal message. 3 sentences max."}])
                    st.markdown(f'<div class="mcard" style="border-left:4px solid {md["color"]};">🌿 {msg}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(str(e))
    st.markdown('<div class="section-title">📊 Mood History</div>', unsafe_allow_html=True)
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date","Mood","Note"])
        if not df.empty:
            if st.button("🗑️ Delete Mood Logs"):
                os.remove("mood_log.csv"); st.rerun()
            st.dataframe(df, use_container_width=True)
            mc = df["Mood"].value_counts().reset_index()
            mc.columns = ["Mood","Count"]
            st.bar_chart(mc.set_index("Mood"))
    else:
        st.info("No mood logs yet!")

# ══ PAGE 3 — JOURNAL ═══════════════════════════════════════════
if page == "📝 Journal":
    st.markdown(f'<div class="section-title">📝 Journal{" — "+name if st.session_state.user_name else ""}</div>', unsafe_allow_html=True)
    st.caption("Your private space. Write anything you feel.")
    jtitle = st.text_input("Title", placeholder="My thoughts today...")
    jentry = st.text_area("Write here...", height=200, placeholder="Today I felt...")
    if st.button("💾 Save Journal Entry"):
        if jentry.strip():
            with open("journal_log.csv","a",newline="") as f:
                csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), jtitle, jentry])
            st.success("Journal entry saved! 🌿")
        else:
            st.warning("Please write something first!")
    st.markdown('<div class="section-title">📖 Past Entries</div>', unsafe_allow_html=True)
    if os.path.exists("journal_log.csv"):
        dfj = pd.read_csv("journal_log.csv", names=["Date","Title","Entry"])
        if not dfj.empty:
            if st.button("🗑️ Delete Journal Entries"):
                os.remove("journal_log.csv"); st.rerun()
            for _, row in dfj.iloc[::-1].iterrows():
                with st.expander(f"📝 {row['Date']} — {row['Title']}"):
                    st.write(row["Entry"])
        else:
            st.info("No entries yet!")
    else:
        st.info("No entries yet!")

# ══ PAGE 4 — DAILY WELLNESS ════════════════════════════════════
if page == "🌅 Daily Wellness":
    hour = datetime.now().hour
    is_morning = 5 <= hour < 12
    is_evening = 17 <= hour <= 23

    st.markdown('<div class="section-title">🌅 Morning Check In</div>', unsafe_allow_html=True)
    if is_morning:
        with st.spinner("Preparing your good morning message..."):
            try:
                gm = groq_call([{"role":"user","content":f"Give {name} a warm cheerful good morning greeting and one motivational sentence for the day. Keep it short and personal."}])
                st.markdown(f'<div class="mcard">🌅 {gm}</div>', unsafe_allow_html=True)
            except:
                st.markdown(f'<div class="mcard">🌅 Good morning{", "+name if st.session_state.user_name else ""}! Today is a new beginning. Make it count! 🌿</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="mcard">🌅 Good morning section is active from 5 AM to 12 PM. Come back tomorrow morning{", "+name if st.session_state.user_name else ""}! 🌿</div>', unsafe_allow_html=True)

    morning_mood = st.selectbox("😊 How are you feeling this morning?", ["😊 Happy","😐 Okay","😔 Sad","😰 Stressed","😡 Angry"])
    st.markdown('<div class="section-title">✅ Things To Do Today</div>', unsafe_allow_html=True)
    tasks_input = st.text_area("Add your tasks for today", placeholder="1. Study for exam\n2. Call mom\n3. Drink water", height=120)

    if st.button("✨ Get AI Suggestions for My Day"):
        with st.spinner("Thinking of suggestions..."):
            try:
                suggestions = groq_call([{"role":"user","content":f"{name} is feeling {morning_mood} this morning. Their tasks are: {tasks_input}. Suggest 3 extra small helpful things they can add to their day based on how they feel. Keep it short and friendly."}])
                st.markdown(f'<div class="mcard">💡 {suggestions}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))

    if st.button("💾 Save Morning Check In"):
        with open("morning_log.csv","a",newline="",encoding="utf-8") as f:
            csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), morning_mood, tasks_input])
        st.success(f"Morning check in saved{', '+name if st.session_state.user_name else ''}! Have an amazing day! 🌅")

    st.divider()
    st.markdown('<div class="section-title">🌙 Evening Check In</div>', unsafe_allow_html=True)
    if is_evening:
        st.markdown(f'<div class="mcard">🌙 Good evening{", "+name if st.session_state.user_name else ""}! Time to wind down and reflect on your day. 🌿</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="mcard">🌙 Evening section is most useful from 5 PM to 11 PM. Fill it in before bed!</div>', unsafe_allow_html=True)

    sleep_hours   = st.slider("😴 How many hours did you sleep last night?", 0, 12, 7)
    sleep_quality = st.radio("Sleep quality:", ["😴 Very Good","🙂 Good","😐 Okay","😔 Poor","😫 Very Poor"], horizontal=True)
    water_glasses = st.slider("💧 How many glasses of water did you drink today?", 0, 15, 8)
    day_rating    = st.slider("⭐ How was your day overall?", 1, 10, 5)
    day_highlight = st.text_input("🌟 Best part of your day?", placeholder="Something good that happened...")
    day_challenge = st.text_input("💪 Hardest part of your day?", placeholder="Something difficult today...")
    grateful_for  = st.text_area("🙏 3 things you are grateful for", placeholder="1. \n2. \n3. ", height=90)
    tomorrow_goal = st.text_input("🎯 One small goal for tomorrow?", placeholder="Something small and achievable...")

    if water_glasses < 6:
        st.warning("💧 You drank less than 6 glasses today. Try to drink more water tomorrow!")
    elif water_glasses >= 8:
        st.success("💧 Great hydration today! Keep it up!")

    if st.button("🌙 Save Evening Check In and Get Goodnight Message"):
        if day_highlight.strip() == "" and grateful_for.strip() == "":
            st.warning("Please fill in at least some fields!")
        else:
            with open("evening_log.csv","a",newline="",encoding="utf-8") as f:
                csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), sleep_hours, sleep_quality, water_glasses, day_rating, day_highlight, day_challenge, grateful_for, tomorrow_goal])
            with open("sleep_log.csv","a",newline="") as f:
                csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), sleep_hours, sleep_quality, ""])
            st.success("Evening check in saved! 🌙")
            with st.spinner("MindEase is preparing your goodnight message..."):
                try:
                    night_prompt = f"""User name: {name}. Evening check in:
                    Sleep last night: {sleep_hours} hours ({sleep_quality}).
                    Water today: {water_glasses} glasses.
                    Day rating: {day_rating}/10.
                    Best part: {day_highlight}.
                    Hardest part: {day_challenge}.
                    Grateful for: {grateful_for}.
                    Tomorrow goal: {tomorrow_goal}.

                    Write THREE things:
                    1. A warm personal goodnight message using their name {name} — 2 sentences.
                    2. A short paragraph summarising how their day went based on the data — 3 sentences.
                    3. Practical advice on how to make tomorrow better and what bad habits to work on — 3 sentences.

                    Separate each part with a line break. Be warm, honest, and caring like a close friend."""
                    night_msg = groq_call([{"role":"user","content":night_prompt}])
                    parts = night_msg.split("\n\n") if "\n\n" in night_msg else night_msg.split("\n")
                    st.markdown(f'<div class="mcard" style="border-left:4px solid #9B72CF;"><strong>🌙 Goodnight Message</strong><br><br>{parts[0]}</div>', unsafe_allow_html=True)
                    if len(parts) > 1:
                        st.markdown(f'<div class="mcard-plain"><strong>📋 Your Day in Summary</strong><br><br>{parts[1]}</div>', unsafe_allow_html=True)
                    if len(parts) > 2:
                        st.markdown(f'<div class="mcard"><strong>💡 How to Make Tomorrow Better</strong><br><br>{parts[2]}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(str(e))

    st.markdown('<div class="section-title">📖 Past Evening Check Ins</div>', unsafe_allow_html=True)
    if os.path.exists("evening_log.csv"):
        dfe = pd.read_csv("evening_log.csv", names=["Date","Sleep","Quality","Water","Rating","Highlight","Challenge","Grateful","Goal"])
        if not dfe.empty:
            if st.button("🗑️ Delete Evening Logs"):
                os.remove("evening_log.csv"); st.rerun()
            for _, row in dfe.iloc[::-1].iterrows():
                with st.expander(f"🌙 {row['Date']} — Day {row['Rating']}/10"):
                    st.markdown(f"**😴 Sleep:** {row['Sleep']} hrs ({row['Quality']})")
                    st.markdown(f"**💧 Water:** {row['Water']} glasses")
                    st.markdown(f"**🌟 Best part:** {row['Highlight']}")
                    st.markdown(f"**💪 Hardest part:** {row['Challenge']}")
                    st.markdown(f"**🙏 Grateful for:** {row['Grateful']}")
                    st.markdown(f"**🎯 Tomorrow goal:** {row['Goal']}")
    else:
        st.info("No evening check ins yet. Come back tonight! 🌙")

# ══ PAGE 5 — MEDITATION ════════════════════════════════════════
if page == "🧘 Meditation":
    st.markdown('<div class="section-title">🧘 Meditation and Breathing</div>', unsafe_allow_html=True)
    ex_type = st.radio("What do you want to do?", ["🌬️ Breathing Exercise","🧘 Guided Meditation"], horizontal=True)
    if ex_type == "🌬️ Breathing Exercise":
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            bp = st.empty()
        rounds = st.slider("Rounds", 1, 5, 3)
        if st.button("Start 🌬️"):
            for i in range(rounds):
                st.markdown(f"**Round {i+1}/{rounds}**")
                for label, grad, toast_msg, secs in [
                    ("Breathe In 🌬️","#02C39A,#028090","Breathe IN...",4),
                    ("Hold ⏸️","#9B72CF,#028090","HOLD...",4),
                    ("Breathe Out 😮‍💨","#028090,#1A1A2E","Breathe OUT...",6),
                ]:
                    bp.markdown(f'<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,{grad});display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.2rem;font-weight:600;">{label}</div>', unsafe_allow_html=True)
                    st.toast(toast_msg)
                    time.sleep(secs)
            bp.markdown('<div style="width:200px;height:200px;border-radius:50%;background:linear-gradient(135deg,#02C39A,#028090);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1.2rem;font-weight:600;">Done! 🌿</div>', unsafe_allow_html=True)
            st.success(f"Great job{', '+name if st.session_state.user_name else ''}! 🌿")
    else:
        med_type = st.selectbox("Choose", ["🌿 5 Minute Calm","😴 Sleep Meditation","😰 Anxiety Relief","💙 Self Love","🎯 Focus Meditation"])
        MEDS = {
            "🌿 5 Minute Calm":[("Settle in","Sit comfortably. Close your eyes. Relax completely. 🌿",10),("Breathe","In 4. Hold 2. Out 6. 🌬️",15),("Body scan","Relax from toes to head. 😌",20),("Peaceful place","Imagine somewhere beautiful and safe. 🌸",30),("Return","Wiggle fingers. Open eyes slowly. ✨",10)],
            "😴 Sleep Meditation":[("Lie down","Sink into your bed. 😴",10),("Slow breath","In 4. Hold 7. Out 8. 🌙",20),("Release the day","Think of one good thing. Let the rest go. 🌿",20),("Body scan","Feel every part relax and get heavy. 💤",30),("Drift off","You are safe. You are calm. Sleep now. 🌙",15)],
            "😰 Anxiety Relief":[("Acknowledge","It is okay to feel anxious. You are safe. 💙",10),("5-4-3-2-1","5 things you see. 4 touch. 3 hear. 2 smell. 1 taste. 🌿",30),("Box breathing","In 4. Hold 4. Out 4. Hold 4. 🌬️",20),("Self talk","I am safe. This will pass. I am strong. 💪",15),("Calm","The anxiety is passing. You are okay. 🌸",15)],
            "💙 Self Love":[("Hand on heart","Breathe slowly. Feel your heartbeat. 💙",10),("Acknowledge yourself","Think of one thing you did well. 🌟",15),("Golden light","Imagine warm light growing in your chest. This is love. 💛",20),("Affirmation","I am enough. I am worthy. I deserve love. 🌸",20),("Gratitude","Thank yourself. Open eyes gently. 🌿",10)],
            "🎯 Focus Meditation":[("Prepare","Sit straight. Three deep breaths. 🎯",10),("Single focus","Pick one object. Stare gently. Return when mind wanders. 👁️",20),("Breath anchor","Use breath as anchor. Notice thoughts and return. 🌬️",20),("Visualise","See yourself completing your task calmly. 🌟",15),("Begin","Open eyes. You are ready. Start now. 🎯",10)],
        }
        if st.button("Start Meditation 🧘"):
            for i,(title,instruction,secs) in enumerate(MEDS[med_type]):
                st.markdown(f'<div class="mcard"><strong style="color:var(--primary);">Step {i+1} — {title}</strong><br><br>{instruction}</div>', unsafe_allow_html=True)
                time.sleep(secs)
            st.success(f"Meditation complete{', '+name if st.session_state.user_name else ''}! Well done! 🌿💙")

# ══ PAGE 6 — AFFIRMATIONS ══════════════════════════════════════
if page == "🎯 Affirmations":
    st.markdown('<div class="section-title">🎯 Your Daily Affirmation</div>', unsafe_allow_html=True)
    if st.session_state.affirmation is None:
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
    st.markdown(f'<div class="affirmation-box">{st.session_state.affirmation}</div>', unsafe_allow_html=True)
    if st.button("New Affirmation 🔄"):
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
        st.rerun()
    st.markdown('<div class="section-title">All Affirmations 🌟</div>', unsafe_allow_html=True)
    for a in AFFIRMATIONS:
        st.markdown(f"🌿 {a}")
    st.markdown('<div class="section-title">🌍 AI Quote Just For You</div>', unsafe_allow_html=True)
    feeling = st.text_input("How are you feeling right now?", placeholder="I feel stressed about...")
    if st.button("Generate My Quote 🌟"):
        if feeling.strip():
            with st.spinner("Creating your quote..."):
                try:
                    q = groq_call([{"role":"user","content":f"I am {name} and I feel: {feeling}. Write one beautiful meaningful short quote for me. Then write the author below. If you made it up write MindEase as author. Maximum 2 sentences."}])
                    st.markdown(f'<div class="quote-box">{q}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(str(e))
        else:
            st.warning("Please tell me how you are feeling!")
    st.markdown('<div class="section-title">Classic Quotes</div>', unsafe_allow_html=True)
    for q, a in QUOTES:
        with st.expander(f"💬 {q[:45]}..."):
            st.markdown(f'*"{q}"*')
            st.markdown(f"**— {a}**")

# ══ PAGE 7 — ASSESSMENT ════════════════════════════════════════
if page == "🧠 Assessment":
    st.markdown('<div class="section-title">🧠 Mental Health Assessment</div>', unsafe_allow_html=True)
    st.caption("Answer 8 honest questions. This is NOT a medical diagnosis — just a self check tool.")
    qs = [
        ("How often do you feel sad or hopeless?",           ["Never","Sometimes","Often","Always"]),
        ("How often do you feel worried or anxious?",         ["Never","Sometimes","Often","Always"]),
        ("How well are you sleeping?",                        ["Very Well","Okay","Poorly","Very Poorly"]),
        ("How often do you feel lonely?",                     ["Never","Sometimes","Often","Always"]),
        ("How often do you lose interest in enjoyable things?",["Never","Sometimes","Often","Always"]),
        ("How often do you feel tired or low energy?",        ["Never","Sometimes","Often","Always"]),
        ("How often do you feel angry or irritated?",         ["Never","Sometimes","Often","Always"]),
        ("How often do you feel overwhelmed?",                ["Never","Sometimes","Often","Always"]),
    ]
    score_map = {"Never":0,"Very Well":0,"Sometimes":1,"Okay":1,"Often":2,"Poorly":2,"Always":3,"Very Poorly":3}
    answers = [st.selectbox(f"{i+1}. {q}", opts) for i,(q,opts) in enumerate(qs)]
    if st.button("See My Results 🧠"):
        total = sum(score_map[a] for a in answers)
        if total <= 6:
            lv,col,em = "Low","#02C39A","😊"
            reason = "You are generally feeling well with good emotional balance."
            tips = ["Keep doing what you are doing! 🌿","Maintain regular sleep.","Stay connected with friends.","Practice affirmations daily."]
            vids = HAPPY_VIDEOS[:2]
        elif total <= 14:
            lv,col,em = "Moderate","#F4A261","😐"
            reason = "You are experiencing some stress. This is normal. With self care you can feel much better."
            tips = ["Try the meditation tab. 🧘","Journal every day. 📝","Log your mood daily. 😊","Get 7-8 hours sleep.","Talk to someone you trust."]
            vids = HAPPY_VIDEOS[:3]
        else:
            lv,col,em = "High","#E63946","😔"
            reason = "You may be going through a difficult time. You are not alone and help is available."
            tips = ["Talk to someone you trust. 💙","Use the Chat tab anytime. 💬","Helpline: https://www.iasp.info/resources/Crisis_Centres/","Try breathing exercises. 🌬️","Consider speaking to a professional."]
            vids = HAPPY_VIDEOS
        st.markdown(f'<div class="result-box" style="background:{col}20;border:2px solid {col};">{em} {name+", your" if st.session_state.user_name else "Your"} wellness level is <strong>{lv}</strong></div>', unsafe_allow_html=True)
        st.markdown(f"**Why?** {reason}")
        st.markdown("**What to do now:**")
        for t in tips:
            st.markdown(f"🌿 {t}")
        st.markdown("**Videos to help you feel better 🎥**")
        for title, url in vids:
            st.markdown(f"**{title}**")
            st.markdown(f'<iframe width="100%" height="200" src="{url}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
        st.caption("Not a medical diagnosis. Please see a doctor if struggling.")

# ══ PAGE 8 — ACHIEVEMENTS ══════════════════════════════════════
if page == "🏆 Achievements":
    st.markdown('<div class="section-title">🏆 Your Achievements</div>', unsafe_allow_html=True)
    mood_count = sleep_count = journal_count = 0
    if os.path.exists("mood_log.csv"):
        mood_count = len(pd.read_csv("mood_log.csv", names=["Date","Mood","Note"]))
    if os.path.exists("sleep_log.csv"):
        sleep_count = len(pd.read_csv("sleep_log.csv", names=["Date","Hours","Quality","Note"]))
    if os.path.exists("journal_log.csv"):
        journal_count = len(pd.read_csv("journal_log.csv", names=["Date","Title","Entry"]))
    streak = get_streak()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="score-box"><div style="font-size:3rem;">🔥</div><div style="font-size:2.5rem;font-weight:800;color:var(--primary);">{streak}</div><div style="opacity:0.6;">Day Streak</div></div>', unsafe_allow_html=True)
    with c2:
        sc = 0
        if os.path.exists("mood_log.csv"):
            df_m = pd.read_csv("mood_log.csv", names=["Date","Mood","Note"])
            if not df_m.empty:
                sc += min(int(len(df_m[df_m["Mood"]=="😊 Happy"])/len(df_m)*30),30)
        if os.path.exists("sleep_log.csv"):
            df_s = pd.read_csv("sleep_log.csv", names=["Date","Hours","Quality","Note"])
            if not df_s.empty:
                avg = df_s["Hours"].mean()
                sc += 25 if avg>=8 else 15 if avg>=6 else 5
        sc += min(journal_count*5,25)
        sc += min(streak*2,20)
        sc_col = "#02C39A" if sc>=80 else "#F4A261" if sc>=60 else "#E9C46A" if sc>=40 else "#E63946"
        st.markdown(f'<div class="score-box" style="border-color:{sc_col};"><div style="font-size:3rem;">🏆</div><div style="font-size:2.5rem;font-weight:800;color:{sc_col};">{sc}</div><div style="opacity:0.6;">Wellness Score / 100</div></div>', unsafe_allow_html=True)
    with c3:
        earned_count = sum(1 for b in BADGES if b["fn"](mood_count,sleep_count,journal_count,streak))
        st.markdown(f'<div class="score-box"><div style="font-size:3rem;">🏅</div><div style="font-size:2.5rem;font-weight:800;color:var(--primary);">{earned_count}/{len(BADGES)}</div><div style="opacity:0.6;">Badges Earned</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Score Breakdown</div>', unsafe_allow_html=True)
    breakdown_items = [
        ("😊 Mood Score",   min(int(len(pd.read_csv("mood_log.csv",names=["Date","Mood","Note"])[pd.read_csv("mood_log.csv",names=["Date","Mood","Note"])["Mood"]=="😊 Happy"])/max(len(pd.read_csv("mood_log.csv",names=["Date","Mood","Note"])),1)*30),30) if os.path.exists("mood_log.csv") else 0, 30),
        ("😴 Sleep Score",  (25 if pd.read_csv("sleep_log.csv",names=["Date","Hours","Quality","Note"])["Hours"].mean()>=8 else 15 if pd.read_csv("sleep_log.csv",names=["Date","Hours","Quality","Note"])["Hours"].mean()>=6 else 5) if os.path.exists("sleep_log.csv") and not pd.read_csv("sleep_log.csv",names=["Date","Hours","Quality","Note"]).empty else 0, 25),
        ("📝 Journal Score", min(journal_count*5,25), 25),
        ("📅 Streak Score",  min(streak*2,20), 20),
    ]
    for lbl, s, mx in breakdown_items:
        col_a, col_b = st.columns([4,1])
        with col_a:
            st.progress(s/mx if mx>0 else 0)
        with col_b:
            st.markdown(f"**{s}/{mx}**")
        st.caption(lbl)

    st.markdown('<div class="section-title">🏅 Badges</div>', unsafe_allow_html=True)
    earned   = [b for b in BADGES if b["fn"](mood_count,sleep_count,journal_count,streak)]
    unearned = [b for b in BADGES if not b["fn"](mood_count,sleep_count,journal_count,streak)]
    if earned:
        st.markdown("**✅ Earned**")
        cols = st.columns(3)
        for i, b in enumerate(earned):
            with cols[i%3]:
                st.markdown(f'<div class="badge-earned"><div style="font-size:1.6rem;">{b["name"].split()[-1]}</div><div style="color:var(--primary);font-weight:600;font-size:0.85rem;">{b["name"]}</div><div style="opacity:0.6;font-size:0.75rem;">{b["desc"]}</div></div>', unsafe_allow_html=True)
    if unearned:
        st.markdown("**🔒 Still to earn**")
        for b in unearned:
            st.markdown(f'<div class="badge-locked">🔒 <strong>{b["name"]}</strong> — {b["desc"]}</div>', unsafe_allow_html=True)

# ══ PAGE 9 — PROGRESS ══════════════════════════════════════════
if page == "📈 Progress":
    st.markdown('<div class="section-title">📈 Progress Report</div>', unsafe_allow_html=True)
    period = st.radio("Show report for:", ["Last 7 Days","Last 30 Days"], horizontal=True)
    days = 7 if period=="Last 7 Days" else 30

    st.markdown(f'<div class="section-title">Mood — {period}</div>', unsafe_allow_html=True)
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv", names=["Date","Mood","Note"])
        df["Date"] = pd.to_datetime(df["Date"])
        f = df[df["Date"] >= pd.Timestamp.now()-pd.Timedelta(days=days)]
        if not f.empty:
            mc = f["Mood"].value_counts().reset_index(); mc.columns=["Mood","Count"]
            st.bar_chart(mc.set_index("Mood"))
            c1,c2,c3,c4 = st.columns(4)
            with c1: st.metric("Total Logs", len(f))
            with c2: st.metric("😊 Happy",   len(f[f["Mood"]=="😊 Happy"]))
            with c3: st.metric("😔 Sad",      len(f[f["Mood"]=="😔 Sad"]))
            with c4: st.metric("😰 Stressed", len(f[f["Mood"]=="😰 Stressed"]))
        else: st.info(f"No mood logs in the last {days} days.")
    else: st.info("No mood logs yet.")

    st.markdown(f'<div class="section-title">Sleep — {period}</div>', unsafe_allow_html=True)
    if os.path.exists("sleep_log.csv"):
        ds = pd.read_csv("sleep_log.csv", names=["Date","Hours","Quality","Note"])
        ds["Date"] = pd.to_datetime(ds["Date"])
        fs = ds[ds["Date"] >= pd.Timestamp.now()-pd.Timedelta(days=days)]
        if not fs.empty:
            avg = fs["Hours"].mean()
            st.metric("Average Sleep", f"{avg:.1f} hrs")
            st.line_chart(fs.set_index("Date")["Hours"])
            if avg>=8: st.success("Great sleep average! 🌟")
            elif avg>=6: st.info("Decent. Aim for 8 hours! 🌙")
            else: st.warning("Not enough sleep. Rest more! 😴")
        else: st.info(f"No sleep logs in the last {days} days.")
    else: st.info("No sleep logs yet.")

    st.markdown(f'<div class="section-title">Journal — {period}</div>', unsafe_allow_html=True)
    if os.path.exists("journal_log.csv"):
        dj = pd.read_csv("journal_log.csv", names=["Date","Title","Entry"])
        dj["Date"] = pd.to_datetime(dj["Date"])
        fj = dj[dj["Date"] >= pd.Timestamp.now()-pd.Timedelta(days=days)]
        st.metric("Entries Written", len(fj))
        if len(fj)>=5: st.success("Amazing journaling habit! 📝🌟")
        elif len(fj)>=1: st.info("Good start! Try daily journaling! 📝")
        else: st.warning("No entries this period. Start writing! 📝")
    else: st.info("No journal entries yet.")

    st.markdown('<div class="section-title">🤖 AI Progress Summary</div>', unsafe_allow_html=True)
    if st.button("Get My AI Summary 🧠"):
        mm = sl = jj = ""
        if os.path.exists("mood_log.csv"):
            df_m = pd.read_csv("mood_log.csv", names=["Date","Mood","Note"])
            if not df_m.empty: mm = df_m["Mood"].value_counts().to_string()
        if os.path.exists("sleep_log.csv"):
            df_s = pd.read_csv("sleep_log.csv", names=["Date","Hours","Quality","Note"])
            if not df_s.empty: sl = f"Average sleep: {df_s['Hours'].mean():.1f} hours"
        if os.path.exists("journal_log.csv"):
            df_j = pd.read_csv("journal_log.csv", names=["Date","Title","Entry"])
            jj = f"Total entries: {len(df_j)}"
        with st.spinner("Reviewing your progress..."):
            try:
                summary = groq_call([{"role":"user","content":f"User: {name}. Mood data: {mm}. Sleep: {sl}. Journal: {jj}. Write 3-4 warm sentences using their name. Highlight what they do well and gently suggest one improvement."}])
                st.markdown(f'<div class="mcard">🌿 {summary}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))
