
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Explain Python decorators with a practical example."
    )

    print("Gemini API working!")
    print(response.text)

except Exception as e:
    print("Gemini API Error:")
    print(e)
