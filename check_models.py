
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from pathlib import Path
import os

# --------------------------------------------------
# 1. Load Environment Variables
# --------------------------------------------------

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found!")
    print("Please check your .env file.")
    raise SystemExit(1)

print("API key loaded successfully!")


# --------------------------------------------------
# 2. Initialize Gemini Client
# --------------------------------------------------

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# 3. Retrieve Available Models
# --------------------------------------------------

print("\nAvailable Gemini Models")
print("=" * 60)

text_models = []
vision_models = []

try:

    for model in client.models.list():

        actions = model.supported_actions or []

        if "generateContent" not in actions:
            continue

        model_name = model.name

        print(f"\nModel: {model_name}")

        print(f"Display Name: {model.display_name}")

        print(f"Supported Actions: {actions}")

        # Check advertised input modalities
        modalities = getattr(
            model,
            "supported_input_modalities",
            None
        )

        if modalities:
            print(f"Input Modalities: {modalities}")

            modality_names = [
                str(m).upper() for m in modalities
            ]

            if any("IMAGE" in m for m in modality_names):
                vision_models.append(model_name)

        text_models.append(model_name)

        print("-" * 60)


    # --------------------------------------------------
    # 4. Summary
    # --------------------------------------------------

    print("\nMODEL SUMMARY")
    print("=" * 60)

    print(
        f"\nTotal GenerateContent Models: "
        f"{len(text_models)}"
    )

    print("\nModels supporting GenerateContent:")

    for name in text_models:
        print(f" - {name}")

    print("\nModels advertising IMAGE input:")

    if vision_models:

        for name in vision_models:
            print(f" - {name}")

    else:
        print(
            "No image-input information was confirmed "
            "from model metadata."
        )
        print(
            "Some multimodal models may still support images. "
            "Check the model documentation or test with an image."
        )


except errors.APIError as e:

    print("\nGemini API Error!")
    print(f"Status Code: {e.code}")
    print(f"Details: {e}")

except Exception as e:

    print("\nUnexpected Error:")
    print(str(e))

finally:
    client.close()
