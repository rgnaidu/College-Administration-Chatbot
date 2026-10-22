
import re
import sys
from pathlib import Path

# Find the project folders
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAG_FOLDER = Path(__file__).resolve().parent

# Make the other RAG files importable
if str(RAG_FOLDER) not in sys.path:
    sys.path.insert(0, str(RAG_FOLDER))

from document_loader import load_text_files
from embeddings import create_embeddings, search_documents
from answer_generator import generate_answer


# Load college documents and create embeddings once
KNOWLEDGE_FOLDER = PROJECT_ROOT / "knowledge_base"

documents = load_text_files(str(KNOWLEDGE_FOLDER))
chunks, sources, embeddings = create_embeddings(documents)


def ask_college_question(question):
    """Find relevant college information and generate an answer."""

    if not question or not question.strip():
        return {
            "status": "invalid_request",
            "answer": "Please enter a question.",
            "source": None,
            "source_url": None
        }

    # Search the knowledge base
    results = search_documents(
        question.strip(),
        chunks,
        sources,
        embeddings,
        top_k=1
    )

    # No useful matching document found
    if not results or results[0].get("score", 0) < 0.45:
        return {
            "status": "not_found",
            "answer": (
                "Sorry, I couldn't find a reliable answer in the available "
                "college records. Please check the official college website "
                "or contact the college administration."
            ),
            "source": None,
            "source_url": "https://www.gvpcew.ac.in/"
        }

    best_result = results[0]
    source_text = best_result.get("text", "")
    source_url_match = re.search(r"https?://[^\s<>\"']+", source_text)
    source_url = source_url_match.group(0).rstrip(".,;)") if source_url_match else None

    # Reliability safeguard for exact B.Tech fee questions for 2026-27
    question_lower = question.lower()
    retrieved_text = source_text.lower()

    asks_exact_fee = (
        any(word in question_lower for word in ["fee", "fees", "tuition"])
        and any(word in question_lower for word in ["exact", "amount", "how much"])
        and any(year in question_lower for year in [
            "2026-27", "2026–27", "2026/27"
        ])
    )

    fee_data_is_outdated = (
        any(year in retrieved_text for year in ["2024-25", "2024–25"])
        and any(word in retrieved_text for word in ["fee", "fees", "amount"])
    )

    if asks_exact_fee and fee_data_is_outdated:
        return {
            "status": "not_verified",
            "answer": (
                "I cannot verify the exact B.Tech fee for 2026–27 from the "
                "available college records. The retrieved fee information "
                "refers to 2024–25. Please check the latest official "
                "admissions notice."
            ),
            "source": best_result.get("source"),
            "source_url": source_url or "https://www.gvpcew.ac.in/"
        }

    # Generate an answer using the AI model
    try:
        generated = generate_answer(question, results)

        if isinstance(generated, dict):
            answer = generated.get("answer", "")
            answer_source = generated.get("source")
        else:
            answer = str(generated)
            answer_source = None

        if not answer:
            raise ValueError("The answer generator returned an empty answer.")

        return {
            "status": "success",
            "answer": answer,
            "source": best_result.get("source") or answer_source,
            "source_url": source_url,
            "score": best_result.get("score")
        }

    except Exception as error:
        error_message = str(error).lower()

        # If the AI service is unavailable or its quota is exhausted,
        # use a directly stored FAQ answer when possible.
        if any(term in error_message for term in [
            "429",
            "quota",
            "resource_exhausted",
            "rate limit",
            "503",
            "unavailable"
        ]):
            answer_match = re.search(
                r"Answer:\s*(.*?)(?=\n\s*(?:Category|Source|URL|Question|FAQ ID)\s*:|\Z)",
                source_text,
                re.IGNORECASE | re.DOTALL
            )

            if answer_match:
                fallback_answer = answer_match.group(1).strip()

                if fallback_answer:
                    return {
                        "status": "success_fallback",
                        "answer": fallback_answer,
                        "source": best_result.get("source"),
                        "source_url": source_url,
                        "score": best_result.get("score")
                    }

            return {
                "status": "temporarily_unavailable",
                "answer": (
                    "The AI answering service is temporarily unavailable, "
                    "and I couldn't extract a direct answer from the "
                    "matching college record. Please try again later or "
                    "check the official college website."
                ),
                "source": best_result.get("source"),
                "source_url": source_url or "https://www.gvpcew.ac.in/"
            }

        # Keep unexpected technical details out of the user-facing answer.
        print("Chatbot error:", repr(error))

        return {
            "status": "error",
            "answer": (
                "Sorry, something went wrong while preparing the answer. "
                "Please try again later."
            ),
            "source": best_result.get("source"),
            "source_url": source_url
        }


if __name__ == "__main__":
    print("GVPCEW College Administration Chatbot")
    print("Type 'exit' to stop.")

    while True:
        user_question = input("\nYou: ").strip()

        if user_question.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        response = ask_college_question(user_question)
        print("Chatbot:", response["answer"])
        print("Status:", response["status"])
