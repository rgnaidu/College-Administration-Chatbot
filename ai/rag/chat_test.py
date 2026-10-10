from document_loader import load_text_files
from embeddings import create_embeddings, search_documents
from answer_generator import generate_answer


# Step 1: Load college documents
documents = load_text_files("knowledge_base")

if not documents:
    print("No text documents found in knowledge_base.")
    raise SystemExit

print("Documents loaded:", len(documents))


# Step 2: Create embeddings
chunks, sources, embeddings = create_embeddings(documents)

if not chunks:
    print("No text chunks available.")
    raise SystemExit

print("Chunks created:", len(chunks))


# Step 3: Ask a question
question = input("\nAsk a college question: ").strip()

if not question:
    print("Please enter a question.")
    raise SystemExit


# Step 4: Retrieve relevant information
results = search_documents(
    question,
    chunks,
    sources,
    embeddings
)


# Step 5: Avoid answering when the match is too weak
# This threshold is an initial testing value.
relevant_results = [
    result for result in results
    if result["score"] >= 0.45
]


# Step 6: Generate an answer using Gemini
try:
    result = generate_answer(question, relevant_results)

    print("\nChatbot answer:")
    print(result["answer"])

    if result["source"]:
        print("\nSource:", result["source"])
    else:
        print("\nSource: No verified source found.")

except Exception as error:
    print("\nCould not generate the answer.")
    print("Error:", error)