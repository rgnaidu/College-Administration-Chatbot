
from document_loader import load_text_files
from embeddings import create_embeddings, search_documents
from answer_generator import generate_answer

tests = [
    {
        "question": "Where is GVPCEW located?",
        "expected": ["kommadi", "madhurawada"]
    },
    {
        "question": "How are Category-A seats filled?",
        "expected": ["APSCHE", "APEAPCET", "counselling"]
    },
    {
        "question": "Where can I find examination notifications?",
        "expected": ["examination", "notification"]
    },
    {
        "question": "Where can I find admission information?",
        "expected": ["admission"]
    },
    {
        "question": "What is the exact B.Tech fee for 2026-27?",
        "expected": [
            "cannot", "not available", "may change",
            "couldn't find", "could not find",
            "verify", "not provided", "don't have",
            "do not have", "not specified"
        ]
    }
]

documents = load_text_files("knowledge_base")

if not documents:
    print("ERROR: No knowledge-base documents found.")
    raise SystemExit

chunks, sources, embeddings = create_embeddings(documents)

passed = 0
failed = 0
skipped = 0

print("\n========== FINAL ANSWER TESTS ==========")

for number, test in enumerate(tests, start=1):
    question = test["question"]
    print(f"\nTest {number}: {question}")

    results = search_documents(
        question, chunks, sources, embeddings, top_k=1
    )

    if not results or results[0]["score"] < 0.45:
        print("Answer: No sufficiently relevant information found.")
        answer = (
            "I couldn't find verified information "
            "to answer that question."
        )
    else:
        try:
            response = generate_answer(question, results)
            answer = response["answer"]

        except Exception as error:
            error_message = str(error).lower()

            if any(term in error_message for term in [
                "429", "resource_exhausted", "quota",
                "rate limit", "too many requests"
            ]):
                print("API quota/rate limit reached.")
                print("Stopping Gemini tests to avoid more requests.")
                skipped = len(tests) - number + 1
                break

            print("API error:", error)
            failed += 1
            continue

    print("Answer:", answer)

    answer_lower = answer.lower()

    if any(word.lower() in answer_lower
           for word in test["expected"]):
        print("PASS: Expected keywords found.")
        passed += 1
    else:
        print("REVIEW: Expected keywords not found.")
        failed += 1

print("\n========== TEST SUMMARY ==========")
print("Passed:", passed)
print("Needs review:", failed)
print("Skipped:", skipped)
print("Total:", len(tests))
print("\nKeyword checks are basic; manually verify")
print("that answers are accurate and supported by sources.")
