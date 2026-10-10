
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load the API key from .env
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(api_key=api_key)


def generate_answer(question, retrieved_results):
    if not retrieved_results:
        return {
            "answer": (
                "I couldn't find verified information "
                "in the available college records."
            ),
            "source": None
        }

    context = "\n\n".join(
        result["text"] for result in retrieved_results
    )

    sources = list(dict.fromkeys(
        result["source"] for result in retrieved_results
    ))

    prompt = f"""
You are a college administration chatbot.

Answer using ONLY the college information below.
Do not invent college rules, dates, fees, or contacts.
If the information is insufficient, say so clearly.
Be polite and concise.

College information:
{context}

Student question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    answer = (response.text or "").strip()

    if not answer:
        answer = (
            "I couldn't generate an answer. "
            "Please try again later."
        )

    return {
        "answer": answer,
        "source": ", ".join(sources)
    }


if __name__ == "__main__":
    print("Gemini answer generator is configured.")
    print("Ready to connect to document retrieval.")
