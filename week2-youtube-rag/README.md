# 🎥 YouTube RAG Bot

A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about any YouTube video using its transcript.

## 🚀 Features

- Extract transcripts directly from YouTube videos
- Automatic transcript chunking using LangChain
- HuggingFace Embeddings for semantic understanding
- FAISS Vector Database for fast similarity search
- Retrieval-Augmented Generation (RAG)
- Groq Llama 3.1 integration for answer generation
- Interactive Gradio Web Interface
- Context-aware answers grounded in video content

---

## 🏗️ Architecture

```text
YouTube URL
     ↓
Transcript Extraction
     ↓
Chunking
     ↓
Embeddings
     ↓
FAISS Vector Store
     ↓
Retriever
     ↓
Relevant Context
     ↓
Groq LLM
     ↓
Answer
```

---

## 🛠️ Tech Stack

- Python
- LangChain
- FAISS
- HuggingFace Embeddings
- Groq API
- Gradio
- YouTube Transcript API

---

## 📂 Project Structure

```text
week2-youtube-rag/
│
├── app.py
├── indexing.py
├── persistence.py
├── retrieval.py
├── config.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/vishnu-g4947/genai-soc-2026.git
cd genai-soc-2026/week2-youtube-rag
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run

```bash
python app.py
```

Gradio will start locally:

```text
http://127.0.0.1:7860
```

---

## 📸 Demo

### Index a Video

- Paste a YouTube URL
- Click **Index Video**

### Ask Questions

Examples:

```text
What is this video about?

Summarize the key points.

What is the 70-30 rule mentioned in the video?

What tools are recommended for beginners?
```

---

## 🎯 Learning Outcomes

This project helped practice:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Embeddings
- Semantic Search
- Prompt Engineering
- LangChain
- LLM Integration
- Building AI Applications with Gradio

---

## 👨‍💻 Author

**Vishnu Gabani**

B.Tech ICT-CS @ DAU (Formerly DA-IICT)

GenAI | Software Development | Robotics