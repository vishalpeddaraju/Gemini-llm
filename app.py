from dotenv import load_dotenv
import streamlit as st
import os
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


# Function to get Gemini response
def get_gemini_response(question):

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=question
    )

    return response.text


# Streamlit application
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini Application")

input_text = st.text_input(
    "Input:",
    key="input"
)

submit = st.button("Ask the question")


# When button is clicked
if submit:

    if input_text:

        response = get_gemini_response(input_text)

        st.subheader("The Response is")

        st.write(response)

    else:

        st.warning("Please enter a question.")