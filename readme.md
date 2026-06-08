An AI study assistant that answers questions, explains topics, and generates quizzes from YOUR own study notes — powered by RAG (Retrieval Augmented Generation).

🚀 Features

📖 Explain Topics — AI explains concepts using ONLY your notes
📝 Generate Quizzes — Creates quizzes grounded in your documents
❓ Answer Questions — Answers from your notes with sources cited
🚫 No Hallucination — Says "I don't know" when answer isn't in your notes
📚 Cite Sources — Every answer shows which file it came from
🔄 Any Documents — Works with any .txt study notes you provide


🛠️ Built With

Python 3.9
OpenAI API — GPT-3.5-turbo + text-embedding-3-small
ChromaDB — Local vector database for semantic search
RAG Pipeline — Retrieval Augmented Generation
python-dotenv — Secure API key management


🧠 How It Works
INDEXING (once at startup):
Your .txt files → Split into chunks → Embed each chunk → Store in ChromaDB

QUERY (every question):
Your question → Embed → Search ChromaDB → Retrieve relevant chunks
→ Send to OpenAI with context → Grounded answer + sources!

⚙️ Setup & Run
1. Clone the repo
bashgit clone https://github.com/balaji-code/rag-studybuddy.git
cd rag-studybuddy
2. Create virtual environment
bashpython3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Create .env file
OPENAI_API_KEY=your-key-here
5. Add your study notes
bashmkdir study_notes
# Add your .txt files to study_notes/
6. Run the app
bashpython rag_studybuddy.py

📸 Sample Usage
📚 Indexing documents...
   ✅ ai_concepts.txt → 5 chunks
   ✅ python_basics.txt → 5 chunks
   ✅ fastapi_notes.txt → 5 chunks
✅ Indexing complete!

🧠 Welcome to RAG StudyBuddy!
Powered by your study notes!

What would you like to do?
1. Explain a topic from my notes
2. Generate quiz from my notes
3. Ask a question
4. Exit

Enter choice (1-4): 3
Question: What are LLMs?

🤖 LLMs are Large Language Models trained on vast text data.
📚 Sources: ai_concepts.txt

Enter choice (1-4): 3
Question: Who is Elon Musk?

❌ Not found in your notes!

📁 Project Structure
rag-studybuddy/
├── study_notes/
│   ├── ai_concepts.txt
│   ├── python_basics.txt
│   └── fastapi_notes.txt
├── chroma_db/              ← auto-created
├── embeddings.py           ← similarity demo
├── vector_files.py         ← ChromaDB basics
├── chunking.py             ← document loading
├── rag_pipeline.py         ← core RAG pipeline
├── rag_studybuddy.py       ← main application
├── .env                    ← API keys (not committed)
├── .gitignore
└── requirements.txt

🗺️ Roadmap

 Document indexing with ChromaDB
 Semantic search with embeddings
 RAG pipeline with hallucination prevention
 Quiz generation from documents
 Source citation for every answer
 PDF document support
 Web interface with FastAPI + Streamlit
 Upload documents via UI
 Track quiz scores over time
 Support for multiple document collections


📚 Concepts Practised

RAG (Retrieval Augmented Generation) pipeline
Text embeddings with OpenAI
Vector similarity search with ChromaDB
Document chunking strategies
Semantic search with distance thresholds
Hallucination prevention with prompt engineering
Structured JSON outputs for quiz generation
Source citation and grounding


👨‍💻 Author
Balaji — AI Engineer in training
Building towards a full AI-powered study platform with web interface, PDF support, and progress tracking.

📄 License
MIT