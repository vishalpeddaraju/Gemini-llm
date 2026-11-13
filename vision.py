
from dotenv import load_dotenv
import streamlit as st
import os
import time
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import errors


# --------------------------------------------------
# 1. Streamlit Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Gemini Image Application",
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
# 4. Gemini Image Response Function
# --------------------------------------------------

def get_gemini_response(prompt, image):

    if not prompt.strip():
        prompt = (
            "Analyze this image and provide a clear description "
            "of its contents, important details, and observations."
        )

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt, image]
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            return response.text

        except errors.APIError as e:

            # Retry temporary server errors
            if e.code == 503 and attempt < 2:

                wait_time = 2 ** (attempt + 1)

                st.warning(
                    f"Gemini server is busy. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise

    raise Exception(
        "Gemini is currently unavailable. Please try again later."
    )


# --------------------------------------------------
# 5. Streamlit Application Interface
# --------------------------------------------------

st.title("🖼️ Gemini Image Application")

st.caption("Powered by Google Gemini API")

st.write(
    "Upload an image and ask Gemini to analyze, "
    "describe, or explain its contents."
)


# --------------------------------------------------
# 6. User Input
# --------------------------------------------------

prompt = st.text_input(
    "Enter your prompt:",
    placeholder="Example: Explain the architecture shown in this image..."
)

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)


# --------------------------------------------------
# 7. Display Uploaded Image
# --------------------------------------------------

image = None

if uploaded_file is not None:

    try:

        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded Image",
            width="stretch"
        )

    except Exception:
        st.error("Unable to read this image. Please upload another image.")
        image = None


# --------------------------------------------------
# 8. Analyze Image
# --------------------------------------------------

if st.button("Analyze Image", use_container_width=True):

    if image is None:

        st.warning("Please upload an image first.")

    else:

        try:

            with st.spinner("Gemini is analyzing your image..."):

                response = get_gemini_response(
                    prompt,
                    image
                )

            st.success("Image analysis completed!")

            st.subheader("Gemini Response")

            st.markdown(response)

        except errors.APIError as e:

            if e.code == 503:

                st.error(
                    "Gemini server is experiencing high demand. "
                    "Please try again after some time."
                )

            elif e.code == 429:

                st.error(
                    "API rate limit reached. Please try again later."
                )

            else:

                st.error(f"Gemini API Error: {e}")

        except Exception as e:

            st.error("Unable to analyze the image.")

            with st.expander("View error details"):
                st.code(str(e))


# --------------------------------------------------
# 9. Footer
# --------------------------------------------------

st.divider()

st.caption("Developed using Python, Streamlit and Google Gemini API")
