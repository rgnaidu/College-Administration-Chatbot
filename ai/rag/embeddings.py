
from sentence_transformers import SentenceTransformer, util
from document_loader import load_text_files
from chunker import split_text

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(documents):
    chunks = []
    sources = []

    for document in documents:
        text_chunks = split_text(document["text"])

        for chunk in text_chunks:
            chunks.append(chunk)
            sources.append(document["source"])

    if not chunks:
        return [], [], None

    embeddings = model.encode(
        chunks,
        convert_to_tensor=True
    )

    return chunks, sources, embeddings


def search_documents(question, chunks, sources, embeddings):
    if not chunks or embeddings is None:
        return []

    question_embedding = model.encode(
        question,
        convert_to_tensor=True
    )

    scores = util.cos_sim(
        question_embedding,
        embeddings
    )[0]

    best_indices = scores.argsort(
        descending=True
    )[:1]

    results = []

    for index in best_indices:
        results.append({
            "text": chunks[index],
            "source": sources[index],
            "score": float(scores[index])
        })

    return results


if __name__ == "__main__":
    documents = load_text_files("knowledge_base")

    chunks, sources, embeddings = create_embeddings(documents)

    print("Documents loaded:", len(documents))
    print("Chunks created:", len(chunks))

    question = input("\nAsk a college question: ")

    results = search_documents(
        question,
        chunks,
        sources,
        embeddings
    )

    print("\nRelevant information:")

    for result in results:
        print("\nSource:", result["source"])
        print("Similarity:", round(result["score"], 3))
        print("Text:", result["text"])
