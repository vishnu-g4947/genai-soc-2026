# 🤖 HybridSight

HybridSight is a hybrid AI assistant built using Streamlit and LangGraph. It can answer questions from uploaded PDFs, search the web, retrieve information from Wikipedia, and analyze images—all within the same conversation.

---

## ✨ Features

- 📄 PDF Question Answering using FAISS
- 🔍 Web Search with DuckDuckGo
- 📚 General Knowledge with Wikipedia
- 🖼️ Image Understanding using Gemini
- 💬 Multi-chat support
- 🧠 Conversation memory with SQLite
- ⚡ Real-time streaming responses

---

## 🛠️ Tech Stack

- Streamlit
- LangGraph
- LangChain
- Groq
- Google Gemini
- FAISS
- HuggingFace Embeddings
- DuckDuckGo Search
- Wikipedia API
- SQLite

---

## 📁 Project Structure

```text
week5-hybridsight/
│
├── tools/
│   ├── tools_rag.py
│   ├── tools_search.py
│   ├── tools_vision.py
│   └── shared_state.py
│
├── agent.py
├── app.py
├── requirements.txt
├── .env
└── .gitignore
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/vishnu-g4947/genai-soc-2026.git
```

Move into the project folder:

```bash
cd genai-soc-2026/week5-hybridsight
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file and add:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧪 Test Cases

### PDF Tool

- Upload a PDF and ask:
  - "Summarize the document."
  - "Extract important information."

### Web Search Tool

- "Search the web about Surat."
- "Latest AI news."

### Wikipedia Tool

- "Who is Sundar Pichai?"
- "Explain quantum computing."

### Vision Tool

- Upload an image and ask:
  - "Describe this image."
  - "Extract the text."

---

## 👨‍💻 Author

**Vishnu Gabani**

Built as part of the GenAI SOC 2026 program.