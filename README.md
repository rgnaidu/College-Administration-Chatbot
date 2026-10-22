# College Administration Chatbot

An AI-powered college administration chatbot designed to answer student questions using college-specific information, Retrieval-Augmented Generation (RAG), and the Gemini API.

## Features

- Answers questions using college information stored in a knowledge base.
- Retrieves relevant text using semantic embeddings.
- Generates answers using Google's Gemini model.
- Provides a FastAPI backend with interactive API documentation.
- Includes a web-based chat interface.
- Provides fallback responses when the AI service is unavailable.
- Includes basic retrieval and answer tests.

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI, Uvicorn
- **RAG:** Sentence Transformers, NumPy
- **AI model:** Google Gemini API
- **Knowledge base:** College FAQ and overview text files

## Project Structure

```text
College-Administration-Chatbot/
├── ai/
│   └── rag/
├── backend/
│   └── rag_api.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── knowledge_base/
│   ├── college_overview.txt
│   └── gvpcew_faq.txt
├── docs/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.12 recommended
- Git (optional, if cloning from GitHub)
- A Google Gemini API key

## Setup Instructions

### 1. Get the project

Extract the ZIP file or clone the repository.

```bash
git clone -b ai-rag https://github.com/rgnaidu/College-Administration-Chatbot.git
cd College-Administration-Chatbot
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Create a copy of `.env.example` named `.env`.

Add your own Gemini API key:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not share or commit `.env`.

### 5. Start the backend

From the project root, run:

```powershell
python -m uvicorn backend.rag_api:app --reload
```

The API should be available at:

- API: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

Keep the backend terminal running while using the chatbot.

### 6. Open the frontend

Open `frontend/index.html` using VS Code Live Server. Ensure the backend is running at `http://127.0.0.1:8000`.

## API Usage

Endpoint:

```text
POST /chat
```

Example request:

```json
{
  "question": "What is the college address?"
}
```

The response includes a status, answer, and source information when available.

## Testing

Run the retrieval tests from the project root:

```powershell
python ai/rag/test_retrieval.py
```

The answer-generation tests may call the Gemini API and consume API quota:

```powershell
python ai/rag/test_answers.py
```

## Important Notes

- Answers depend on the accuracy and freshness of the college knowledge base.
- Confirm current fees, admission deadlines, and other time-sensitive details with official college sources.
- A successful local test does not mean the application is deployed publicly.
- Keep API keys private. Never upload `.env` or `.venv`.
- The embedding model may download automatically on first use.

## Repository

GitHub: https://github.com/rgnaidu/College-Administration-Chatbot

Development branch: `ai-rag`
