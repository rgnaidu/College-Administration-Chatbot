
from pathlib import Path

def load_text_files(folder_path):
    documents = []

    folder = Path(folder_path)

    for file_path in folder.rglob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "text": text,
            "source": file_path.name
        })

    return documents


if __name__ == "__main__":
    documents = load_text_files("knowledge_base")

    print("Documents loaded:", len(documents))

    for document in documents:
        print("Source:", document["source"])
        print("Content:", document["text"][:200])
