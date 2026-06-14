# DocBuddy Pro

DocBuddy Pro is a simple Retrieval-Augmented Generation (RAG) application built using LangChain, ChromaDB, Groq, and Gradio.

Users can upload PDF documents, index them into a vector database, and ask questions about their documents. The application retrieves relevant chunks from the documents and uses an LLM to generate grounded answers.

---

# Application Demo

## Question Answering

Add screenshots here showing:

- PDF upload
- Indexed documents
- Generated answer
- Retrieved context accordion

---

# What is RAG?

RAG (Retrieval-Augmented Generation) is a technique that combines document retrieval with Large Language Models.

Instead of answering only from its training data, the model first retrieves relevant information from uploaded documents and then uses that information to generate an answer.

This helps reduce hallucinations and ensures answers are grounded in the provided documents.

---

# Features

- Upload multiple PDF files
- Automatic document chunking
- Embedding generation using HuggingFace embeddings
- ChromaDB vector storage
- Persistent vector database
- Retrieval-based question answering
- Groq LLM integration
- Anti-hallucination prompting
- Retrieved context viewer
- Gradio web interface

---

# Tech Stack

- Python
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq
- Gradio

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/genai-soc-2026.git

cd genai-soc-2026/week2-docbuddy
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Create a .env file

```env
GROQ_API_KEY=your_groq_api_key
```

## 4. Run the application

```bash
python app.py
```

The application will start on:

```text
http://127.0.0.1:7860
```

---

# Project Structure

```text
week2-docbuddy/
│
├── app.py
├── indexing.py
├── retrieval.py
├── persistence.py
├── config.py
├── requirements.txt
├── chroma_store/
└── README.md
```

---

# How It Works

1. User uploads one or more PDF documents.
2. PDFs are loaded and split into chunks.
3. Chunks are converted into embeddings.
4. Embeddings are stored in ChromaDB.
5. User asks a question.
6. Relevant chunks are retrieved from ChromaDB.
7. Retrieved context is sent to Groq LLM.
8. The answer is generated using only the retrieved context.

---

# Anti-Hallucination Testing

The system was tested with questions both present and absent from the uploaded documents.

## Questions Present in Documents

### Question 1

**Q:** What languages does Vishnu know?

**A:** C++, Python

---

### Question 2

**Q:** Which college does Vishnu study in?

**A:** DAIICT, Gandhinagar

---

### Question 3

**Q:** Which club is Vishnu a member of?

**A:** Electronics and Hardware Club (EHC)

---

### Question 4

**Q:** What is Vishnu's branch?

**A:** ICT-CS

---

### Question 5

**Q:** What internship/work experience does Vishnu have?

**A:** Data Annotator at DataAnnotation.tech

---

## Questions Not Present in Documents

### Question 1

**Q:** What is the capital of France?

**A:** I don't have enough information in the documents.

---

### Question 2

**Q:** Who wrote Hamlet?

**A:** I don't have enough information in the documents.

---

### Question 3

**Q:** What is the population of India?

**A:** I don't have enough information in the documents.

---

### Question 4

**Q:** Who won the FIFA World Cup 2022?

**A:** I don't have enough information in the documents.

---

### Question 5

**Q:** What is the tallest mountain in the world?

**A:** I don't have enough information in the documents.

---

# Multi-Document Retrieval Testing

Two documents were uploaded:

1. Vishnu_Gabani_Resume.pdf
2. 12_Chem.pdf

---

## Test 1 – Question from Resume

**Q:** What languages does Vishnu know?

**A:** C++, Python

**Source:** Vishnu_Gabani_Resume.pdf

---

## Test 2 – Question from Chemistry Document

**Q:** What is Chapter 7 in the chemistry syllabus?

**A:** (Answer retrieved from 12_Chem.pdf)

**Source:** 12_Chem.pdf

---

## Test 3 – Cross Document Retrieval

**Q:** What programming languages does Vishnu know and what is Chapter 7 in Chemistry?

**A:** Information retrieved from both documents.

**Sources:**

- Vishnu_Gabani_Resume.pdf
- 12_Chem.pdf

---

# What Worked Well

- ChromaDB persistence worked successfully.
- Retrieval was fast and accurate.
- Groq generated responses quickly.
- Multi-document retrieval functioned correctly.
- Gradio made UI development straightforward.

---

# Future Improvements

- Add source citations directly beside answers.
- Add conversation memory.
- Support DOCX and TXT files.
- Add reranking for better retrieval quality.
- Deploy the application online.
- Add chat history support.

---

# What I Learned

Through this project I learned:

- How Retrieval-Augmented Generation (RAG) works.
- Document chunking strategies.
- Embedding generation using HuggingFace models.
- Vector databases using ChromaDB.
- Retrieval with LangChain.
- Prompt engineering for grounded responses.
- Persistence of vector stores.
- Building interactive applications with Gradio.

---

# Author

Vishnu Gabani

DAIICT Gandhinagar

ICT-CS