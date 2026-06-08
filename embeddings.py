from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np

texts = [
        "Python is a programming language",
        "Python is used for AI development",
        "Cats are domestic animals",
        "Dogs are loyal pets",
        "Machine learning uses algorithms"
    ]

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    # How similar are two embeddings?
    # Returns: 1.0 = identical, 0.0 = completely different
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

embeddings_list =[]
for text in texts:
  embedding = get_embedding(text)
  embeddings_list.append(embedding)
  print(f"Dimensions: {len(embedding)}")     # → 1536
  print(f"First 5 numbers: {embedding[:5]}")
  
for i, embedding in enumerate(embeddings_list):
   if i == 0:
     continue
   similarity = cosine_similarity(embeddings_list[0], embedding)
   print(f"{texts[0][:30]} vs {texts[i][:30]} → {similarity:.4f}")  

