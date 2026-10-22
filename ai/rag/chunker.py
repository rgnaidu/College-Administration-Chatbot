
import re


def split_text(text, chunk_size=1000, overlap=100):
    text = text.strip()

    # Split the knowledge base before each FAQ question
    sections = re.split(r"(?=Question:)", text)

    chunks = []

    for section in sections:
        section = section.strip()

        if not section:
            continue

        # Keep complete FAQ entries together when possible
        if section.startswith("Question:") and len(section) <= chunk_size:
            chunks.append(section)
            continue

        # Split long sections at paragraph boundaries where possible
        if len(section) <= chunk_size:
            chunks.append(section)
            continue

        start = 0

        while start < len(section):
            end = min(start + chunk_size, len(section))

            # Prefer ending at a newline rather than cutting a line
            if end < len(section):
                newline_position = section.rfind("\n", start, end)

                if newline_position > start:
                    end = newline_position

            chunk = section[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(section):
                break

            start = max(start + 1, end - overlap)

    return chunks
