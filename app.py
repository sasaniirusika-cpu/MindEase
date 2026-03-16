import streamlit as st
import google.generativeai as genai

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
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input("Enter your Gemini API Key", type="password", placeholder="AIza...")
    st.caption("Get your free API key at aistudio.google.com")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

SYSTEM_PROMPT = """You are MindEase, a warm, empathetic, and caring AI mental health companion.
- Listen carefully and respond with kindness and understanding
- Validate the user feelings without judgment
- Ask gentle follow-up questions to help them feel heard
- Suggest simple coping activities like breathing exercises, journaling, or mindfulness when helpful
- Always respond in simple, easy-to-understand language
- If the user mentions self-harm or crisis, share this helpline: https://www.iasp.info/resources/Crisis_Centres/
- Never diagnose or replace professional therapy"""

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🌿"):
        st.markdown("Hi there! I am MindEase, your personal wellness companion. 😊 How are you feeling today?")

for message in st.session_state.messages:
    avatar = "🌿" if message["role"] == "assistant" else "🧑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

user_input = st.chat_input("Share how you are feeling...")

if user_input:
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar to start chatting.")
    else:
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("assistant", avatar="🌿"):
            with st.spinner("MindEase is listening..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name="gemini-2.0-flash", system_instruction=SYSTEM_PROMPT)
                    history = []
                    for m in st.session_state.messages[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        history.append({"role": role, "parts": [m["content"]]})
                    chat = model.start_chat(history=history)
                    response = chat.send_message(user_input)
                    reply = response.text
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
