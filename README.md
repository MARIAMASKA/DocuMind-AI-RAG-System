<div align="center">

<img src="https://img.icons8.com/fluency/96/brain.png" width="80"/>

# DocuMind AI

### End-to-End Retrieval-Augmented Generation (RAG) System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-8B5CF6?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-22C55E?style=for-the-badge)](https://www.trychroma.com)
[![RAG](https://img.shields.io/badge/Architecture-RAG-F97316?style=for-the-badge)](https://arxiv.org/abs/2005.11401)

*Transforming static documents into interactive AI-powered knowledge systems.*

</div>

---

## 📽️ Demo

<p align="center">
  <img src="assets/demo.gif" width="800" alt="DocuMind AI Demo"/>
</p>

<p align="center">
  <em>Upload → Semantic Indexing → AI Summary → MCQ Generation → Context-Aware Chat</em>
</p>

---

## 🚀 Overview

**DocuMind AI** is a full-stack AI application that implements a complete Retrieval-Augmented Generation (RAG) pipeline — turning any static document into a living, queryable knowledge base.

Unlike basic LLM apps, DocuMind **grounds every response strictly in retrieved document context**, dramatically reducing hallucinations and keeping answers accurate and relevant.

| Feature | Description |
|---|---|
| 📄 **Document Upload** | Supports PDF, DOCX, and TXT formats |
| 🧠 **AI Summarization** | Structured summaries generated from document content |
| 🎯 **MCQ Generation** | 10 auto-generated multiple-choice questions with explanations |
| 💬 **Contextual Chat** | Semantic retrieval-powered Q&A grounded in your document |
| 📦 **Vector Persistence** | Embeddings stored and reused via ChromaDB |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│                    User Interface                │
│          (Drag & Drop Upload + Chat UI)          │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│                  Flask Backend                   │
│                                                  │
│  ① Text Extraction  ──  pdfplumber / python-docx │
│  ② Chunking         ──  RecursiveCharacterSplitter│
│  ③ Embedding        ──  MiniLM (SentenceTransf.) │
│  ④ Vector Storage   ──  ChromaDB (persistent)    │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
          Top-K Semantic Retrieval
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│              Gemini 2.5 Flash                    │
│                                                  │
│   Summary  │  MCQs  │  Context-Aware Answers     │
└─────────────────────────────────────────────────┘
```

---

## 🧠 Core AI Concepts

| Concept | Implementation |
|---|---|
| **RAG Pipeline** | Full retrieve-then-generate architecture |
| **Semantic Search** | Embedding similarity over document chunks |
| **Top-K Retrieval** | Most relevant chunks fed to the LLM |
| **Hallucination Control** | Context-restricted answering with explicit fallback |
| **Vector Indexing** | Persistent ChromaDB storage |
| **Structured Output** | JSON-parsed MCQs and summaries |

---

## 🛠️ Tech Stack

**Backend**

- [Flask](https://flask.palletsprojects.com/) — Lightweight Python web framework
- [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) — LLM for generation
- [SentenceTransformers (MiniLM)](https://www.sbert.net/) — Embedding model
- [ChromaDB](https://www.trychroma.com/) — Persistent vector database
- [LangChain Text Splitters](https://python.langchain.com/) — Intelligent chunking

**Frontend**

- Custom modern UI with animated interactive components
- Drag & drop file upload
- Real-time streaming chat interface

---

## 📂 Project Structure

```
DocuMind-AI-RAG-System/
│
├── app.py                  # Main Flask application & RAG pipeline
├── templates/
│   └── index.html          # Frontend UI
├── chroma_db/              # Persistent vector store (auto-generated)
├── uploads/                # Temporary document storage (auto-generated)
├── assets/
│   └── demo.gif            # Demo preview
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DocuMind-AI-RAG-System.git
cd DocuMind-AI-RAG-System
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

> Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Run the application

```bash
python app.py
```

Open your browser and navigate to **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🎯 Example Workflow

```
1. Upload a research paper or any document
       ↓
2. System splits text into semantic chunks
       ↓
3. Embeddings generated & stored in ChromaDB
       ↓
4. AI generates a structured document summary
       ↓
5. 10 MCQs auto-created with explanations
       ↓
6. Ask any contextual question — answers grounded in your document
```

---

## 🔐 Hallucination Control Strategy

DocuMind AI uses a multi-layered approach to ensure reliable, grounded responses:

- **Context-only answering** — The LLM is instructed to answer solely from retrieved chunks
- **Top-3 semantic retrieval** — Only the most relevant document segments are passed to the model
- **Explicit fallback** — If the answer is not in the document, the system says so honestly
- **Structured generation constraints** — Output schemas enforce consistent, parseable responses

---

## 📈 Roadmap

- [ ] Cross-encoder re-ranking for improved retrieval precision
- [ ] Evaluation metrics (Faithfulness, Context Precision, Answer Relevancy)
- [ ] Multi-document memory and cross-document querying
- [ ] Streaming responses
- [ ] Token usage monitoring & cost dashboard
- [ ] Cloud deployment (GCP / AWS)

---

## 👩‍💻 Author

<div align="center">

**Maria Gamal**  
*AI Engineer · NLP Specialist*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com)

</div>

---

<div align="center">

*If you found this project helpful, consider giving it a ⭐*

</div>
