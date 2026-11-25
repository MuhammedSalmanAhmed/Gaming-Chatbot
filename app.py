
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="GameMate AI",
    page_icon="🎮",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #10131a;
}

h1 {
    color: #00ff99;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #aaaaaa;
    margin-bottom: 25px;
}

.stChatMessage {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# System prompt
SYSTEM_PROMPT = """
You are GameMate AI, a friendly and knowledgeable gaming expert chatbot.

You specialize in:
1. Game recommendations.
2. Gaming tips and strategies.
3. Gaming hardware and peripherals.
4. Gaming troubleshooting.
5. Game information and mechanics.
6. FPS improvement and performance optimization.

Provide clear, accurate, and helpful answers.
Use simple language and a friendly, professional tone.

Only answer questions related to video games and gaming technology.
Politely decline unrelated questions and redirect users toward gaming topics.

Do not invent facts or present outdated information as current.
If you are unsure about something, clearly mention it.
"""

# Model configuration
MODEL_NAME = "openai/gpt-oss-120b"
TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 1024

# API key
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# Initialize client
if not GROQ_API_KEY:
    st.error("Groq API key is missing. Please configure it in Streamlit secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Application heading
st.title("🎮 GameMate AI")
st.markdown(
    '<p class="subtitle">Your Personal Gaming Assistant</p>',
    unsafe_allow_html=True
)

st.write(
    "Ask me anything about video games, gaming strategies, "
    "hardware, troubleshooting, and performance optimization!"
)

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask GameMate AI something...")

if user_input:

    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Prepare conversation
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + st.session_state.messages

        with st.chat_message("assistant"):
            with st.spinner("GameMate AI is thinking..."):

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=TEMPERATURE,
                    max_completion_tokens=MAX_OUTPUT_TOKENS
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

        # Save assistant response
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        st.error(f"Unable to generate a response: {str(e)}")
