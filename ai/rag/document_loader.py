
from pathlib import Path
from pypdf import PdfReader
from docx import Document

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base"


def read_txt(file_path):
    return file_path.read_text(encoding="utf-8")


def read_pdf(file_path):
    reader = PdfReader(str(file_path))
    return "\n".join(
        page.extract_text() or "" for page in reader.pages
    )


def read_docx(file_path):
    document = Document(str(file_path))
    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


def load_documents(folder_path=KNOWLEDGE_BASE):
    documents = []
    folder = Path(folder_path)
    supported_extensions = {".txt", ".pdf", ".docx"}

    for file_path in folder.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        try:
            extension = file_path.suffix.lower()

            if extension == ".txt":
                text = read_txt(file_path)
            elif extension == ".pdf":
                text = read_pdf(file_path)
            else:
                text = read_docx(file_path)

            if not text.strip():
                print(f"Warning: No extractable text: {file_path.name}")
                continue

            documents.append({
                "text": text,
                "source": file_path.name
            })
            print(f"Loaded: {file_path.name}")

        except Exception as error:
            print(f"Could not read {file_path.name}: {error}")

    return documents


# Keeps compatibility with the existing embeddings.py
def load_text_files(folder_path=KNOWLEDGE_BASE):
    return load_documents(folder_path)


if __name__ == "__main__":
    documents = load_documents()
    print("\nDocuments loaded:", len(documents))

    for document in documents:
        print("\nSource:", document["source"])
        print("Characters:", len(document["text"]))
        print("Preview:", document["text"][:200])
