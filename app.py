import streamlit as st
from groq import Groq
from supabase import create_client
from datetime import datetime
import pandas as pd
import random
import time

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
.auth-box {
    max-width: 420px;
    margin: 2rem auto;
    padding: 2.5rem;
    border-radius: 20px;
    border: 1px solid var(--primary-border);
    background: var(--primary-light);
}
.auth-tab-active {
    border-bottom: 3px solid #02C39A !important;
    color: #02C39A !important;
    font-weight: 700 !important;
    background: transparent !important;
    box-shadow: none !important;
    transform: none !important;
    border-radius: 0 !important;
}
.auth-tab-inactive {
    border-bottom: 3px solid transparent !important;
    color: inherit !important;
    font-weight: 500 !important;
    background: transparent !important;
    box-shadow: none !important;
    transform: none !important;
    border-radius: 0 !important;
    opacity: 0.5 !important;
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
section[data-testid="stSidebar"] [data-testid^="stButton-nav_"] > button {
    background: transparent !important;
    color: inherit !important;
    border: 1px solid transparent !important;
    border-radius: 9px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    box-shadow: none !important;
    transform: none !important;
    transition: background 0.2s ease !important;
    padding: 0.4rem 0.85rem 0.4rem 2.2rem !important;
    margin: 0.04rem 0 !important;
    position: relative !important;
}
section[data-testid="stSidebar"] [data-testid^="stButton-nav_"] > button:hover {
    background: rgba(2,195,154,0.1) !important;
    border-color: rgba(2,195,154,0.3) !important;
    transform: none !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] [data-testid="stButton-music_play"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-music_stop"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-new_chat"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-delete_history"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-logout"] > button {
    background: linear-gradient(135deg, #028090, #02C39A) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transform: none !important;
    width: 100% !important;
    opacity: 1 !important;
    position: relative !important;
    font-size: 0.85rem !important;
}

/* Auth tab buttons */
[data-testid="stButton-tab_login"] > button {
    background: transparent !important;
    color: #02C39A !important;
    border: none !important;
    border-bottom: 3px solid #02C39A !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    transform: none !important;
    font-size: 1rem !important;
}
[data-testid="stButton-tab_signup"] > button {
    background: transparent !important;
    color: inherit !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    border-radius: 0 !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transform: none !important;
    opacity: 0.5 !important;
    font-size: 1rem !important;
}
[data-testid="stButton-tab_login_active"] > button {
    background: transparent !important;
    color: #02C39A !important;
    border: none !important;
    border-bottom: 3px solid #02C39A !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    transform: none !important;
    font-size: 1rem !important;
}
[data-testid="stButton-tab_signup_active"] > button {
    background: transparent !important;
    color: #02C39A !important;
    border: none !important;
    border-bottom: 3px solid #02C39A !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    transform: none !important;
    font-size: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────
for key, default in {
    "messages": [],
    "affirmation": None,
    "user_name": "",
    "user_email": "",
    "logged_in": False,
    "auth_token": None,
    "music_playing": False,
    "selected_music": None,
    "current_conversation": [],
    "page": "💬 Chat",
    "auth_mode": "Login",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Supabase + Groq ────────────────────────────────────────────
api_key = st.secrets["GROQ_API_KEY"]
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ── Supabase helper functions ──────────────────────────────────
def db_insert(table, data):
    try:
        supabase.table(table).insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Save failed: {e}")
        return False

def db_fetch(table, email):
    try:
        res = supabase.table(table).select("*").eq("user_email", email).order("created_at", desc=True).execute()
        return res.data
    except:
        return []

def db_delete_all(table, email):
    try:
        supabase.table(table).delete().eq("user_email", email).execute()
        return True
    except:
        return False

def get_streak(email):
    try:
        res = supabase.table("mood_logs").select("created_at").eq("user_email", email).execute()
        if not res.data:
            return 0
        dates = sorted(set([r["created_at"][:10] for r in res.data]), reverse=True)
        streak, today = 0, datetime.now().date()
        for i, d in enumerate(dates):
            if str(today - pd.Timedelta(days=i)) == d:
                streak += 1
            else:
                break
        return streak
    except:
        return 0

# ── Auth functions ─────────────────────────────────────────────
def sign_up(name, email, password):
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"name": name}}
        })
        if res.user:
            return True, "Account created successfully! 🌿"
        return False, "Something went wrong. Please try again."
    except Exception as e:
        return False, str(e)

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if res.user:
            name = res.user.user_metadata.get("name", email.split("@")[0])
            return True, name, "Welcome back! 🌿"
        return False, "", "Invalid email or password."
    except Exception as e:
        return False, "", "Invalid email or password. Please try again."

