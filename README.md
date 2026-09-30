# 📄 RAG-Based Document Assistant

An AI-powered document question-answering system built with **LangChain**, **ChromaDB**, and **OpenAI**. Upload your documents and ask questions — the assistant retrieves the most relevant content and generates accurate answers using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📂 Load and process multiple document types
- 🔍 Semantic search using vector embeddings
- 🧠 Accurate answers using LangChain RAG pipeline
- 💾 Persistent vector storage with ChromaDB
- ⚡ Fast retrieval with efficient document chunking

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| LangChain | RAG pipeline & chaining |
| ChromaDB | Vector store & embeddings storage |
| OpenAI | LLM & embeddings |
| Python | Core language |

---

## 📁 Project Structure

```
RAG-Based-Document-Assistant/
│
├── app.py                  # Main application entry point
├── main.py                 # Core logic
├── create_database.py      # Creates and populates ChromaDB vector store
├── requirements.txt        # Project dependencies
├── .env.example            # Environment variable template
├── README.md               # Project documentation
│
├── document loaders/       # Document loading utilities
├── retrievers/             # Retrieval chain components
└── vector store/           # Vector store configuration
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/RAG-Based-Document-Assistant.git
cd RAG-Based-Document-Assistant
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
```

Activate it:
- **Windows:** `.venv\Scripts\activate`
- **Mac/Linux:** `source .venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
Then fill in your actual API keys in `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

### 5. Create the Vector Database
```bash
python create_database.py
```

### 6. Run the Application
```bash
python app.py
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `LANGCHAIN_API_KEY` | Your LangChain API key |

> ⚠️ Never commit your `.env` file to GitHub. It is already added to `.gitignore`.

---

## 📝 How It Works

```
Your Document
     ↓
Document Loader
     ↓
Text Chunking
     ↓
Embeddings (OpenAI)
     ↓
Vector Store (ChromaDB)
     ↓
User Query → Semantic Search → Relevant Chunks → LLM → Answer
```

1. **Load** — Documents are loaded using LangChain document loaders
2. **Chunk** — Text is split into smaller overlapping chunks
3. **Embed** — Each chunk is converted to a vector embedding
4. **Store** — Embeddings are saved in ChromaDB
5. **Retrieve** — On query, the most similar chunks are fetched
6. **Generate** — LLM generates an answer using retrieved context

---

## 📦 Requirements

See `requirements.txt` for full list. Main dependencies:
```
langchain
chromadb
openai
python-dotenv
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/your-feature`)
3. Commit your changes (`git commit -m "feat: add your feature"`)
4. Push to the branch (`git push origin feat/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Your Name**
- GitHub: [AYUSHGUPTA9506](https://github.com/AYUSHGUPTA9506/)
