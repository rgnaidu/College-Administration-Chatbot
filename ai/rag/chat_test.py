
from document_loader import load_text_files
from embeddings import create_embeddings, search_documents
from answer_generator import generate_answer

# Load college knowledge base
documents = load_text_files("knowledge_base")

if not documents:
    print("No college documents found.")
    raise SystemExit

# Create document embeddings
chunks, sources, embeddings = create_embeddings(documents)

if not chunks:
    print("No information available in the knowledge base.")
    raise SystemExit

# Get student's question
question = input("\nAsk your college question: ").strip()

if not question:
    print("Please enter a question.")
    raise SystemExit

# Retrieve only the best-matching chunk
results = search_documents(
    question,
    chunks,
    sources,
    embeddings,
    top_k=1
)

# Generate one answer
if not results or results[0]["score"] < 0.45:
    print(
        "\nAnswer: I couldn't find sufficiently relevant, "
        "verified information in the college records. "
        "Please check the official college website."
    )
else:
    response = generate_answer(question, results)

    print("\nAnswer:", response["answer"])

    if response.get("source"):
        print("Source:", response["source"])
