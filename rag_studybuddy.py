import os
import json
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_chroma = chromadb.PersistentClient(path="./chroma_db")
collection = client_chroma.get_or_create_collection("study_notes_chunked")

STUDY_NOTES_FOLDER = "./study_notes"

#------------------------------------
# Indexing 
#------------------------------------

def chunk_by_line(text):
    lines = text.split("\n")
    return [line.strip() for line in lines if line.strip()]

def index_documents(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r") as file:
                text = file.read()
            chunks = chunk_by_line(text)
            documents,metadatas,ids = [],[],[] 

            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({"source": filename, 
                         "chunk_id": i })
                ids.append(f"{filename}_chunk_{i}")

            collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids)
            print(f"   ✅ {filename} → {len(chunks)} chunks indexed!")
    print(f"\n📚 All documents indexed!")
#------------------------------------
# RAG retrieval
#------------------------------------

def retrieve_context(question, n_results=3, distance_threshold=1.2):
    results = collection.query(
        query_texts=[question],
        n_results=n_results)
    if results["documents"] is None or results["metadatas"] is None or results["distances"] is None:
        return []
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    relevant_chunks = []
    for doc, meta, dist in zip(docs, metas, distances):
        if dist < distance_threshold:
            relevant_chunks.append({
                "content": doc,
                "source": meta.get("source", "unknown"),
                "distance": dist
            })
    return relevant_chunks

#------------------------------------
   #studybuddy features  
#------------------------------------

def explain_topic(topic):
    chunks = retrieve_context(f"Explain the topic: {topic}")
    if not chunks:
     print(f"I couldn't find any information about {topic} in your notes.")
     return

    context = "\n\n".join([c["content"] for c in chunks])
    sources = list(set([c["source"] for c in chunks]))

    response = client_openai.chat.completions.create(
              model="gpt-3.5-turbo",
              messages=[
                {
                    "role": "system",
                    "content": """You are StudyBuddy.
Explain topics using ONLY the provided context.
Do NOT add information from your training data.
Only use what is explicitly stated in the context."""
                },
                {
                    "role": "user",
                    "content": f"Topic: {topic}\n\nContext: {context}\n\nSources: {sources}"
                }
              ])
    print(f"💡 Explanation for {topic}: {response.choices[0].message.content}")
    print(f"📖 Sources: {', '.join(sources)}")

def generate_quiz_from_notes(topic):
    chunks = retrieve_context(topic)
    if not chunks:
        print(f"I couldn't find any information about {topic} in your notes.")
        return

    context = "\n\n".join([c["content"] for c in chunks])
    sources = list(set([c["source"] for c in chunks]))

    response = client_openai.chat.completions.create(
              model="gpt-3.5-turbo",
              messages=[
                {
                    "role": "system",
                    "content": """Generate a quiz in JSON format:
                  {
                    "topic": "topic name",
                    "questions": [{
                            "question": "question text",
                            "options": {"A": "opt1", "B": "opt2",
                                       "C": "opt3", "D": "opt4"},
                            "correct": "A",
                            "explanation": "why correct"
                        }
                    ]
                  }
                  Use ONLY the provided context!"""
                },
                {
                    "role": "user",
                    "content": f"Create 3 quiz questions from:\n{context}"
                }
              ],
              response_format={"type": "json_object"}
              )

    quiz = json.loads(response.choices[0].message.content or "{}")

    print(f"\n📝 Quiz from YOUR notes!")
    print(f"📚 Source: {', '.join(sources)}")
    print("=" * 50)

    for i, q in enumerate(quiz["questions"], 1):
        print(f"\nQ{i}: {q['question']}")
        for opt, text in q["options"].items():
            print(f"   {opt}) {text}")

    answer = input("\nSee answers? (yes/no): ").strip().lower()
    if answer == "yes":
        print("\n✅ Answers:")
        for i, q in enumerate(quiz["questions"], 1):
            print(f"Q{i}: {q['correct']} — {q['explanation']}")

#------------------------------------
# Main App
#------------------------------------

def main():
    index_documents(STUDY_NOTES_FOLDER)

    print("Welcome to RAG Studdy Buddy ! 📚🤖")
    print("Powered by your study notes! \n")

    while True:
        print("\nWhat would you like to do?")
        print("1. Explain a topic from my notes")
        print("2. generate quiz from my notes")
        print("3. Ask a question")
        print("4. Exit")


        choice = input("Enter your choice (1/2/3/4): ").strip()
        if choice == "1":
            topic = input("Enter topic (e.g. RAG, Python, FastAPI): ").strip()
            explain_topic(topic)
        elif choice == "2":
            topic = input("Enter topic (e.g. Python, RAG, FastAPI): ").strip()
            generate_quiz_from_notes(topic)
        elif choice == "3":
            question = input("Question: ").strip()
            chunks = retrieve_context(question)
            if not chunks:
                print("❌ Not found in your notes!")
    
            else:
                context = "\n".join([c["content"] for c in chunks])
                sources = list(set([c["source"] for c in chunks]))
                response = client_openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "Answer ONLY from the context. Say 'I don't know' if not in context."
                        },
                        {
                            "role": "user",
                            "content": f"CONTEXT:\n{context}\n\nQUESTION: {question}"
                        }
                    ]
                )
                print(f"\n🤖 {response.choices[0].message.content}")
                print(f"📚 Sources: {', '.join(sources)}")

        elif choice == "4":
            print("\n👋 Goodbye! Keep studying!")
            break

        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()