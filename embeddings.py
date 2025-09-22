# embeddings.py
import faiss
import numpy as np
from ollama import Ollama

DIM = 512  # Adjust to your Ollama embedding dimension
index = faiss.IndexFlatL2(DIM)
metadata = []
client = Ollama()

def get_embedding(text):
    emb = client.embed(model="llama2-mini", text=text)
    return np.array(emb, dtype='float32')

def add_to_index(text, meta):
    vec = get_embedding(text).reshape(1, -1)
    index.add(vec)
    metadata.append(meta)

def retrieve(query, top_k=5):
    qvec = get_embedding(query).reshape(1, -1)
    D, I = index.search(qvec, top_k)
    return [metadata[i] for i in I[0]]

