from dotenv import load_dotenv
import streamlit as st
import os
from pathlib import Path
from PIL import Image
from google import genai

# Load .env from the same folder as this Python file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY is not found in your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


def get_gemini_response(prompt, image):

    if prompt:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[prompt, image]
        )
    else:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=image
        )

    return response.text


# Streamlit app
st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Image Application")

prompt = st.text_input(
    "Input Prompt:",
    placeholder="Describe this image..."
)

uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png"]
)

image = None

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        width="stretch"
    )


if st.button("Tell me about the image"):

    if image is None:

        st.warning("Please upload an image first.")

    else:

        with st.spinner("Gemini is analyzing the image..."):

            try:

                response = get_gemini_response(
                    prompt,
                    image
                )

                st.subheader("Response")

                st.write(response)

            except Exception as e:

                st.error("Error while communicating with Gemini:")
                st.exception(e)