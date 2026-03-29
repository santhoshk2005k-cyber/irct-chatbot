import streamlit as st
import google.generativeai as genai

# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY   = "AIzaSyCgNhKifs1VhC4XHB542Yp4J4nWTpLcpl8"          # ← paste your key here
KB_PATH   = "train_schedule_20.txt"      # ← path to your knowledge-base file
MODEL     = "gemini-2.5-flash"
# ────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def load_chat():
    """Load KB, configure Gemini, and return a chat session (cached)."""
    with open(KB_PATH, encoding="utf-8") as f:
        kb = f.read()

    system_prompt = f"""
You are an IRCTC customer care executive. Your job is to answer questions
asked by customers. Be polite and helpful. If a question is outside the
knowledge base, say you don't have that information. Only refer to the
knowledge base provided below.

{kb}
"""
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL, system_instruction=system_prompt)
    return model.start_chat()


# ── PAGE SETUP ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="IRCTC Support", page_icon="🚆")
st.title("🚆 IRCTC Customer Support")
st.caption("Ask me anything about train schedules, tickets, and more.")

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []   # list of {"role": ..., "content": ...}

# ── RENDER HISTORY ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── CHAT INPUT ────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Type your question here..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat = load_chat()
            response = chat.send_message(user_input)
            reply = response.text
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})