
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import sys
from pathlib import Path

# Locate the existing RAG service
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAG_FOLDER = PROJECT_ROOT / "ai" / "rag"

sys.path.insert(0, str(RAG_FOLDER))

from rag_service import ask_college_question

app = FastAPI(
    title="GVPCEW College Administration Chatbot API",
    version="1.0.0"
)

# Allow the frontend to connect during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "GVPCEW Chatbot API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    return ask_college_question(request.question)
