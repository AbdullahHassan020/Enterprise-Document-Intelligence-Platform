# 📚 Enterprise Document Intelligence Platform

An AI-powered **Retrieval-Augmented Generation (RAG)** application that enables users to upload enterprise documents, perform semantic search, and interact with them through an intelligent conversational interface.

Developed as part of an **AI Engineering Internship – Week 2**.

---

## Features

- 📄 Upload PDF, TXT and MARKDOWN documents
- ✂️ Automatic document chunking
- 🧠 Embedding generation using Sentence Transformers
- 🗂 Persistent vector storage with ChromaDB
- 🔍 Semantic document retrieval
- 💬 Multi-chat conversational interface
- 📚 Enterprise document library
- 🎯 Prompt templates
- 📊 Workspace statistics dashboard
- 🧹 Chat management and export
- 🧠 Conversation memory

---

## Architecture

```text
User
   │
   ▼
Streamlit Frontend
   │
   ▼
Document Upload
   │
   ▼
Document Loader
   │
   ▼
Text Chunking
   │
   ▼
Embedding Generation
   │
   ▼
Chroma Vector Database
   │
   ▼
Retriever
   │
   ▼
OpenRouter LLM
   │
   ▼
AI Response
```

The detailed architecture diagram is available in the **docs** folder.

---

## Technology Stack

- Python
- Streamlit
- OpenRouter
- ChromaDB
- Sentence Transformers
- python-dotenv

---

## Project Structure

```text
components/
    chat.py
    document_filter.py
    document_library.py
    sidebar.py
    templates.py
    upload_panel.py

utils/
    loader.py
    chunker.py
    embeddings.py
    vectordb.py
    retriever.py
    document_manager.py
    memory.py
    openrouter.py

data/
    uploads/
    chroma_db/

app.py
requirements.txt
```

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd Retrieval-Augmented-Generation
```

### Create a virtual environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file using `.env.example`

Example

```env
OPENROUTER_API_KEY=your_api_key_here
```

### Run the application

```bash
streamlit run app.py
```

---
## Future Improvements

- Support additional document formats
- Hybrid retrieval
- Re-ranking
- Metadata filtering
- OCR support
- Cloud deployment
- User authentication

---
## Security

- API keys stored using environment variables
- No hard-coded secrets
- Persistent vector storage
- Local document management

---

## License

This project was developed for educational purposes as part of an AI Engineering Internship.
