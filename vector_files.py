import chromadb
import os
folder_path = "./study_notes"
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("study_notes")
def load_folder_to_chromadb(folder_path, collection):
    documents = []
    metadatas = []
    ids = []

    for i, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)

            with open(filepath, "r") as file:
                content = file.read()

            documents.append(content)
            metadatas.append({
                "source": filename,
                "type": "text"
            })
            ids.append(f"doc_{i}")
            print(f"✅ Loaded: {filename}")

    # Store in vector database!
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"\n📚 {len(documents)} documents stored!")

def print_results(query, results):
    print(f"\n🔍 Query: '{query}'")
    print("─" * 50)
    docs      = results["documents"][0]
    metas     = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, dist) in enumerate(
        zip(docs, metas, distances), 1
    ):
        print(f"{i}. Source: {meta.get('source','unknown')}")
        print(f"   Content: {doc[:80]}...")
        print(f"   Distance: {dist:.4f}")

load_folder_to_chromadb(folder_path, collection)

# Query
results = collection.query(
    query_texts=["How do I define a function in Python?"],
    n_results=2
)
print_results("How do I define a function in Python?", results)