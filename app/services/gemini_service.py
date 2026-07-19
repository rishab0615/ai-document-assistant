from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(
    api_key = GEMINI_API_KEY
)


def ask_gemini(
    document_text:str,
    question:str
):
    prompt = f"""
You are an AI document assistant.

Document:
{document_text}

Question:
{question}

Answer the question using ONLY the information in the document.
If the answer isn't in the document, say you couldn't find it.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text