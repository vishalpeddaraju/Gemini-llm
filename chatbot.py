
from dotenv import load_dotenv
import streamlit as st
import os
from pathlib import Path
from google import genai

# --------------------------------------------------
# 1. Streamlit Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Gemini LLM Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------------------------
# 2. Load Environment Variables
# --------------------------------------------------

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

# --------------------------------------------------
# 3. Initialize Gemini Client
# --------------------------------------------------

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"

# --------------------------------------------------
# 4. Initialize Session State
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# 5. Gemini Response Function
# --------------------------------------------------

def get_gemini_response(question, response_length):

    word_limits = {
        "Short": 150,
        "Medium": 300,
        "Detailed": 600
    }

    word_limit = word_limits[response_length]

    # Include previous conversation for context
    conversation = []

    for role, message in st.session_state.chat_history:
        conversation.append({
            "role": "user" if role == "You" else "model",
            "parts": [{"text": message}]
        })

    # Add current question with response instructions
    prompt = f"""
    Answer the following question clearly and accurately.

    Response Length: {response_length}
    Approximate Word Limit: {word_limit} words.

    Instructions:
    1. Keep the response within approximately {word_limit} words.
    2. Use clear headings and bullet points where appropriate.
    3. Include practical examples wherever useful.
    4. For programming questions, provide readable code examples.
    5. Avoid unnecessary explanations and repetition.

    Question: {question}
    """

    conversation.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=conversation
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text


# --------------------------------------------------
# 6. Streamlit Application
# --------------------------------------------------

st.title("🤖 Gemini LLM Chatbot")

st.caption("Powered by Google Gemini API")

st.write(
    "Ask technical questions and interact with "
    "Google Gemini using natural language."
)

# --------------------------------------------------
# 7. User Input
# --------------------------------------------------

question = st.text_input(
    "Enter your question:",
    placeholder="Example: Explain Python decorators with examples..."
)

# Response length selection
response_length = st.selectbox(
    "Choose Response Length:",
    ["Short", "Medium", "Detailed"],
    index=1
)

col1, col2 = st.columns(2)

with col1:
    submit = st.button(
        "Ask Gemini",
        use_container_width=True
    )

with col2:
    clear = st.button(
        "Clear Chat",
        use_container_width=True
    )

# --------------------------------------------------
# 8. Clear Conversation
# --------------------------------------------------

if clear:
    st.session_state.chat_history = []
    st.rerun()

# --------------------------------------------------
# 9. Generate Gemini Response
# --------------------------------------------------

if submit:

    if question.strip():

        try:
            with st.spinner("Gemini is generating your response..."):

                answer = get_gemini_response(
                    question,
                    response_length
                )

            # Store conversation
            st.session_state.chat_history.append(
                ("You", question)
            )

            st.session_state.chat_history.append(
                ("Gemini", answer)
            )

        except Exception as e:

            st.error("Unable to generate a response from Gemini.")
            st.exception(e)

    else:
        st.warning("Please enter a question.")

# --------------------------------------------------
# 10. Display Conversation History
# --------------------------------------------------

st.divider()

st.subheader("Conversation History")

if st.session_state.chat_history:

    for role, message in st.session_state.chat_history:

        if role == "You":

            with st.chat_message("user"):
                st.markdown(message)

        else:

            with st.chat_message("assistant"):
                st.markdown(message)

else:

    st.info("Your conversation will appear here.")
