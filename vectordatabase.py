import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("study_notes")

# upsert instead of add — safe for reruns!
collection.upsert(
    documents=[
        "Python functions are reusable blocks of code",
        "RAG retrieves relevant documents before generating",
        "Vector databases store embeddings for similarity search",
        "FastAPI builds REST APIs quickly in Python",
        "Embeddings convert text to numerical vectors"
    ],
    metadatas=[
        {"topic": "python"},
        {"topic": "AI"},
        {"topic": "AI"},
        {"topic": "python"},
        {"topic": "AI"}
    ],
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
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
        print(f"{i}. {doc}")
        print(f"   Topic: {meta['topic']} | Distance: {dist:.4f}")

# Query 1 — AI topics
results1 = collection.query(
    query_texts=["How do I search documents semantically?"],
    n_results=2,
    where={"topic": "AI"}
)
print_results("How do I search documents semantically?", results1)

# Query 2 — Python topics
results2 = collection.query(
    query_texts=["What is Python used for?"],
    n_results=2,
    where={"topic": "python"}
)
print_results("What is Python used for?", results2)


