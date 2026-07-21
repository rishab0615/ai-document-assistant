import time

from google import genai
from google.genai.errors import ServerError

from app.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite"
]


def ask_gemini(
    document_text: str,
    question: str
):
    prompt = f"""
    You are an expert document assistant.

Document:
{document_text}

Question:
{question}

Rules:

1. Use the document as your primary source.

2. If the question asks for information contained in the document,
answer only from the document.

3. If the question asks for analysis, suggestions,
critique or improvements,
use your professional knowledge while referring
to the document.

4. Never invent facts that are not present.

5. Clearly distinguish between
facts from the document
and your recommendations.
"""

    last_error = None

    for model in MODELS:
        try:
            print(f"Trying model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

        except ServerError as e:
            print(f"{model} unavailable. Trying next model...")
            last_error = e
            time.sleep(2)

    raise Exception(
        "All Gemini models are temporarily unavailable. Please try again later."
    ) from last_error