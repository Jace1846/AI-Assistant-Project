import chromadb
from sentence_transformers import SentenceTransformer
import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

# load the embedding model locally
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# create a local ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("memories")


def store_memory(role, content):
    embedding = embedder.encode(content).tolist()
    collection.add(
        documents=[content],
        embeddings=[embedding],
        metadatas=[{"role": role}],
        ids=[str(collection.count() + 1)]
    )


def search_memory(query, n_results=3):
    embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )

    if not results["documents"][0]:
        return ""

    formatted = ""
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        formatted += f"{meta['role']}: {doc}\n"

    return formatted