def sign_out():
    try:
        supabase.auth.sign_out()
    except:
        pass
    for key in ["logged_in", "auth_token", "user_name", "user_email", "messages", "current_conversation"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ── Login / Signup Screen ──────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align:center; padding:2rem 0 1rem;'>
        <span style='font-size:3rem;'>🌿</span>
        <h1 style='color:#02C39A; font-size:2.5rem; font-weight:800; margin:0.3rem 0;'>MindEase</h1>
        <p style='opacity:0.6; font-size:1rem;'>Your personal AI companion for mental wellness</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:

        # ── Google style tabs ──
        st.markdown('<div style="border-bottom:2px solid rgba(128,128,128,0.15); margin-bottom:1.5rem;">', unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            login_key = "tab_login_active" if st.session_state.auth_mode == "Login" else "tab_login"
            if st.button("Login", key=login_key, use_container_width=True):
                st.session_state.auth_mode = "Login"
                st.rerun()
        with t2:
            signup_key = "tab_signup_active" if st.session_state.auth_mode == "Create Account" else "tab_signup"
            if st.button("Create Account", key=signup_key, use_container_width=True):
                st.session_state.auth_mode = "Create Account"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        mode = st.session_state.auth_mode

        if mode == "Create Account":
            new_name  = st.text_input("Your Name", placeholder="Sasani...")
            new_email = st.text_input("Email", placeholder="your@email.com...")
            new_pass  = st.text_input("Password", type="password", placeholder="At least 6 characters...")
            new_pass2 = st.text_input("Confirm Password", type="password", placeholder="Same password again...")

            if st.button("Create Account 🌿", use_container_width=True):
                if not new_name.strip():
                    st.warning("Please enter your name!")
                elif not new_email.strip():
                    st.warning("Please enter your email!")
                elif len(new_pass) < 6:
                    st.warning("Password must be at least 6 characters!")
                elif new_pass != new_pass2:
                    st.warning("Passwords do not match!")
                else:
                    with st.spinner("Creating your account..."):
                        success, msg = sign_up(new_name, new_email, new_pass)
                        if success:
                            st.success(msg)
                            ok, uname, _ = sign_in(new_email, new_pass)
                            if ok:
                                st.session_state.logged_in  = True
                                st.session_state.user_name  = uname
                                st.session_state.user_email = new_email
                                st.rerun()
                        else:
                            st.error(msg)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; font-size:0.9rem; opacity:0.6;">Already have an account? <span style="color:#02C39A; cursor:pointer; font-weight:600;">Login above</span></div>', unsafe_allow_html=True)

        else:
            login_email = st.text_input("Email", placeholder="your@email.com...", key="login_email")
            login_pass  = st.text_input("Password", type="password", placeholder="Your password...", key="login_pass")

            if st.button("Login 🌿", use_container_width=True):
                if not login_email.strip() or not login_pass.strip():
                    st.warning("Please enter your email and password!")
                else:
                    with st.spinner("Logging in..."):
                        success, uname, msg = sign_in(login_email, login_pass)
                        if success:
                            st.session_state.logged_in  = True
                            st.session_state.user_name  = uname
                            st.session_state.user_email = login_email
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; font-size:0.9rem; opacity:0.6;">New to MindEase? <span style="color:#02C39A; cursor:pointer; font-weight:600;">Create Account above</span></div>', unsafe_allow_html=True)

    st.stop()

# ── From here app only shows if logged in ─────────────────────
name  = st.session_state.user_name  if st.session_state.user_name  else "friend"
email = st.session_state.user_email if st.session_state.user_email else ""

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

NAV_ITEMS = [
    ("💬 Chat",           "Chat"),
    ("😊 Mood",           "Mood"),
    ("📝 Journal",        "Journal"),
    ("🌅 Daily Wellness", "Daily Wellness"),
    ("🧘 Meditation",     "Meditation"),
    ("🎯 Affirmations",   "Affirmations"),
    ("🧠 Assessment",     "Assessment"),
    ("🏆 Achievements",   "Achievements"),
    ("📈 Progress",       "Progress"),
]

SYSTEM_PROMPT = f"""You are MindEase, a very close and caring best friend.
The user's name is {name}.
Always call them by their name — {name}.
Be warm, gentle, empathetic. Talk casually like a real close friend.
Never sound robotic. Use simple language and gentle emojis 🌿 💙 😊.
Always acknowledge feelings first. Ask one gentle question at a time.
Keep responses short and warm like a text message from a close friend.
If user mentions self-harm share: https://www.iasp.info/resources/Crisis_Centres/
Never diagnose. Encourage professional help gently when needed.
IMPORTANT LANGUAGE RULE: If the user writes in Sinhala language, you MUST reply in Sinhala language. If the user writes in English, reply in English. Always match the language the user is writing in."""

def groq_call(messages, system=SYSTEM_PROMPT):
    client = Groq(api_key=api_key)
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + messages
    ).choices[0].message.content

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

    st.markdown(f"""
    <div class='mcard' style='text-align:center; padding:0.8rem;'>
        <div style='font-size:1.6rem;'>😊</div>
        <div style='font-weight:700;'>{name}</div>
        <div style='font-size:0.75rem; opacity:0.5;'>{email}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout", key="logout", use_container_width=True):
        sign_out()

    st.divider()
    st.markdown("**🎵 Music Player**")
    selected_music = st.selectbox("Choose", list(MUSIC_OPTIONS.keys()), label_visibility="collapsed")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Play", key="music_play", use_container_width=True):
            st.session_state.music_playing = True
            st.session_state.selected_music = selected_music
            st.rerun()
    with col2:
        if st.button("■ Stop", key="music_stop", use_container_width=True):
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
        if st.session_state.current_conversation:
            db_insert("chat_history", {
                "user_email": email,
                "preview": st.session_state.current_conversation[0]["content"][:40] + "...",
                "conversation": st.session_state.current_conversation
            })
        st.session_state.messages = []
        st.session_state.current_conversation = []
        st.rerun()

    chat_history = db_fetch("chat_history", email)
    if chat_history:
        if st.button("🗑️ Delete History", key="delete_history", use_container_width=True):
            db_delete_all("chat_history", email)
            st.success("History deleted!")
            st.rerun()
        for conv in chat_history[:8]:
            date = conv["created_at"][:16].replace("T", " ")
            preview = conv.get("preview", "Chat")
            st.markdown(f"""
            <div class='chat-history-item'>
                <div style='font-weight:600; font-size:0.82rem;'>💬 {date}</div>
                <div style='opacity:0.7; font-size:0.78rem;'>{preview}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No history yet. Start chatting!")

    st.divider()
    st.markdown("**Menu**")
    for key, label in NAV_ITEMS:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()
    active_key = st.session_state.page
    st.markdown(f"""<style>
    section[data-testid="stSidebar"] [data-testid="stButton-nav_{active_key}"] > button {{
        background: rgba(2,195,154,0.15) !important;
        border-color: rgba(2,195,154,0.4) !important;
        color: #02C39A !important;
    }}
    </style>""", unsafe_allow_html=True)

page = st.session_state.page

st.markdown(f"""
<div class='main-header'>
    <h1>🌿 MindEase</h1>
    <p>Welcome back, {name}! So glad you are here. 💙</p>
</div>
""", unsafe_allow_html=True)

# ══ PAGE 1 — CHAT ══════════════════════════════════════════════
if page == "💬 Chat":
    chat_container = st.container(height=480)
    with chat_container:
        if not st.session_state.messages:
            with st.chat_message("assistant", avatar="🌿"):
                st.markdown(f"Hi {name}! 😊 I am MindEase, your personal wellness companion. How are you feeling today?")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🌿" if msg["role"]=="assistant" else "🧑"):
                st.markdown(msg["content"])
    user_input = st.chat_input(f"Share how you are feeling, {name}...")
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
    st.markdown(f'<div class="section-title">😊 How are you feeling, {name}?</div>', unsafe_allow_html=True)
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
            if db_insert("mood_logs", {"user_email": email, "mood": mood, "note": note}):
                st.success(f"Mood saved, {name}! 🌿")
    with c2:
        if st.button("💬 Get Personal Message"):
            with st.spinner("Thinking..."):
                try:
                    msg = groq_call([{"role":"user","content":f"I am feeling {mood}. Write me a warm short personal message. 3 sentences max."}])
                    st.markdown(f'<div class="mcard" style="border-left:4px solid {md["color"]};">🌿 {msg}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(str(e))
    st.markdown('<div class="section-title">📊 Mood History</div>', unsafe_allow_html=True)
    mood_data = db_fetch("mood_logs", email)
    if mood_data:
        if st.button("🗑️ Delete Mood Logs"):
            db_delete_all("mood_logs", email)
            st.success("Deleted!")
            st.rerun()
        df = pd.DataFrame(mood_data)
        st.dataframe(df[["created_at","mood","note"]], use_container_width=True)
        mc = df["mood"].value_counts().reset_index()
        mc.columns = ["Mood","Count"]
        st.bar_chart(mc.set_index("Mood"))
    else:
        st.info("No mood logs yet!")

# ══ PAGE 3 — JOURNAL ═══════════════════════════════════════════
if page == "📝 Journal":
    st.markdown(f'<div class="section-title">📝 Journal — {name}</div>', unsafe_allow_html=True)
    st.caption("Your private space. Write anything you feel.")
    jtitle = st.text_input("Title", placeholder="My thoughts today...")
    jentry = st.text_area("Write here...", height=200, placeholder="Today I felt...")
    if st.button("💾 Save Journal Entry"):
        if jentry.strip():
            if db_insert("journal_logs", {"user_email": email, "title": jtitle, "entry": jentry}):
                st.success("Journal entry saved! 🌿")
        else:
            st.warning("Please write something first!")
    st.markdown('<div class="section-title">📖 Past Entries</div>', unsafe_allow_html=True)
    journal_data = db_fetch("journal_logs", email)
    if journal_data:
        if st.button("🗑️ Delete Journal Entries"):
            db_delete_all("journal_logs", email)
            st.success("Deleted!")
            st.rerun()
        for row in journal_data:
            date = row["created_at"][:16].replace("T"," ")
            with st.expander(f"📝 {date} — {row['title']}"):
                st.write(row["entry"])
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
                yesterday_goal = ""
                try:
                    last_evening = supabase.table("evening_logs").select("goal").eq("user_email", email).order("created_at", desc=True).limit(1).execute()
                    if last_evening.data:
                        yesterday_goal = last_evening.data[0]["goal"]
                except:
                    pass
                morning_prompt = f"""Write a warm personal good morning message for {name}.
                Include these 3 things naturally in 3 to 4 sentences:
                1. A cheerful good morning greeting using their name {name}.
                2. Ask them how many hours they slept last night and mention that good sleep gives energy for the day.
                3. {"Remind them that yesterday they set this goal for today: " + yesterday_goal + " — encourage them warmly to work on it today!" if yesterday_goal else "Encourage them to set one small goal for today."}
                Be warm and friendly like a close friend. Keep it short."""
                gm = groq_call([{"role":"user","content":morning_prompt}])
                st.markdown(f'<div class="mcard">🌅 {gm}</div>', unsafe_allow_html=True)
            except:
                st.markdown(f'<div class="mcard">🌅 Good morning, {name}! Today is a new beginning. Make it count! 🌿</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="mcard">🌅 Good morning section is active from 5 AM to 12 PM. Come back tomorrow morning, {name}! 🌿</div>', unsafe_allow_html=True)

    morning_mood = st.selectbox("😊 How are you feeling this morning?", ["😊 Happy","😐 Okay","😔 Sad","😰 Stressed","😡 Angry"])
    sleep_hours_morning = st.slider("😴 How many hours did you sleep last night?", 0, 12, 7)
    sleep_quality_morning = st.radio("How was your sleep?", ["😴 Very Good","🙂 Good","😐 Okay","😔 Poor","😫 Very Poor"], horizontal=True)
    if sleep_hours_morning < 6:
        st.warning("😴 You did not sleep enough last night. Try to rest more tonight!")
    elif sleep_hours_morning >= 8:
        st.success("😴 Great sleep last night! You should have good energy today!")

    st.markdown('<div class="section-title">✅ Things To Do Today</div>', unsafe_allow_html=True)
    tasks_input = st.text_area("Add your tasks for today", placeholder="1. Study for exam\n2. Call mom\n3. Drink water", height=120)

    if st.button("✨ Get AI Suggestions for My Day"):
        with st.spinner("Thinking of suggestions..."):
            try:
                suggestions = groq_call([{"role":"user","content":f"{name} is feeling {morning_mood} this morning. They slept {sleep_hours_morning} hours last night ({sleep_quality_morning}). Their tasks are: {tasks_input}. Suggest 3 extra small helpful things they can add to their day. Keep it short and friendly."}])
                st.markdown(f'<div class="mcard">💡 {suggestions}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))

    if st.button("💾 Save Morning Check In"):
        if db_insert("morning_logs", {"user_email": email, "mood": morning_mood, "tasks": tasks_input}):
            db_insert("sleep_logs", {"user_email": email, "hours": sleep_hours_morning, "quality": sleep_quality_morning, "note": ""})
            st.success(f"Morning check in saved, {name}! Have an amazing day! 🌅")

    st.divider()
    st.markdown('<div class="section-title">🌙 Evening Check In</div>', unsafe_allow_html=True)
    if is_evening:
        st.markdown(f'<div class="mcard">🌙 Good evening, {name}! Time to wind down and reflect on your day. 🌿</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="mcard">🌙 Evening section is most useful from 5 PM to 11 PM. Fill it in before bed!</div>', unsafe_allow_html=True)

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
            db_insert("evening_logs", {
                "user_email": email,
                "sleep_hours": 0,
                "sleep_quality": "N/A",
                "water_glasses": water_glasses,
                "day_rating": day_rating,
                "highlight": day_highlight,
                "challenge": day_challenge,
                "grateful": grateful_for,
                "goal": tomorrow_goal
            })
            st.success("Evening check in saved! 🌙")
            with st.spinner("MindEase is preparing your goodnight message..."):
                try:
                    night_prompt = f"""User name: {name}. Evening check in:
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
    evening_data = db_fetch("evening_logs", email)
    if evening_data:
        if st.button("🗑️ Delete Evening Logs"):
            db_delete_all("evening_logs", email)
            st.success("Deleted!")
            st.rerun()
        for row in evening_data:
            date = row["created_at"][:16].replace("T"," ")
            with st.expander(f"🌙 {date} — Day {row['day_rating']}/10"):
                st.markdown(f"**💧 Water:** {row['water_glasses']} glasses")
                st.markdown(f"**🌟 Best part:** {row['highlight']}")
                st.markdown(f"**💪 Hardest part:** {row['challenge']}")
                st.markdown(f"**🙏 Grateful for:** {row['grateful']}")
                st.markdown(f"**🎯 Tomorrow goal:** {row['goal']}")
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
            st.success(f"Great job, {name}! 🌿")
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
            st.success(f"Meditation complete, {name}! Well done! 🌿💙")

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
        ("How often do you feel sad or hopeless?",            ["Never","Sometimes","Often","Always"]),
        ("How often do you feel worried or anxious?",          ["Never","Sometimes","Often","Always"]),
        ("How well are you sleeping?",                         ["Very Well","Okay","Poorly","Very Poorly"]),
        ("How often do you feel lonely?",                      ["Never","Sometimes","Often","Always"]),
        ("How often do you lose interest in enjoyable things?",["Never","Sometimes","Often","Always"]),
        ("How often do you feel tired or low energy?",         ["Never","Sometimes","Often","Always"]),
        ("How often do you feel angry or irritated?",          ["Never","Sometimes","Often","Always"]),
        ("How often do you feel overwhelmed?",                 ["Never","Sometimes","Often","Always"]),
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
        st.markdown(f'<div class="result-box" style="background:{col}20;border:2px solid {col};">{em} {name}, your wellness level is <strong>{lv}</strong></div>', unsafe_allow_html=True)
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
    mood_count    = len(db_fetch("mood_logs", email))
    sleep_count   = len(db_fetch("sleep_logs", email))
    journal_count = len(db_fetch("journal_logs", email))
    streak        = get_streak(email)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="score-box"><div style="font-size:3rem;">🔥</div><div style="font-size:2.5rem;font-weight:800;color:var(--primary);">{streak}</div><div style="opacity:0.6;">Day Streak</div></div>', unsafe_allow_html=True)
    with c2:
        sc = 0
        mood_data = db_fetch("mood_logs", email)
        if mood_data:
            happy = sum(1 for r in mood_data if r["mood"]=="😊 Happy")
            sc += min(int(happy/len(mood_data)*30),30)
        sleep_data = db_fetch("sleep_logs", email)
        if sleep_data:
            avg = sum(r["hours"] for r in sleep_data)/len(sleep_data)
            sc += 25 if avg>=8 else 15 if avg>=6 else 5
        sc += min(journal_count*5,25)
        sc += min(streak*2,20)
        sc_col = "#02C39A" if sc>=80 else "#F4A261" if sc>=60 else "#E9C46A" if sc>=40 else "#E63946"
        st.markdown(f'<div class="score-box" style="border-color:{sc_col};"><div style="font-size:3rem;">🏆</div><div style="font-size:2.5rem;font-weight:800;color:{sc_col};">{sc}</div><div style="opacity:0.6;">Wellness Score / 100</div></div>', unsafe_allow_html=True)
    with c3:
        earned_count = sum(1 for b in BADGES if b["fn"](mood_count,sleep_count,journal_count,streak))
        st.markdown(f'<div class="score-box"><div style="font-size:3rem;">🏅</div><div style="font-size:2.5rem;font-weight:800;color:var(--primary);">{earned_count}/{len(BADGES)}</div><div style="opacity:0.6;">Badges Earned</div></div>', unsafe_allow_html=True)

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
    cutoff = (datetime.now() - pd.Timedelta(days=days)).isoformat()

    st.markdown(f'<div class="section-title">Mood — {period}</div>', unsafe_allow_html=True)
    try:
        mood_res = supabase.table("mood_logs").select("*").eq("user_email",email).gte("created_at",cutoff).execute()
        if mood_res.data:
            df = pd.DataFrame(mood_res.data)
            mc = df["mood"].value_counts().reset_index(); mc.columns=["Mood","Count"]
            st.bar_chart(mc.set_index("Mood"))
            c1,c2,c3,c4 = st.columns(4)
            with c1: st.metric("Total Logs", len(df))
            with c2: st.metric("😊 Happy",   len(df[df["mood"]=="😊 Happy"]))
            with c3: st.metric("😔 Sad",      len(df[df["mood"]=="😔 Sad"]))
            with c4: st.metric("😰 Stressed", len(df[df["mood"]=="😰 Stressed"]))
        else: st.info(f"No mood logs in the last {days} days.")
    except: st.info("No mood logs yet.")

    st.markdown(f'<div class="section-title">Sleep — {period}</div>', unsafe_allow_html=True)
    try:
        sleep_res = supabase.table("sleep_logs").select("*").eq("user_email",email).gte("created_at",cutoff).execute()
        if sleep_res.data:
            df_s = pd.DataFrame(sleep_res.data)
            avg = df_s["hours"].mean()
            st.metric("Average Sleep", f"{avg:.1f} hrs")
            st.line_chart(df_s.set_index("created_at")["hours"])
            if avg>=8: st.success("Great sleep average! 🌟")
            elif avg>=6: st.info("Decent. Aim for 8 hours! 🌙")
            else: st.warning("Not enough sleep. Rest more! 😴")
        else: st.info(f"No sleep logs in the last {days} days.")
    except: st.info("No sleep logs yet.")

    st.markdown(f'<div class="section-title">Journal — {period}</div>', unsafe_allow_html=True)
    try:
        journal_res = supabase.table("journal_logs").select("*").eq("user_email",email).gte("created_at",cutoff).execute()
        count = len(journal_res.data) if journal_res.data else 0
        st.metric("Entries Written", count)
        if count>=5: st.success("Amazing journaling habit! 📝🌟")
        elif count>=1: st.info("Good start! Try daily journaling! 📝")
        else: st.warning("No entries this period. Start writing! 📝")
    except: st.info("No journal entries yet.")

    st.markdown('<div class="section-title">🤖 AI Progress Summary</div>', unsafe_allow_html=True)
    if st.button("Get My AI Summary 🧠"):
        mm = sl = jj = ""
        mood_all = db_fetch("mood_logs", email)
        if mood_all:
            counts = {}
            for r in mood_all:
                counts[r["mood"]] = counts.get(r["mood"],0)+1
            mm = str(counts)
        sleep_all = db_fetch("sleep_logs", email)
        if sleep_all:
            avg = sum(r["hours"] for r in sleep_all)/len(sleep_all)
            sl = f"Average sleep: {avg:.1f} hours"
        journal_all = db_fetch("journal_logs", email)
        jj = f"Total entries: {len(journal_all)}"
        with st.spinner("Reviewing your progress..."):
            try:
                summary = groq_call([{"role":"user","content":f"User: {name}. Mood data: {mm}. Sleep: {sl}. Journal: {jj}. Write 3-4 warm sentences using their name. Highlight what they do well and gently suggest one improvement."}])
                st.markdown(f'<div class="mcard">🌿 {summary}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))
