import re

def split_text(text, chunk_size=300, overlap=50):
    text = text.strip()

    # Split before each new FAQ question
    sections = re.split(r'(?=Question:)', text)

    chunks = []

    for section in sections:
        section = section.strip()

        if not section:
            continue

        if len(section) <= chunk_size:
            chunks.append(section)
        else:
            start = 0

            while start < len(section):
                end = min(start + chunk_size, len(section))
                chunk = section[start:end].strip()

                if chunk:
                    chunks.append(chunk)

                if end == len(section):
                    break

                start = end - overlap

    return chunks