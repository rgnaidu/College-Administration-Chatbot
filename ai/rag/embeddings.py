
from sentence_transformers import SentenceTransformer, util
from document_loader import load_text_files
from chunker import split_text

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

    embeddings = model.encode(chunks, convert_to_tensor=True)

    return chunks, sources, embeddings




def search_documents(question, chunks, sources, embeddings, top_k=3):
    import re

    if not chunks or embeddings is None:
        return []

    question_embedding = model.encode(
        question,
        convert_to_tensor=True
    )

    scores = util.cos_sim(question_embedding, embeddings)[0]
    query_words = set(re.findall(r"[a-z0-9]+", question.lower()))

    topic_groups = {
        "fees": {
            "fee", "fees", "tuition", "cost", "amount", "charges"
        },
        "admissions": {
            "admission", "admissions", "apply", "application",
            "counselling", "eligibility", "documents"
        },
        "exams": {
            "exam", "examination", "hall", "results"
        },
        "calendar": {
            "calendar", "timetable", "schedule"
        },
        "placements": {
            "placement", "placements", "salary", "recruitment"
        },
    }

    active_topics = {
        topic for topic, words in topic_groups.items()
        if query_words & words
    }

    results = []

    for index, chunk in enumerate(chunks):
        text = chunk.lower()

        match = re.search(
            r"question:\s*(.*?)(?:\n|$)",
            text
        )

        faq_question = match.group(1) if match else text
        faq_words = set(
            re.findall(r"[a-z0-9]+", faq_question)
        )

        overlap = len(query_words & faq_words)
        score = float(scores[index]) + 0.03 * overlap

        if "fees" in active_topics:
            if not re.search(
                r"\b(fee|fees|tuition|cost|amount|charges)\b",
                text
            ):
                score -= 0.15

        if "admissions" in active_topics:
            if "admissions" not in text and not re.search(
                r"\b(admission|apply|application|counselling|eligibility)\b",
                text
            ):
                score -= 0.10

        results.append({
            "text": chunks[index],
            "source": sources[index],
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]
