import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_chroma = chromadb.PersistentClient(path="./chroma_db")
collection = client_chroma.get_or_create_collection("study_notes_chunked")

def rag_query(question, n_results=3, distance_threshold=1.2):

    # Step 1 — Search ChromaDB
    print(f"\n🔍 Searching for: '{question}'")
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    # Step 2 — Get relevant chunks
    if results["documents"] is None or results["metadatas"] is None or results["distances"] is None:
        return "I couldn't find relevant information in your notes!"

    docs      = results["documents"][0]
    metas     = results["metadatas"][0]
    distances = results["distances"][0]

    # Step 3 — Filter by relevance
    relevant_chunks = []
    for doc, meta, dist in zip(docs, metas, distances):
        if dist < distance_threshold:
            relevant_chunks.append({
                "content": doc,
                "source": meta.get("source", "unknown"),
                "distance": dist
            })

    if not relevant_chunks:
        return "I couldn't find relevant information in your notes!"

    # Step 4 — Build context from chunks
    context = "\n\n".join([
        f"From {chunk['source']}:\n{chunk['content']}"
        for chunk in relevant_chunks
    ])

    print(f"📚 Found {len(relevant_chunks)} relevant chunks!")

    # Step 5 — Build prompt with context
    prompt = f"""Answer the question based ONLY on the context below.
If the answer is not in the context, say "I don't know based on your notes."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    # Step 6 — Send to OpenAI
    response = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful study assistant. Answer questions based only on the provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    # Step 7 — Return answer with sources
    sources = list(set([c["source"] for c in relevant_chunks]))
    return answer, sources


def ask_studybuddy(question):
    print(f"\n{'='*50}")
    print(f"❓ Question: {question}")
    print(f"{'='*50}")

    result = rag_query(question)

    if isinstance(result, str):
        print(f"\n🤖 Answer: {result}")
        return

    answer, sources = result
    print(f"\n🤖 Answer:\n{answer}")
    print(f"\n📖 Sources: {', '.join(sources)}")
    print(f"{'='*50}")

    
    
ask_studybuddy("What is RAG?")
ask_studybuddy("How do I define a function in Python?")
ask_studybuddy("What is the capital of France?")