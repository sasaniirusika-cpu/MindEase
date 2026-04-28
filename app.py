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

/* Switch link buttons */
[data-testid="stButton-switch_to_login"] > button,
[data-testid="stButton-switch_to_signup"] > button {
    background: transparent !important;
    color: #02C39A !important;
    border: none !important;
    box-shadow: none !important;
    transform: none !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-decoration: underline !important;
    opacity: 0.85 !important;
}
[data-testid="stButton-switch_to_login"] > button:hover,
[data-testid="stButton-switch_to_signup"] > button:hover {
    opacity: 1 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── MOBILE IMPROVEMENTS ───────────────────────────────────── */
@media (max-width: 768px) {
    .main-header {
        padding: 1.2rem 1rem !important;
        border-radius: 14px !important;
        margin-bottom: 0.8rem !important;
    }
    .main-header h1 {
        font-size: 1.6rem !important;
    }
    .main-header p {
        font-size: 0.88rem !important;
    }
    .mcard {
        padding: 0.9rem 1rem !important;
        border-radius: 12px !important;
        margin: 0.5rem 0 !important;
    }
    .mcard-plain {
        padding: 0.9rem 1rem !important;
        border-radius: 12px !important;
    }
    .section-title {
        font-size: 1rem !important;
        margin: 1rem 0 0.5rem 0 !important;
    }
    .score-box {
        padding: 1.2rem 0.8rem !important;
    }
    .score-box div[style*="font-size:3rem"] {
        font-size: 2rem !important;
    }
    .score-box div[style*="font-size:2.5rem"] {
        font-size: 1.8rem !important;
    }
    .badge-earned {
        padding: 0.6rem !important;
        margin: 0.2rem !important;
    }
    .affirmation-box {
        padding: 1.2rem !important;
        font-size: 1rem !important;
    }
    .quote-box {
        padding: 1rem 1.2rem !important;
        font-size: 0.95rem !important;
    }
    .stButton > button {
        font-size: 0.95rem !important;
        padding: 0.6rem 1rem !important;
        min-height: 48px !important;
    }
    div[data-testid="stChatInput"] {
        border-radius: 18px !important;
    }
    iframe {
        height: 180px !important;
    }
    .block-container {
        padding: 0.5rem 0.8rem 2rem !important;
    }
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.2rem !important; }
    h3 { font-size: 1.05rem !important; }
    p, li, div { font-size: 0.93rem; }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
    }
}

@media (max-width: 480px) {
    .main-header h1 {
        font-size: 1.35rem !important;
    }
    .main-header p {
        font-size: 0.8rem !important;
    }
    .stButton > button {
        min-height: 52px !important;
        font-size: 1rem !important;
    }
    .score-box {
        padding: 0.9rem 0.5rem !important;
    }
    .block-container {
        padding: 0.4rem 0.5rem 2rem !important;
    }
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

# ── Auto restore session on refresh ───────────────────────────
if not st.session_state.logged_in:
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            st.session_state.logged_in  = True
            st.session_state.user_name  = session.user.user_metadata.get("name", session.user.email.split("@")[0])
            st.session_state.user_email = session.user.email
    except:
        pass

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
        mode = st.session_state.auth_mode

        if mode == "Create Account":
            st.markdown("**Create your MindEase account** 🌿")
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
            if st.button("Already have an account? Login", key="switch_to_login", use_container_width=True):
                st.session_state.auth_mode = "Login"
                st.rerun()

        else:
            st.markdown("**Welcome back!** 😊")
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
            if st.button("New to MindEase? Create Account", key="switch_to_signup", use_container_width=True):
                st.session_state.auth_mode = "Create Account"
                st.rerun()

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
