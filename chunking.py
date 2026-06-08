
import os
import chromadb

folder_path = "./study_notes"

# Fresh database
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("study_notes_chunked")

def chunk_by_line(text):
    lines = text.split("\n")
    chunks = [line.strip() for line in lines if line.strip()]
    return chunks

def load_and_chunk_file(filepath, collection):
    filename = os.path.basename(filepath)

    with open(filepath, "r") as file:
        text = file.read()

    chunks = chunk_by_line(text)
    print(f"📄 {filename} → {len(chunks)} chunks")

    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({
            "source": filename,
            "chunk_id": i,
            "total_chunks": len(chunks)
        })
        ids.append(f"{filename}_chunk_{i}")

    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def print_results(query, results):
    print(f"\n🔍 Query: '{query}'")
    print("─" * 50)
    docs      = results["documents"][0]
    metas     = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, dist) in enumerate(
        zip(docs, metas, distances), 1
    ):
        source   = meta.get("source", "unknown")
        chunk_id = meta.get("chunk_id", "?")
        print(f"{i}. Source: {source} | Chunk: {chunk_id}")
        print(f"   Content: {doc[:80]}...")
        print(f"   Distance: {dist:.4f}")

# Load ALL files with chunking
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        filepath = os.path.join(folder_path, filename)
        load_and_chunk_file(filepath, collection)

print(f"\n📚 All files chunked and stored!")

# Query
results = collection.query(
    query_texts=["What is RAG?"],
    n_results=3
)
print_results("What is RAG?", results)
