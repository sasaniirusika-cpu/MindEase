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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #02A87A;
    --primary-light: #02C39A;
    --primary-glow: rgba(2, 168, 122, 0.15);
    --primary-border: rgba(2, 168, 122, 0.25);
    --bg-base: #FAF7F2;
    --bg-card: #FFFFFF;
    --bg-card2: #F5F1EC;
    --bg-input: #F5F1EC;
    --text-primary: #2C2C2C;
    --text-secondary: #7A7065;
    --border: rgba(0,0,0,0.07);
    --shadow: 0 4px 20px rgba(0,0,0,0.06);
    --shadow-teal: 0 4px 20px rgba(2,168,122,0.12);
}

* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: var(--bg-base) !important;
    color: var(--text-primary) !important;
}
.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 900px !important;
}

p, span, li, label { color: var(--text-primary); }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--primary-border); border-radius: 3px; }

/* ── Header ── */
.main-header {
    background: linear-gradient(135deg, #028C6A 0%, #02A87A 50%, #02C39A 100%);
    padding: 2rem 2.5rem;
    border-radius: 20px;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 30px rgba(2,168,122,0.25);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
    pointer-events: none;
}
.main-header h1 {
    color: white !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    margin: 0 !important;
}
.main-header p {
    color: rgba(255,255,255,0.82) !important;
    margin: 0.4rem 0 0 0 !important;
    font-size: 0.92rem !important;
    font-weight: 300 !important;
    letter-spacing: 0.3px !important;
}

/* ── Cards ── */
.mcard {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin: 0.6rem 0;
    box-shadow: var(--shadow);
    transition: all 0.2s;
}
.mcard:hover {
    border-color: var(--primary-border);
    box-shadow: var(--shadow-teal);
}
.mcard-plain {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin: 0.6rem 0;
}
.mcard-accent {
    background: linear-gradient(135deg, rgba(2,168,122,0.06), rgba(2,195,154,0.04));
    border: 1px solid var(--primary-border);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin: 0.6rem 0;
    box-shadow: var(--shadow-teal);
}

/* ── Section titles ── */
.section-title {
    color: var(--text-secondary) !important;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin: 1.8rem 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* ── Score boxes ── */
.score-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 1rem;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: var(--shadow);
    transition: all 0.2s;
}
.score-box:hover {
    border-color: var(--primary-border);
    box-shadow: var(--shadow-teal);
    transform: translateY(-2px);
}

/* ── Affirmation ── */
.affirmation-box {
    background: linear-gradient(135deg, #F0FBF7, #E8F8F3);
    border: 1px solid var(--primary-border);
    border-radius: 20px;
    padding: 2.2rem;
    text-align: center;
    font-size: 1.15rem;
    line-height: 1.9;
    margin: 0.8rem 0;
    color: var(--text-primary) !important;
    font-weight: 300;
    letter-spacing: 0.2px;
    box-shadow: var(--shadow-teal);
}

/* ── Quote ── */
.quote-box {
    border-left: 3px solid var(--primary);
    background: var(--bg-card);
    border-radius: 0 14px 14px 0;
    padding: 1.25rem 1.5rem;
    margin: 0.8rem 0;
    font-style: italic;
    font-size: 1rem;
    line-height: 1.8;
    color: var(--text-primary) !important;
    font-weight: 300;
    box-shadow: var(--shadow);
}

/* ── Result ── */
.result-box {
    border-radius: 16px;
    padding: 1.25rem;
    text-align: center;
    font-size: 1rem;
    font-weight: 600;
    margin: 0.8rem 0;
    color: var(--text-primary) !important;
}

/* ── Badges ── */
.badge-earned {
    background: linear-gradient(135deg, #F0FBF7, #E8F8F3);
    border: 1px solid var(--primary-border);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
    margin: 0.3rem;
    transition: all 0.2s;
    box-shadow: var(--shadow);
}
.badge-earned:hover {
    box-shadow: var(--shadow-teal);
    transform: translateY(-2px);
}
.badge-locked {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin: 0.2rem 0;
    opacity: 0.5;
}

/* ── Chat history ── */
.chat-history-item {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.65rem 1rem;
    margin: 0.25rem 0;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
}
.chat-history-item:hover {
    border-color: var(--primary-border);
    background: #F0FBF7;
}

/* ── Chat input ── */
div[data-testid="stChatInput"] {
    background: var(--bg-card) !important;
    border-radius: 14px !important;
    border: 1.5px solid var(--border) !important;
    box-shadow: var(--shadow) !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-glow) !important;
}
div[data-testid="stChatInput"] textarea {
    color: var(--text-primary) !important;
    background: transparent !important;
}
div[data-testid="stChatInput"] button {
    background: var(--primary) !important;
    border-radius: 10px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #028C6A, #02C39A) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.3px !important;
    padding: 0.65rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(2,168,122,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(2,168,122,0.3) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Nav buttons ── */
section[data-testid="stSidebar"] [data-testid^="stButton-nav_"] > button {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    box-shadow: none !important;
    transform: none !important;
    padding: 0.55rem 0.9rem !important;
    margin: 0.06rem 0 !important;
}
section[data-testid="stSidebar"] [data-testid^="stButton-nav_"] > button:hover {
    background: rgba(2,168,122,0.08) !important;
    color: var(--primary) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Sidebar action buttons ── */
section[data-testid="stSidebar"] [data-testid="stButton-music_play"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-music_stop"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-new_chat"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-delete_history"] > button,
section[data-testid="stSidebar"] [data-testid="stButton-logout"] > button {
    background: rgba(2,168,122,0.08) !important;
    color: var(--primary) !important;
    border: 1px solid var(--primary-border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transform: none !important;
    width: 100% !important;
    font-size: 0.82rem !important;
}
section[data-testid="stSidebar"] [data-testid="stButton-music_play"] > button:hover,
section[data-testid="stSidebar"] [data-testid="stButton-music_stop"] > button:hover,
section[data-testid="stSidebar"] [data-testid="stButton-new_chat"] > button:hover,
section[data-testid="stSidebar"] [data-testid="stButton-delete_history"] > button:hover,
section[data-testid="stSidebar"] [data-testid="stButton-logout"] > button:hover {
    background: rgba(2,168,122,0.15) !important;
    transform: none !important;
}

/* ── Switch link buttons ── */
[data-testid="stButton-switch_to_login"] > button,
[data-testid="stButton-switch_to_signup"] > button {
    background: transparent !important;
    color: var(--primary) !important;
    border: none !important;
    box-shadow: none !important;
    transform: none !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-decoration: underline !important;
    opacity: 0.85 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #F5F0EA !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div {
    background: #F5F0EA !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label {
    color: var(--text-secondary);
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-glow) !important;
    background: white !important;
}
.stTextInput > label, .stTextArea > label {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}
.stSelectbox > label {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* ── Slider ── */
.stSlider > label {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--primary) !important;
    box-shadow: 0 0 0 4px var(--primary-glow) !important;
}
.stSlider [data-baseweb="slider"] div[data-testid="stSliderTrackActive"] {
    background: var(--primary) !important;
}

/* ── Radio ── */
.stRadio > label { color: var(--text-secondary) !important; font-size: 0.82rem !important; font-weight: 500 !important; }
.stRadio label { color: var(--text-secondary) !important; font-size: 0.88rem !important; }

/* ── Metrics ── */
[data-testid="stMetricValue"] {
    color: var(--primary) !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.5px !important;
}

/* ── Expander ── */
details {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin: 0.3rem 0 !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}
details summary {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    padding: 0.85rem 1rem !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    list-style: none !important;
}
details summary::-webkit-details-marker { display: none !important; }
details summary::after {
    content: ' ›' !important;
    font-size: 1.2rem !important;
    color: var(--text-secondary) !important;
    float: right !important;
}
details[open] summary::after {
    content: ' ‹' !important;
}
details > div {
    background: var(--bg-card2) !important;
    padding: 0.8rem 1rem 1rem !important;
    border-top: 1px solid var(--border) !important;
}
details > div p,
details > div span,
details > div div,
details > div strong,
details > div em {
    color: var(--text-primary) !important;
}
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin: 0.3rem 0 !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stExpander"] p,
[data-testid="stExpander"] strong,
[data-testid="stExpander"] span,
[data-testid="stExpander"] div {
    color: var(--text-primary) !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; box-shadow: var(--shadow) !important; }

/* ── Alerts ── */
.stAlert {
    border-radius: 12px !important;
    font-size: 0.88rem !important;
}
.stAlert p { color: var(--text-primary) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 0.8rem 0 !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 0.9rem 1.1rem !important;
    margin: 0.3rem 0 !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stChatMessage"] p {
    color: var(--text-primary) !important;
}

/* ── Mobile ── */
@media (max-width: 768px) {
    .block-container { padding: 0.8rem 0.8rem 3rem !important; }
    .main-header { padding: 1.3rem 1rem !important; border-radius: 16px !important; }
    .main-header h1 { font-size: 1.5rem !important; }
    .stButton > button { min-height: 48px !important; font-size: 0.95rem !important; }
    .score-box { padding: 1rem 0.5rem !important; }
}
@media (max-width: 480px) {
    .main-header h1 { font-size: 1.3rem !important; }
    .block-container { padding: 0.5rem 0.5rem 3rem !important; }
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
            return True, "Account created successfully!"
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
            return True, name, "Welcome back!"
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
    <div style='text-align:center; padding:3rem 0 1.5rem;'>
        <div style='font-size:2.8rem; margin-bottom:0.5rem;'>🌿</div>
        <h1 style='color:#2C2C2C; font-size:2.2rem; font-weight:700; margin:0; letter-spacing:-0.5px;'>MindEase</h1>
        <p style='color:#7A7065; font-size:0.9rem; margin:0.5rem 0 0 0; font-weight:400; letter-spacing:1.5px; text-transform:uppercase;'>Your Personal Wellness Companion</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown(f"""
        <div style='background:white; border:1px solid rgba(0,0,0,0.07);
        border-radius:20px; padding:2rem 2rem 0.5rem; box-shadow:0 10px 40px rgba(0,0,0,0.08);'>
        <p style='color:#7A7065; font-size:0.72rem; letter-spacing:1.8px; text-transform:uppercase;
        margin:0 0 1.2rem 0; font-weight:600;'>
        {"CREATE ACCOUNT" if st.session_state.auth_mode == "Create Account" else "SIGN IN"}</p>
        </div>
        """, unsafe_allow_html=True)

        mode = st.session_state.auth_mode

        if mode == "Create Account":
            new_name  = st.text_input("Full Name", placeholder="Your name")
            new_email = st.text_input("Email Address", placeholder="you@email.com")
            new_pass  = st.text_input("Password", type="password", placeholder="Min. 6 characters")
            new_pass2 = st.text_input("Confirm Password", type="password", placeholder="Repeat password")

            if st.button("Create Account", use_container_width=True):
                if not new_name.strip():
                    st.warning("Please enter your name.")
                elif not new_email.strip():
                    st.warning("Please enter your email.")
                elif len(new_pass) < 6:
                    st.warning("Password must be at least 6 characters.")
                elif new_pass != new_pass2:
                    st.warning("Passwords do not match.")
                else:
                    with st.spinner("Creating account..."):
                        success, msg = sign_up(new_name, new_email, new_pass)
                        if success:
                            ok, uname, _ = sign_in(new_email, new_pass)
                            if ok:
                                st.session_state.logged_in  = True
                                st.session_state.user_name  = uname
                                st.session_state.user_email = new_email
                                st.rerun()
                        else:
                            st.error(msg)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Already have an account? Sign In", key="switch_to_login", use_container_width=True):
                st.session_state.auth_mode = "Login"
                st.rerun()
        else:
            login_email = st.text_input("Email Address", placeholder="you@email.com", key="login_email")
            login_pass  = st.text_input("Password", type="password", placeholder="Your password", key="login_pass")

            if st.button("Sign In", use_container_width=True):
                if not login_email.strip() or not login_pass.strip():
                    st.warning("Please enter your email and password.")
                else:
                    with st.spinner("Signing in..."):
                        success, uname, msg = sign_in(login_email, login_pass)
                        if success:
                            st.session_state.logged_in  = True
                            st.session_state.user_name  = uname
                            st.session_state.user_email = login_email
                            st.rerun()
                        else:
                            st.error(msg)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("New to MindEase? Create Account", key="switch_to_signup", use_container_width=True):
                st.session_state.auth_mode = "Create Account"
                st.rerun()

    st.stop()

# ── From here app only shows if logged in ─────────────────────
name  = st.session_state.user_name  if st.session_state.user_name  else "there"
email = st.session_state.user_email if st.session_state.user_email else ""

AFFIRMATIONS = [
    "You are stronger than you think.",
    "Every day is a new beginning.",
    "You are worthy of love and happiness.",
    "It is okay to not be okay. Take it one step at a time.",
    "You have survived every difficult day so far.",
    "Your feelings are valid. You matter.",
    "Small steps still move you forward. Keep going.",
    "You are not alone. Better days are coming.",
    "Be kind to yourself today. You deserve it.",
    "You are capable of amazing things. Believe in yourself.",
    "Today is a good day to try again.",
    "Your mental health matters. Taking care of yourself is brave.",
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
    ("Relaxing Nature Sounds", "https://www.youtube.com/embed/1ZYbU82GVz4"),
    ("Calm Piano Music", "https://www.youtube.com/embed/lFcSrYw-ARY"),
    ("Peaceful Ocean Waves", "https://www.youtube.com/embed/bn9F19Hi1Lk"),
    ("Uplifting Morning Music", "https://www.youtube.com/embed/inpok4MKVLM"),
    ("Funny Animals", "https://www.youtube.com/embed/WYkiiGnOyBw"),
]

MOOD_COLORS = {
    "Happy":    {"color": "#E8A020", "bg": "rgba(232,160,32,0.07)",  "label": "Happy",    "message": "You are radiating great energy today. Keep it going."},
    "Okay":     {"color": "#4A9EBF", "bg": "rgba(74,158,191,0.07)", "label": "Calm",     "message": "A steady, balanced day. That is perfectly fine."},
    "Sad":      {"color": "#7B8FD4", "bg": "rgba(123,143,212,0.07)","label": "Low",      "message": "It is okay to feel sad. Be gentle with yourself today."},
    "Stressed": {"color": "#D46B6B", "bg": "rgba(212,107,107,0.07)","label": "Stressed", "message": "Take a slow breath. You can work through this."},
    "Angry":    {"color": "#C4633A", "bg": "rgba(196,99,58,0.07)",  "label": "Angry",    "message": "Your feelings are valid. Try the breathing exercise."},
}

MUSIC_OPTIONS = {
    "Relaxing Nature": "https://www.youtube.com/embed/1ZYbU82GVz4",
    "Calm Piano":      "https://www.youtube.com/embed/lFcSrYw-ARY",
    "Ocean Waves":     "https://www.youtube.com/embed/bn9F19Hi1Lk",
    "Sleep Music":     "https://www.youtube.com/embed/1vx8iUvfyCY",
    "Rain Sounds":     "https://www.youtube.com/embed/mPZkdNFkNps",
    "Fireplace":       "https://www.youtube.com/embed/UgHKb_7884o",
    "Lofi Hip Hop":    "https://www.youtube.com/embed/jfKfPfyJRdk",
    "Morning Music":   "https://www.youtube.com/embed/inpok4MKVLM",
}

BADGES = [
    {"name": "First Step",   "icon": "◈", "desc": "Logged your first mood",         "fn": lambda m,s,j,st: m>=1},
    {"name": "Mood Tracker", "icon": "◉", "desc": "Logged mood 5 times",            "fn": lambda m,s,j,st: m>=5},
    {"name": "Consistent",   "icon": "◈", "desc": "Logged mood 10 times",           "fn": lambda m,s,j,st: m>=10},
    {"name": "Sleep Logger", "icon": "◑", "desc": "Logged your first sleep",        "fn": lambda m,s,j,st: s>=1},
    {"name": "Dear Diary",   "icon": "◎", "desc": "Wrote your first journal entry", "fn": lambda m,s,j,st: j>=1},
    {"name": "Storyteller",  "icon": "◈", "desc": "Wrote 5 journal entries",        "fn": lambda m,s,j,st: j>=5},
    {"name": "3 Day Streak", "icon": "◉", "desc": "Logged mood 3 days in a row",    "fn": lambda m,s,j,st: st>=3},
    {"name": "Week Warrior", "icon": "◈", "desc": "Logged mood 7 days in a row",    "fn": lambda m,s,j,st: st>=7},
    {"name": "Champion",     "icon": "◉", "desc": "Logged mood 30 days in a row",   "fn": lambda m,s,j,st: st>=30},
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
Never sound robotic. Use simple language and gentle emojis where appropriate.
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
    st.markdown(f"""
    <div style='padding:1.5rem 0.5rem 1rem;'>
        <div style='font-size:1.1rem; font-weight:700; color:#2C2C2C; letter-spacing:-0.3px;'>MindEase</div>
        <div style='font-size:0.68rem; color:#7A7065; letter-spacing:1.2px; text-transform:uppercase; margin-top:0.2rem;'>Wellness Companion</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:white; border:1px solid rgba(0,0,0,0.07);
    border-radius:12px; padding:0.9rem 1rem; margin-bottom:0.5rem; box-shadow:0 2px 8px rgba(0,0,0,0.05);'>
        <div style='font-weight:600; font-size:0.9rem; color:#2C2C2C;'>{name}</div>
        <div style='font-size:0.72rem; color:#7A7065; margin-top:0.15rem;'>{email}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Sign Out", key="logout", use_container_width=True):
        sign_out()

    st.divider()
    st.markdown("<p style='font-size:0.66rem; color:#7A7065; letter-spacing:1.4px; text-transform:uppercase; margin:0.3rem 0 0.5rem;'>MUSIC</p>", unsafe_allow_html=True)
    selected_music = st.selectbox("Track", list(MUSIC_OPTIONS.keys()), label_visibility="collapsed")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play", key="music_play", use_container_width=True):
            st.session_state.music_playing = True
            st.session_state.selected_music = selected_music
            st.rerun()
    with col2:
        if st.button("Stop", key="music_stop", use_container_width=True):
            st.session_state.music_playing = False
            st.session_state.selected_music = None
            st.rerun()

    if st.session_state.music_playing and st.session_state.selected_music:
        url = MUSIC_OPTIONS[st.session_state.selected_music]
        st.markdown(f"""
        <div style='border-radius:8px; overflow:hidden; margin-top:0.5rem;'>
        <iframe width="100%" height="70" src="{url}?autoplay=1"
        frameborder="0" allow="autoplay; encrypted-media"></iframe>
        </div>
        <div style='font-size:0.72rem; color:#7A7065; margin-top:0.3rem;'>
        Now playing — {st.session_state.selected_music}
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='font-size:0.66rem; color:#7A7065; letter-spacing:1.4px; text-transform:uppercase; margin:0.3rem 0 0.5rem;'>CONVERSATIONS</p>", unsafe_allow_html=True)
    if st.button("New Conversation", key="new_chat", use_container_width=True):
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
        if st.button("Clear History", key="delete_history", use_container_width=True):
            db_delete_all("chat_history", email)
            st.rerun()
        for conv in chat_history[:6]:
            date = conv["created_at"][:16].replace("T", " ")
            preview = conv.get("preview", "Conversation")
            st.markdown(f"""
            <div class='chat-history-item'>
                <div style='font-weight:500; color:#2C2C2C; font-size:0.78rem;'>{date}</div>
                <div style='color:#7A7065; font-size:0.73rem; margin-top:0.1rem;'>{preview}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:0.78rem; color:#7A7065;'>No conversations yet.</p>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='font-size:0.66rem; color:#7A7065; letter-spacing:1.4px; text-transform:uppercase; margin:0.3rem 0 0.5rem;'>NAVIGATE</p>", unsafe_allow_html=True)
    for key, label in NAV_ITEMS:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    active_key = st.session_state.page
    st.markdown(f"""<style>
    section[data-testid="stSidebar"] [data-testid="stButton-nav_{active_key}"] > button {{
        background: rgba(2,168,122,0.1) !important;
        color: #02A87A !important;
        border: 1px solid rgba(2,168,122,0.2) !important;
    }}
    </style>""", unsafe_allow_html=True)

page = st.session_state.page

st.markdown(f"""
<div class='main-header'>
    <h1>MindEase</h1>
    <p>Welcome back, {name}. Good to see you.</p>
</div>
""", unsafe_allow_html=True)

# ══ PAGE 1 — CHAT ══════════════════════════════════════════════
if page == "💬 Chat":
    chat_container = st.container(height=480)
    with chat_container:
        if not st.session_state.messages:
            with st.chat_message("assistant", avatar="🌿"):
                st.markdown(f"Hi {name}. I am MindEase, your wellness companion. How are you feeling today?")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🌿" if msg["role"]=="assistant" else "🧑"):
                st.markdown(msg["content"])
    user_input = st.chat_input("Talk to MindEase...")
    if user_input:
        with chat_container:
            with st.chat_message("user", avatar="🧑"):
                st.markdown(user_input)
        st.session_state.messages.append({"role":"user","content":user_input})
        st.session_state.current_conversation.append({"role":"user","content":user_input})
        with chat_container:
            with st.chat_message("assistant", avatar="🌿"):
                with st.spinner(""):
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
    st.markdown(f'<div class="section-title">How are you feeling, {name}?</div>', unsafe_allow_html=True)
    mood_label = st.radio("", ["Happy","Okay","Sad","Stressed","Angry"], horizontal=True)
    note = st.text_input("Add a note", placeholder="What is on your mind?")
    md = MOOD_COLORS[mood_label]
    st.markdown(f"""
    <div style='text-align:center; background:{md["bg"]}; border:1px solid {md["color"]}33;
    border-radius:16px; padding:2rem; margin:0.8rem 0; box-shadow:0 4px 15px rgba(0,0,0,0.05);'>
        <div style='font-size:0.68rem; letter-spacing:2px; text-transform:uppercase;
        color:{md["color"]}; font-weight:600; margin-bottom:0.6rem;'>{md["label"]}</div>
        <div style='width:64px;height:64px;border-radius:50%;background:{md["color"]};
        margin:0 auto 0.8rem; opacity:0.9; box-shadow:0 4px 15px {md["color"]}44;'></div>
        <div style='font-size:0.9rem; color:#7A7065; font-weight:300;'>{md["message"]}</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Save Mood", use_container_width=True):
            if db_insert("mood_logs", {"user_email": email, "mood": mood_label, "note": note}):
                st.success(f"Mood saved, {name}.")
    with c2:
        if st.button("Get a Message", use_container_width=True):
            with st.spinner(""):
                try:
                    msg = groq_call([{"role":"user","content":f"I am feeling {mood_label}. Write me a warm short personal message. 3 sentences max."}])
                    st.markdown(f'<div class="mcard-accent"><p style="color:#2C2C2C; margin:0;">{msg}</p></div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(str(e))
    st.markdown('<div class="section-title">Mood History</div>', unsafe_allow_html=True)
    mood_data = db_fetch("mood_logs", email)
    if mood_data:
        if st.button("Clear Logs", use_container_width=True):
            db_delete_all("mood_logs", email)
            st.rerun()
        df = pd.DataFrame(mood_data)
        st.dataframe(df[["created_at","mood","note"]], use_container_width=True)
        mc = df["mood"].value_counts().reset_index()
        mc.columns = ["Mood","Count"]
        st.bar_chart(mc.set_index("Mood"))
    else:
        st.markdown('<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">No mood logs yet. Log your first mood above.</p></div>', unsafe_allow_html=True)

# ══ PAGE 3 — JOURNAL ═══════════════════════════════════════════
if page == "📝 Journal":
    st.markdown(f'<div class="section-title">Journal — {name}</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#7A7065; font-size:0.85rem; margin:0 0 0.8rem;">Your private space. Write freely.</p>', unsafe_allow_html=True)
    jtitle = st.text_input("Title", placeholder="Entry title...")
    jentry = st.text_area("Write here", height=200, placeholder="Today I felt...")
    if st.button("Save Entry", use_container_width=True):
        if jentry.strip():
            if db_insert("journal_logs", {"user_email": email, "title": jtitle, "entry": jentry}):
                st.success("Entry saved.")
        else:
            st.warning("Write something first.")
    st.markdown('<div class="section-title">Past Entries</div>', unsafe_allow_html=True)
    journal_data = db_fetch("journal_logs", email)
    if journal_data:
        if st.button("Clear Entries", use_container_width=True):
            db_delete_all("journal_logs", email)
            st.rerun()
        for row in journal_data:
            date = row["created_at"][:16].replace("T"," ")
            with st.expander(f"{date} — {row['title']}"):
                st.markdown(f"<p style='color:#2C2C2C;'>{row['entry']}</p>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">No entries yet. Start writing above.</p></div>', unsafe_allow_html=True)

# ══ PAGE 4 — DAILY WELLNESS ════════════════════════════════════
if page == "🌅 Daily Wellness":
    hour = datetime.now().hour
    is_morning = 5 <= hour < 12
    is_evening = 17 <= hour <= 23

    st.markdown('<div class="section-title">Morning Check In</div>', unsafe_allow_html=True)
    if is_morning:
        with st.spinner(""):
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
                st.markdown(f'<div class="mcard-accent"><p style="color:#2C2C2C; margin:0;">{gm}</p></div>', unsafe_allow_html=True)
            except:
                st.markdown(f'<div class="mcard"><p style="color:#2C2C2C; margin:0;">Good morning, {name}. Today is a new beginning.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">Morning section is active from 5 AM to 12 PM. See you tomorrow morning, {name}.</p></div>', unsafe_allow_html=True)

    morning_mood = st.selectbox("How are you feeling this morning?", ["Happy","Okay","Sad","Stressed","Angry"])
    sleep_hours_morning = st.slider("Hours slept last night", 0, 12, 7)
    sleep_quality_morning = st.radio("Sleep quality", ["Very Good","Good","Okay","Poor","Very Poor"], horizontal=True)
    if sleep_hours_morning < 6:
        st.warning("You slept less than 6 hours. Try to rest more tonight.")
    elif sleep_hours_morning >= 8:
        st.success("Great sleep. You should have good energy today.")

    st.markdown('<div class="section-title">Tasks for Today</div>', unsafe_allow_html=True)
    tasks_input = st.text_area("Your tasks", placeholder="1. Study\n2. Exercise\n3. Read", height=100)

    if st.button("Get AI Suggestions", use_container_width=True):
        with st.spinner(""):
            try:
                suggestions = groq_call([{"role":"user","content":f"{name} is feeling {morning_mood} this morning. They slept {sleep_hours_morning} hours ({sleep_quality_morning}). Tasks: {tasks_input}. Suggest 3 helpful additions to their day. Short and friendly."}])
                st.markdown(f'<div class="mcard-accent"><p style="color:#2C2C2C; margin:0;">{suggestions}</p></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))

    if st.button("Save Morning Check In", use_container_width=True):
        if db_insert("morning_logs", {"user_email": email, "mood": morning_mood, "tasks": tasks_input}):
            db_insert("sleep_logs", {"user_email": email, "hours": sleep_hours_morning, "quality": sleep_quality_morning, "note": ""})
            st.success(f"Saved. Have a great day, {name}.")

    st.divider()
    st.markdown('<div class="section-title">Evening Check In</div>', unsafe_allow_html=True)
    if is_evening:
        st.markdown(f'<div class="mcard-accent"><p style="color:#2C2C2C; margin:0;">Good evening, {name}. Time to reflect on your day.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">Evening section is most useful from 5 PM to 11 PM.</p></div>', unsafe_allow_html=True)

    water_glasses = st.slider("Glasses of water today", 0, 15, 8)
    day_rating    = st.slider("Day rating", 1, 10, 5)
    day_highlight = st.text_input("Best part of your day", placeholder="Something good that happened...")
    day_challenge = st.text_input("Hardest part of your day", placeholder="Something difficult...")
    grateful_for  = st.text_area("3 things you are grateful for", placeholder="1.\n2.\n3.", height=90)
    tomorrow_goal = st.text_input("One goal for tomorrow", placeholder="Something small and achievable...")

    if water_glasses < 6:
        st.warning("Less than 6 glasses today. Try to drink more tomorrow.")
    elif water_glasses >= 8:
        st.success("Great hydration today.")

    if st.button("Save Evening Check In", use_container_width=True):
        if day_highlight.strip() == "" and grateful_for.strip() == "":
            st.warning("Please fill in at least some fields.")
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
            st.success("Evening check in saved.")
            with st.spinner(""):
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
                    2. A short paragraph summarising how their day went — 3 sentences.
                    3. Practical advice on how to make tomorrow better — 3 sentences.
                    Separate each part with a line break. Be warm, honest, caring."""
                    night_msg = groq_call([{"role":"user","content":night_prompt}])
                    parts = night_msg.split("\n\n") if "\n\n" in night_msg else night_msg.split("\n")
                    st.markdown(f'<div class="mcard-accent"><strong style="color:#02A87A; font-size:0.68rem; letter-spacing:1.5px; text-transform:uppercase;">Goodnight</strong><br><br><span style="color:#2C2C2C;">{parts[0]}</span></div>', unsafe_allow_html=True)
                    if len(parts) > 1:
                        st.markdown(f'<div class="mcard-plain"><strong style="color:#7A7065; font-size:0.68rem; letter-spacing:1.5px; text-transform:uppercase;">Day Summary</strong><br><br><span style="color:#2C2C2C;">{parts[1]}</span></div>', unsafe_allow_html=True)
                    if len(parts) > 2:
                        st.markdown(f'<div class="mcard"><strong style="color:#02A87A; font-size:0.68rem; letter-spacing:1.5px; text-transform:uppercase;">Tomorrow</strong><br><br><span style="color:#2C2C2C;">{parts[2]}</span></div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(str(e))

    st.markdown('<div class="section-title">Past Evening Check Ins</div>', unsafe_allow_html=True)
    evening_data = db_fetch("evening_logs", email)
    if evening_data:
        if st.button("Clear Evening Logs", use_container_width=True):
            db_delete_all("evening_logs", email)
            st.rerun()
        for row in evening_data:
            date = row["created_at"][:16].replace("T"," ")
            with st.expander(f"{date} — Day {row['day_rating']}/10"):
                st.markdown(f"<p style='color:#2C2C2C; margin:0.2rem 0;'><strong style='color:#02A87A;'>Water:</strong> {row['water_glasses']} glasses</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#2C2C2C; margin:0.2rem 0;'><strong style='color:#02A87A;'>Best part:</strong> {row['highlight']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#2C2C2C; margin:0.2rem 0;'><strong style='color:#02A87A;'>Challenge:</strong> {row['challenge']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#2C2C2C; margin:0.2rem 0;'><strong style='color:#02A87A;'>Grateful for:</strong> {row['grateful']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#2C2C2C; margin:0.2rem 0;'><strong style='color:#02A87A;'>Tomorrow goal:</strong> {row['goal']}</p>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">No check ins yet. Come back tonight.</p></div>', unsafe_allow_html=True)

# ══ PAGE 5 — MEDITATION ════════════════════════════════════════
if page == "🧘 Meditation":
    st.markdown('<div class="section-title">Meditation and Breathing</div>', unsafe_allow_html=True)
    ex_type = st.radio("", ["Breathing Exercise","Guided Meditation"], horizontal=True)
    if ex_type == "Breathing Exercise":
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            bp = st.empty()
        rounds = st.slider("Rounds", 1, 5, 3)
        if st.button("Begin", use_container_width=True):
            for i in range(rounds):
                st.markdown(f"<p style='color:#2C2C2C;'><strong>Round {i+1} of {rounds}</strong></p>", unsafe_allow_html=True)
                for label, grad, toast_msg, secs in [
                    ("Breathe In","#02A87A,#028C6A","Breathe IN...",4),
                    ("Hold","#7B6CB0,#028C6A","Hold...",4),
                    ("Breathe Out","#4A9EBF,#02A87A","Breathe OUT...",6),
                ]:
                    bp.markdown(f'<div style="width:180px;height:180px;border-radius:50%;background:linear-gradient(135deg,{grad});display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1rem;font-weight:600;letter-spacing:0.5px;box-shadow:0 8px 30px rgba(0,0,0,0.15);">{label}</div>', unsafe_allow_html=True)
                    st.toast(toast_msg)
                    time.sleep(secs)
            bp.markdown('<div style="width:180px;height:180px;border-radius:50%;background:linear-gradient(135deg,#02A87A,#02C39A);display:flex;align-items:center;justify-content:center;margin:auto;color:white;font-size:1rem;font-weight:600;box-shadow:0 8px 30px rgba(2,168,122,0.3);">Complete</div>', unsafe_allow_html=True)
            st.success(f"Well done, {name}.")
    else:
        med_type = st.selectbox("Select meditation", ["5 Minute Calm","Sleep Meditation","Anxiety Relief","Self Love","Focus"])
        MEDS = {
            "5 Minute Calm":[("Settle in","Sit comfortably. Close your eyes. Relax completely.",10),("Breathe","In for 4. Hold for 2. Out for 6.",15),("Body scan","Relax from toes to head.",20),("Peaceful place","Imagine somewhere beautiful and safe.",30),("Return","Wiggle fingers. Open eyes slowly.",10)],
            "Sleep Meditation":[("Lie down","Sink into your bed.",10),("Slow breath","In 4. Hold 7. Out 8.",20),("Release the day","Think of one good thing. Let the rest go.",20),("Body scan","Feel every part relax and get heavy.",30),("Drift off","You are safe. You are calm. Sleep now.",15)],
            "Anxiety Relief":[("Acknowledge","It is okay to feel anxious. You are safe.",10),("5-4-3-2-1","5 things you see. 4 touch. 3 hear. 2 smell. 1 taste.",30),("Box breathing","In 4. Hold 4. Out 4. Hold 4.",20),("Self talk","I am safe. This will pass. I am strong.",15),("Calm","The anxiety is passing. You are okay.",15)],
            "Self Love":[("Hand on heart","Breathe slowly. Feel your heartbeat.",10),("Acknowledge yourself","Think of one thing you did well.",15),("Golden light","Imagine warm light growing in your chest.",20),("Affirmation","I am enough. I am worthy. I deserve love.",20),("Gratitude","Thank yourself. Open eyes gently.",10)],
            "Focus":[("Prepare","Sit straight. Three deep breaths.",10),("Single focus","Pick one object. Stare gently. Return when mind wanders.",20),("Breath anchor","Use breath as anchor. Notice thoughts and return.",20),("Visualise","See yourself completing your task calmly.",15),("Begin","Open eyes. You are ready. Start now.",10)],
        }
        if st.button("Begin Meditation", use_container_width=True):
            for i,(title,instruction,secs) in enumerate(MEDS[med_type]):
                st.markdown(f'<div class="mcard"><strong style="color:#02A87A; font-size:0.68rem; letter-spacing:1.5px; text-transform:uppercase;">Step {i+1} — {title}</strong><br><br><span style="color:#7A7065; font-weight:300;">{instruction}</span></div>', unsafe_allow_html=True)
                time.sleep(secs)
            st.success(f"Meditation complete, {name}. Well done.")

# ══ PAGE 6 — AFFIRMATIONS ══════════════════════════════════════
if page == "🎯 Affirmations":
    st.markdown('<div class="section-title">Daily Affirmation</div>', unsafe_allow_html=True)
    if st.session_state.affirmation is None:
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
    st.markdown(f'<div class="affirmation-box">{st.session_state.affirmation}</div>', unsafe_allow_html=True)
    if st.button("Next Affirmation", use_container_width=True):
        st.session_state.affirmation = random.choice(AFFIRMATIONS)
        st.rerun()
    st.markdown('<div class="section-title">All Affirmations</div>', unsafe_allow_html=True)
    for a in AFFIRMATIONS:
        st.markdown(f'<div class="mcard" style="padding:0.75rem 1.2rem; margin:0.3rem 0;"><p style="margin:0; color:#2C2C2C; font-size:0.88rem; font-weight:300;">{a}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Quote for You</div>', unsafe_allow_html=True)
    feeling = st.text_input("How are you feeling right now?", placeholder="I feel...")
    if st.button("Generate Quote", use_container_width=True):
        if feeling.strip():
            with st.spinner(""):
                try:
                    q = groq_call([{"role":"user","content":f"I am {name} and I feel: {feeling}. Write one beautiful meaningful short quote for me. Then write the author below. If you made it up write MindEase as author. Maximum 2 sentences."}])
                    st.markdown(f'<div class="quote-box"><span style="color:#2C2C2C;">{q}</span></div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(str(e))
        else:
            st.warning("Please tell me how you are feeling.")
    st.markdown('<div class="section-title">Classic Quotes</div>', unsafe_allow_html=True)
    for q, a in QUOTES:
        with st.expander(f"{q[:50]}..."):
            st.markdown(f'<p style="font-style:italic; color:#2C2C2C; font-weight:300; margin:0 0 0.5rem;">"{q}"</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#02A87A; font-size:0.82rem; margin:0;">— {a}</p>', unsafe_allow_html=True)

# ══ PAGE 7 — ASSESSMENT ════════════════════════════════════════
if page == "🧠 Assessment":
    st.markdown('<div class="section-title">Mental Health Self Assessment</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#7A7065; font-size:0.85rem; margin:0 0 1rem;">Answer 8 questions honestly. This is not a medical diagnosis — it is a personal check in tool.</p>', unsafe_allow_html=True)
    qs = [
        ("How often do you feel sad or hopeless?",            ["Never","Sometimes","Often","Always"]),
        ("How often do you feel worried or anxious?",          ["Never","Sometimes","Often","Always"]),
        ("How well are you sleeping?",                         ["Very Well","Okay","Poorly","Very Poorly"]),
        ("How often do you feel lonely?",                      ["Never","Sometimes","Often","Always"]),
        ("How often do you lose interest in things you enjoy?",["Never","Sometimes","Often","Always"]),
        ("How often do you feel tired or low energy?",         ["Never","Sometimes","Often","Always"]),
        ("How often do you feel angry or irritated?",          ["Never","Sometimes","Often","Always"]),
        ("How often do you feel overwhelmed?",                 ["Never","Sometimes","Often","Always"]),
    ]
    score_map = {"Never":0,"Very Well":0,"Sometimes":1,"Okay":1,"Often":2,"Poorly":2,"Always":3,"Very Poorly":3}
    answers = [st.selectbox(f"{i+1}. {q}", opts) for i,(q,opts) in enumerate(qs)]
    if st.button("View Results", use_container_width=True):
        total = sum(score_map[a] for a in answers)
        if total <= 6:
            lv,col = "Low","#02A87A"
            reason = "You are generally feeling well with good emotional balance."
            tips = ["Keep doing what you are doing.","Maintain regular sleep.","Stay connected with friends.","Practice affirmations daily."]
            vids = HAPPY_VIDEOS[:2]
        elif total <= 14:
            lv,col = "Moderate","#E8A020"
            reason = "You are experiencing some stress. With self care you can feel much better."
            tips = ["Try the meditation section.","Journal every day.","Log your mood daily.","Get 7 to 8 hours of sleep.","Talk to someone you trust."]
            vids = HAPPY_VIDEOS[:3]
        else:
            lv,col = "High","#D46B6B"
            reason = "You may be going through a difficult time. You are not alone and help is available."
            tips = ["Talk to someone you trust.","Use the Chat section anytime.","Crisis helpline: iasp.info/resources/Crisis_Centres","Try breathing exercises.","Consider speaking to a professional."]
            vids = HAPPY_VIDEOS
        st.markdown(f'<div class="result-box" style="background:{col}10;border:1.5px solid {col}33;"><span style="color:#2C2C2C;">{name}, your wellness level is currently </span><strong style="color:{col};">{lv}</strong></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">{reason}</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)
        for t in tips:
            st.markdown(f'<div class="mcard" style="padding:0.6rem 1rem; margin:0.25rem 0;"><p style="margin:0; color:#2C2C2C; font-size:0.85rem;">{t}</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Watch</div>', unsafe_allow_html=True)
        for title, url in vids:
            st.markdown(f'<p style="color:#7A7065; font-size:0.82rem; margin:0.5rem 0 0.2rem;">{title}</p>', unsafe_allow_html=True)
            st.markdown(f'<iframe width="100%" height="180" src="{url}" frameborder="0" allowfullscreen style="border-radius:14px; box-shadow:0 4px 15px rgba(0,0,0,0.08);"></iframe>', unsafe_allow_html=True)
        st.markdown('<p style="color:#7A7065; font-size:0.75rem; margin-top:1rem;">Not a medical diagnosis. Please see a professional if you are struggling.</p>', unsafe_allow_html=True)

# ══ PAGE 8 — ACHIEVEMENTS ══════════════════════════════════════
if page == "🏆 Achievements":
    st.markdown('<div class="section-title">Your Progress</div>', unsafe_allow_html=True)
    mood_count    = len(db_fetch("mood_logs", email))
    sleep_count   = len(db_fetch("sleep_logs", email))
    journal_count = len(db_fetch("journal_logs", email))
    streak        = get_streak(email)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="score-box"><div style="font-size:0.62rem; letter-spacing:1.8px; text-transform:uppercase; color:#7A7065; margin-bottom:0.5rem;">STREAK</div><div style="font-size:2.2rem; font-weight:700; color:#02A87A;">{streak}</div><div style="font-size:0.75rem; color:#7A7065;">days</div></div>', unsafe_allow_html=True)
    with c2:
        sc = 0
        mood_data = db_fetch("mood_logs", email)
        if mood_data:
            happy = sum(1 for r in mood_data if r["mood"]=="Happy")
            sc += min(int(happy/len(mood_data)*30),30)
        sleep_data = db_fetch("sleep_logs", email)
        if sleep_data:
            avg = sum(r["hours"] for r in sleep_data)/len(sleep_data)
            sc += 25 if avg>=8 else 15 if avg>=6 else 5
        sc += min(journal_count*5,25)
        sc += min(streak*2,20)
        sc_col = "#02A87A" if sc>=80 else "#E8A020" if sc>=60 else "#4A9EBF" if sc>=40 else "#D46B6B"
        st.markdown(f'<div class="score-box" style="border-color:{sc_col}33;"><div style="font-size:0.62rem; letter-spacing:1.8px; text-transform:uppercase; color:#7A7065; margin-bottom:0.5rem;">WELLNESS</div><div style="font-size:2.2rem; font-weight:700; color:{sc_col};">{sc}</div><div style="font-size:0.75rem; color:#7A7065;">out of 100</div></div>', unsafe_allow_html=True)
    with c3:
        earned_count = sum(1 for b in BADGES if b["fn"](mood_count,sleep_count,journal_count,streak))
        st.markdown(f'<div class="score-box"><div style="font-size:0.62rem; letter-spacing:1.8px; text-transform:uppercase; color:#7A7065; margin-bottom:0.5rem;">BADGES</div><div style="font-size:2.2rem; font-weight:700; color:#02A87A;">{earned_count}</div><div style="font-size:0.75rem; color:#7A7065;">of {len(BADGES)}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Badges</div>', unsafe_allow_html=True)
    earned   = [b for b in BADGES if b["fn"](mood_count,sleep_count,journal_count,streak)]
    unearned = [b for b in BADGES if not b["fn"](mood_count,sleep_count,journal_count,streak)]
    if earned:
        st.markdown('<p style="color:#02A87A; font-size:0.68rem; letter-spacing:1.5px; text-transform:uppercase; margin:0 0 0.5rem;">EARNED</p>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, b in enumerate(earned):
            with cols[i%3]:
                st.markdown(f'<div class="badge-earned"><div style="font-size:1.4rem; color:#02A87A;">{b["icon"]}</div><div style="color:#2C2C2C; font-weight:600; font-size:0.82rem; margin:0.3rem 0 0.1rem;">{b["name"]}</div><div style="color:#7A7065; font-size:0.72rem;">{b["desc"]}</div></div>', unsafe_allow_html=True)
    if unearned:
        st.markdown('<p style="color:#7A7065; font-size:0.68rem; letter-spacing:1.5px; text-transform:uppercase; margin:0.8rem 0 0.5rem;">LOCKED</p>', unsafe_allow_html=True)
        for b in unearned:
            st.markdown(f'<div class="badge-locked"><span style="color:#7A7065; font-size:0.82rem;">{b["name"]}</span> <span style="color:#7A7065; font-size:0.75rem; opacity:0.7;">— {b["desc"]}</span></div>', unsafe_allow_html=True)

# ══ PAGE 9 — PROGRESS ══════════════════════════════════════════
if page == "📈 Progress":
    st.markdown('<div class="section-title">Progress Report</div>', unsafe_allow_html=True)
    period = st.radio("Period", ["Last 7 Days","Last 30 Days"], horizontal=True)
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
            with c1: st.metric("Total", len(df))
            with c2: st.metric("Happy", len(df[df["mood"]=="Happy"]))
            with c3: st.metric("Sad",   len(df[df["mood"]=="Sad"]))
            with c4: st.metric("Stressed", len(df[df["mood"]=="Stressed"]))
        else: st.markdown(f'<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">No mood logs in the last {days} days.</p></div>', unsafe_allow_html=True)
    except: st.markdown('<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">No mood data yet.</p></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-title">Sleep — {period}</div>', unsafe_allow_html=True)
    try:
        sleep_res = supabase.table("sleep_logs").select("*").eq("user_email",email).gte("created_at",cutoff).execute()
        if sleep_res.data:
            df_s = pd.DataFrame(sleep_res.data)
            avg = df_s["hours"].mean()
            st.metric("Average Sleep", f"{avg:.1f} hrs")
            st.line_chart(df_s.set_index("created_at")["hours"])
            if avg>=8: st.success("Great sleep average.")
            elif avg>=6: st.info("Decent. Aim for 8 hours.")
            else: st.warning("Not enough sleep. Rest more.")
        else: st.markdown(f'<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">No sleep logs in the last {days} days.</p></div>', unsafe_allow_html=True)
    except: st.markdown('<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">No sleep data yet.</p></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-title">Journal — {period}</div>', unsafe_allow_html=True)
    try:
        journal_res = supabase.table("journal_logs").select("*").eq("user_email",email).gte("created_at",cutoff).execute()
        count = len(journal_res.data) if journal_res.data else 0
        st.metric("Entries Written", count)
        if count>=5: st.success("Excellent journaling habit.")
        elif count>=1: st.info("Good start. Try writing daily.")
        else: st.warning("No entries this period.")
    except: st.markdown('<div class="mcard"><p style="color:#7A7065; font-size:0.88rem; margin:0;">No journal data yet.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">AI Summary</div>', unsafe_allow_html=True)
    if st.button("Generate My Summary", use_container_width=True):
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
        with st.spinner(""):
            try:
                summary = groq_call([{"role":"user","content":f"User: {name}. Mood data: {mm}. Sleep: {sl}. Journal: {jj}. Write 3-4 warm sentences using their name. Highlight what they do well and gently suggest one improvement."}])
                st.markdown(f'<div class="mcard-accent"><p style="color:#2C2C2C; margin:0;">{summary}</p></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))
