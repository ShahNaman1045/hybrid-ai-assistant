# Hybrid AI Assistant

A Hybrid AI Assistant built with **FastAPI**, **OpenAI**, **SQLite**, and **ChromaDB** that intelligently answers enterprise questions by choosing between:

- **SQL** → for structured database queries
- **RAG** → for policy/document questions
- **SQL + RAG** → for questions requiring both structured data and enterprise documents

The project intentionally avoids high-level orchestration frameworks (LangChain, LangGraph, LlamaIndex, CrewAI, AutoGen, etc.) and implements the reasoning and orchestration manually using the OpenAI SDK.

---

# Features

- Hybrid SQL + RAG architecture
- Manual ReAct-style orchestration
- Automatic SQL generation using OpenAI
- SQL safety validation
- Automatic SQL repair and retry
- PDF ingestion into ChromaDB
- Semantic document retrieval using OpenAI embeddings
- Structured JSON responses
- Source citations
- Execution metadata
- REST API using FastAPI

---

# Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| LLM | OpenAI GPT-4.1 Mini |
| Embeddings | OpenAI text-embedding-3-small |
| Database | SQLite |
| ORM | SQLAlchemy |
| Vector Database | ChromaDB |
| PDF Parsing | PyMuPDF |
| Language | Python 3.11+ |

---

# Project Structure

```
HYBRID-AI-ASSISTANT/

├── app/
│   ├── agent/
│   ├── api/
│   ├── database/
│   ├── llm/
│   ├── prompts/
│   ├── rag/
│   ├── sql/
│   ├── utils/
│   ├── config.py
│   └── main.py
│
├── chroma_db/
│
├── data/
│   ├── database/
│   └── documents/
│
├── scripts/
│
├── requirements.txt
├── README.md
└── .env
```

---

# Architecture

```
                    User
                      │
                      ▼
               FastAPI /ask
                      │
                      ▼
              Manual Planner
                      │
         ┌────────────┼────────────┐
         │                │               │
         ▼               ▼               ▼
       SQL               RAG             BOTH
         │                │
         ▼               ▼
   SQLite DB           ChromaDB
         │                │
         └──────┬──────┘
                  ▼
      Final Answer Generator
                  │
                  ▼
            JSON Response
```

---

# SQL Flow

```
Question

↓

Generate SQL

↓

Validate SQL

↓

Execute SQL

↓

If Failed

↓

Repair SQL

↓

Execute Again

↓

Return Result
```

---

# RAG Flow

```
PDF Documents

↓

Extract Text

↓

Chunk Text

↓

OpenAI Embeddings

↓

Store in ChromaDB

↓

Semantic Search

↓

Relevant Context
```

---

# Manual ReAct Flow

Instead of using LangChain or LangGraph, the application implements a lightweight manual orchestration flow.

```
Question

↓

Planner

↓

Choose Tool

↓

SQL
RAG
or BOTH

↓

Execute Tool(s)

↓

Observe Results

↓

Generate Final Answer
```

---

# Setup

## Clone Repository

```bash
git clone <repository-url>

cd hybrid-ai-assistant
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

```
OPENAI_API_KEY=your_api_key

OPENAI_MODEL=gpt-4.1-mini

EMBEDDING_MODEL=text-embedding-3-small
```

---

# Database Setup

Convert the provided MySQL dump into SQLite.

```bash
python -m scripts.convert_database
```

Generate schema.

```bash
python -m scripts.test_schema
```

---

# Document Ingestion

Before asking document-related questions:

```bash
POST /ingest
```

or

```bash
python -m scripts.ingest_documents
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# API

## POST /ask

Example

```json
{
    "question":"Top 10 customers by revenue"
}
```

Response

```json
{
    "answer":"...",
    "sources":[
        "Travel_Policy.pdf (Page 2)"
    ],
    "metadata":{
        "action":"SQL",
        "execution_time_ms":1200
    }
}
```

---

## POST /ingest

Indexes all PDF documents into ChromaDB.

---

# Design Decisions

### Why SQLite?

The assignment dataset is static and does not require a running MySQL server. Converting to SQLite simplifies setup while preserving SQL capabilities.

---

### Why ChromaDB?

ChromaDB provides a lightweight embedded vector database suitable for semantic document retrieval without external infrastructure.

---

### Why OpenAI Embeddings?

Using OpenAI for both LLM inference and embeddings simplifies deployment and improves embedding quality.

---

### Why No LangChain?

The assignment explicitly prohibits high-level AI orchestration frameworks.

Therefore:

- SQL generation
- Tool selection
- SQL repair
- RAG retrieval
- Final orchestration

are implemented manually using the OpenAI SDK.

---

# Error Handling

The project includes:

- SQL validation
- SQL repair
- OpenAI error handling
- Database exception handling
- Safe SELECT-only execution
- Duplicate ingestion prevention

---

# Assumptions

- Questions are written in English.
- Database schema remains relatively stable.
- PDF documents are indexed before RAG queries.
- SQLite is sufficient for the provided dataset.

---

# Future Improvements

- Conversation memory
- Streaming responses
- Hybrid keyword + semantic search
- Query result caching
- Authentication
- Docker deployment
- Background document ingestion
- Unit and integration tests
