# 🚀 DocMind Backend

Backend API for **DocMind**, an AI-powered document assistant built with **FastAPI**, **PostgreSQL**, and **Google Gemini AI**.

The backend handles authentication, PDF upload & processing, document management, persistent chat history, and AI-powered question answering.

---

# ✨ Features

- 🔐 JWT Authentication
- 👤 User Registration & Login
- 📄 PDF Upload
- 📖 Automatic PDF Text Extraction
- 🤖 Google Gemini AI Integration
- 💬 Persistent Chat History
- 🧠 Conversation Memory
- 🗂️ Document Management
- 🗑️ Delete Documents & Chat History
- 🛡️ User-specific Data Isolation
- ⚡ RESTful APIs
- 🗄️ PostgreSQL Database

---

# 🛠️ Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT Authentication
- Google Gemini API
- PyPDF
- Python

---

# 🏗️ Architecture

```text
Flutter App
      │
      ▼
FastAPI Backend
      │
 ┌────┴────────────┐
 │                 │
 ▼                 ▼
PostgreSQL     Google Gemini
      │
      ▼
 Uploaded PDFs
```

---

# 📂 Project Structure

```
app/
├── crud.py
├── database.py
├── dependencies.py
├── models.py
├── oauth2.py
├── schemas.py
├── main.py
│
├── config.py
├── routers/
│   ├── auth.py
│   ├── documents.py
│   └── ai.py
│
├── services/
│   ├── gemini_service.py
│   └── pdf_service.py
│
└── uploads/
```

---

# 🔌 API Endpoints

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | `/auth/register` |
| POST | `/auth/login` |

---

## Documents

| Method | Endpoint |
|---------|----------|
| GET | `/documents/` |
| POST | `/documents/` |
| DELETE | `/documents/{id}` |

---

## AI

| Method | Endpoint |
|---------|----------|
| POST | `/ai/ask` |
| GET | `/ai/history/{document_id}` |

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/rishab0615/doc-ai-document-assistant-backend.git
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```env
DATABASE_URL=your_postgres_url

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

GEMINI_API_KEY=your_gemini_api_key
```

Run migrations

```bash
alembic upgrade head
```

Start the server

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 🔄 Request Flow

```text
User

↓

JWT Authentication

↓

Upload PDF

↓

Extract Text

↓

Store in PostgreSQL

↓

Ask Question

↓

Load Previous Chat History

↓

Send Context + Document to Gemini

↓

Store AI Response

↓

Return Answer
```

---

# 🔒 Authentication

Protected endpoints require a JWT access token.

```
Authorization: Bearer <access_token>
```

---

# 🚀 Future Improvements

- Refresh Tokens
- RAG (Vector Search)
- Streaming AI Responses
- OCR Support
- Multiple AI Providers
- Docker
- CI/CD
- Unit Tests

---

# 📱 Frontend

Flutter Client

https://github.com/rishab0615/doc-ai-flutter

---

# 👨‍💻 Author

**Rishab Sharma**

Flutter & FastAPI Developer

GitHub

https://github.com/rishab0615

Portfolio

https://rishabsharma.web.app

LinkedIn

https://www.linkedin.com/in/rishab-sharma-3ba404235/