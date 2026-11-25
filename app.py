
import streamlit as st
from groq import Groq
import re
from guardrails import (
    validate_input,
    check_injection,
    check_domain
)

def clean_response(text):
    # Replace HTML line breaks, including escaped versions
    text = re.sub(r"\\?\s*<br\s*/?>", " • ", text, flags=re.IGNORECASE)
    return text

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="GameMate AI | Gaming Assistant",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f5f7fb;
    color: #1e293b;
}

/* Main content width */
.block-container {
    max-width: 950px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main heading */
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 0;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
    margin-top: 5px;
    margin-bottom: 25px;
}

/* Hero section */
.hero {
    background: linear-gradient(120deg, #e0e7ff, #eef2ff);
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 25px;
    border: 1px solid #dbe4ff;
}

.hero h2 {
    color: #172554;
    font-size: 27px;
    margin-bottom: 8px;
}

.hero p {
    color: #475569;
    font-size: 15px;
}

/* Feature cards */
.feature-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    min-height: 115px;
    margin-bottom: 12px;
}

.feature-card h4 {
    color: #1e293b;
    margin-bottom: 5px;
}

.feature-card p {
    color: #64748b;
    font-size: 13px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 12px;
    color: #1e293b;
}

/* Chat input */
[data-testid="stChatInput"] {
    background-color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: 1px solid #dbe4ff;
    background-color: #eef2ff;
    color: #3730a3;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #e0e7ff;
    border-color: #818cf8;
    color: #312e81;
}

/* Divider */
hr {
    border-color: #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """
You are GameMate AI, a friendly and knowledgeable gaming expert chatbot.

ROLE:
You are an expert assistant specializing in video games and gaming technology.
Your goal is to provide useful, accurate, and engaging gaming-related information.

AUDIENCE:
Your audience includes beginner, intermediate, and experienced gamers.

AREAS OF EXPERTISE:
1. Game recommendations based on user preferences.
2. Gaming tips, tricks, guides, and strategies.
3. Gaming hardware, including CPUs, GPUs, PCs, and peripherals.
4. Troubleshooting gaming errors and technical issues.
5. Game information, features, mechanics, and updates.
6. FPS improvement and gaming performance optimization.

BEHAVIOR:
- Don't provide very lengthy answers.
- Provide clear, helpful, and accurate answers.
- Use simple language that gamers can easily understand.
- Give step-by-step instructions when needed.
- Ask follow-up questions when more information is required.
- Avoid making up information when uncertain.
- Keep responses relevant to the user's question.
- Use standard Markdown for formatting. Never generate HTML tags such as <br>, <div>, or <p>.
- Do not use HTML line breaks inside tables.
- Prefer headings and bullet points instead of large tables.
- Keep answers well-structured, readable, and concise.

DOMAIN RESTRICTION:
You must only assist with video games and gaming technology.
If a user asks about unrelated topics, politely explain that you
specialize in gaming and encourage them to ask a gaming-related question.
Do not answer unrelated questions even if the user insists.

TONE:
Be friendly, professional, engaging, and supportive.
Respond like an experienced gaming assistant.
"""

# ---------------- MODEL CONFIGURATION ----------------

MODEL_NAME = "openai/gpt-oss-120b"
TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 1024


# ---------------- API CONFIGURATION ----------------

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error("Groq API key is missing. Please configure Streamlit secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🎮 GameMate AI")

    st.caption("Your personal gaming assistant")

    st.divider()

    st.markdown("### About")

    st.write(
        "GameMate AI helps gamers discover games, "
        "improve gameplay, solve technical problems, "
        "and choose gaming hardware."
    )

    st.divider()

    st.markdown("### What I can help with")

    st.markdown("""
    - 🎯 Gaming strategies
    - 🕹️ Game recommendations
    - 🖥️ PC hardware advice
    - 🚀 FPS optimization
    - 🔧 Gaming troubleshooting
    """)

    st.divider()

    st.markdown("### Conversation")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Groq API")


# ---------------- MAIN HEADER ----------------

st.markdown(
    '<div class="main-title">🎮 GameMate AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">YOUR PERSONAL GAMING ASSISTANT</div>',
    unsafe_allow_html=True
)


# ---------------- HERO SECTION ----------------

st.markdown("""
<div class="hero">
    <h2>Level up your gaming experience.</h2>
    <p>
        Get expert gaming advice, discover new games,
        optimize your PC and improve your gameplay.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- WELCOME MESSAGE ----------------

if not st.session_state.messages:

    with st.chat_message("assistant", avatar="🎮"):
        st.markdown(
            "Hey! Welcome to GameMate AI. 👋\n\n"
            "I'm here to help with games, strategies, "
            "gaming hardware and performance optimization.\n\n"
            "**What would you like to explore today?**"
        )


# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:

    avatar = "🎮" if message["role"] == "assistant" else "👤"

    with st.chat_message(message["role"]):
      if message["role"] == "assistant":
          st.markdown(clean_response(message["content"]))
      else:
          st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------

user_input = st.chat_input("Ask GameMate anything about gaming...")

if user_input:

    # 1. Input validation
    is_valid, error_message = validate_input(user_input)

    if not is_valid:
        st.warning(error_message)
        st.stop()

    # 2. Prompt injection detection
    if check_injection(user_input):
        st.warning(
            "Your request contains an instruction that I cannot follow. "
            "Let's keep our conversation gaming-related!"
        )
        st.stop()

    # 3. Gaming domain detection
    if not check_domain(user_input, st.session_state.messages):
        st.info(
            "I'm GameMate AI, and I specialize in gaming "
            "and gaming technology. Please ask a gaming-related question!"
        )
        st.stop()

    # Save only validated messages
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    try:

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + st.session_state.messages

        with st.chat_message("assistant", avatar="🎮"):

            with st.spinner("GameMate is thinking..."):

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=TEMPERATURE,
                    max_completion_tokens=MAX_OUTPUT_TOKENS
                )

                answer = response.choices[0].message.content

                if not answer:
                    raise ValueError("The API returned an empty response.")

                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:

        st.error(
            "Sorry! I couldn't generate a response. "
            "Please try again in a moment."
        )

        st.caption(f"Technical details: {str(e)}")

        # Remove failed user request from history
        st.session_state.messages.pop()

# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    "<center style='color:#94a3b8;font-size:13px;'>"
    "🎮 GameMate AI | Powered by Groq"
    "</center>",
    unsafe_allow_html=True
)
