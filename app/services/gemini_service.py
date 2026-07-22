import time

from google import genai
from google.genai.errors import ClientError, ServerError

from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
]


def build_chat_history(messages):
    if not messages:
        return "No previous conversation."

    history = []

    for message in messages:
        if message.role == "user":
            history.append(f"User: {message.message}")
        else:
            history.append(f"Assistant: {message.message}")

    return "\n\n".join(history)


def ask_gemini(
    document_text: str,
    chat_history: str,
    question: str,
):
    prompt = f"""
You are an expert document assistant.

Previous Conversation:
{chat_history}

--------------------------------------------------------

Document:
{document_text}

--------------------------------------------------------

Current Question:
{question}

Rules:

1. Use the document as your primary source.

2. Use the previous conversation only to understand context.

3. Never contradict the document.

4. If the answer exists in the document,
answer from the document.

5. If the user asks for analysis,
you may provide professional recommendations,
but clearly distinguish them from document facts.

6. Never invent information not supported
by the document.
"""

    last_error = None

    for model in MODELS:
        try:
            print(f"Trying model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            print(f"Success using {model}")
            return response.text

        except ClientError as e:
            last_error = e

            if "RESOURCE_EXHAUSTED" in str(e):
                print(f"{model} quota exhausted. Trying next model...")
                continue

            print(f"{model} client error: {e}")
            raise

        except ServerError as e:
            last_error = e

            print(f"{model} server unavailable. Trying next model...")
            time.sleep(2)
            continue

    raise Exception(
        "The AI service is temporarily unavailable. Please try again later."
    ) from last_error