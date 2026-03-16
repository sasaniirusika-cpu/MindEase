import streamlit as st
from groq import Groq

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
st.divider()

with st.sidebar:
    st.markdown("### Settings")
    api_key = st.text_input("Enter your Groq API Key", type="password", placeholder="gsk_...")
    st.caption("Get your free API key at console.groq.com")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

SYSTEM_PROMPT = "You are MindEase, a warm and caring AI mental health companion. Listen with kindness. Validate feelings. Ask gentle follow-up questions. Suggest breathing exercises or journaling when helpful. Use simple language. If user mentions self-harm share this: https://www.iasp.info/resources/Crisis_Centres/ Never diagnose or replace therapy."

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
