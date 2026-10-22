
from document_loader import load_text_files
from embeddings import create_embeddings, search_documents

# Questions and keywords expected in the best retrieved result
tests = [
    {
        "question": "Where is GVPCEW located?",
        "expected": ["kommadi", "madhurawada"]
    },
    {
        "question": "How are Category-A seats filled?",
        "expected": ["apsc he", "apeapcet", "counselling"]
    },
    {
        "question": "What is the exact B.Tech fee for 2026-27?",
        "expected": ["fee", "2024", "change"]
    },
    {
        "question": "Where can I find examination notifications?",
        "expected": ["examination", "notification"]
    },
    {
        "question": "What are the college contact details?",
        "expected": ["gvpcew", "phone", "email"]
    },
    {
        "question": "Where can I find admission information?",
        "expected": ["admission", "admissionspage.php"]
    },
    {
        "question": "Where can I find the academic calendar?",
        "expected": ["calendar", "academic"]
    },
    {
        "question": "Where can I find placement information?",
        "expected": ["placement", "placementinfo.php"]
    },
    {
        "question": "What documents are required for admission?",
        "expected": ["documents", "admission"]
    },
    {
        "question": "Where can I find the college regulations and syllabus?",
        "expected": ["regulations", "syllabus"]
    }
]

documents = load_text_files("knowledge_base")

if not documents:
    print("ERROR: No knowledge-base documents found.")
    raise SystemExit

chunks, sources, embeddings = create_embeddings(documents)

if not chunks:
    print("ERROR: No chunks available for testing.")
    raise SystemExit

passed = 0
failed = 0

print("\n========== RAG RETRIEVAL TESTS ==========")
print("Questions to test:", len(tests))

for number, test in enumerate(tests, start=1):
    results = search_documents(
        test["question"],
        chunks,
        sources,
        embeddings,
        top_k=1
    )

    print(f"\nTest {number}: {test['question']}")

    if not results:
        print("FAIL: No result retrieved.")
        failed += 1
        continue

    best = results[0]
    retrieved_text = best["text"].lower()

    matched = [
        word for word in test["expected"]
        if word in retrieved_text
    ]

    # At least one expected keyword must be present
    if matched:
        print("PASS: Expected information found.")
        passed += 1
    else:
        print("FAIL: Expected keywords not found.")
        failed += 1

    print("Source:", best["source"])
    print("Similarity:", round(best["score"], 3))
    print("Retrieved:", best["text"][:250].replace("\n", " "))

print("\n========== TEST SUMMARY ==========")
print("Passed:", passed)
print("Failed:", failed)
print("Total:", len(tests))
print("\nNote: These are basic retrieval checks, not proof")
print("that the final Gemini answer is factually correct.")
