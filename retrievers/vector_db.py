import os
import json
from datetime import datetime
import hashlib

from services.chroma_client import collection
from sentence_transformers import SentenceTransformer
from services.chroma_client import collection

def make_id(text, file_path):
    raw = file_path + text
    return hashlib.md5(raw.encode()).hexdigest()

def upsert_vector(chunks, embeddings):
    total_docs_before = collection.count()

    for chunk, emb in zip(chunks, embeddings):
        
        doc_id = make_id(chunk["text"], chunk["file"])
        collection.upsert(
            ids=[doc_id],
            embeddings=[emb],
            documents=[chunk["text"]],
            metadatas=[{"file": chunk["file"]}]
        )
    total_docs_after = collection.count()
    print(total_docs_before, total_docs_after)

    print("Stored in vector DB")


def dense_retrieve(query_embedding, k=5):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    best_distance = min(distances)

    dense_docs = []

    for doc_id, doc, meta, dist in zip(ids, docs, metas, distances):
        dense_docs.append({
            "doc_id": doc_id,
            "text": doc,
            "meta": meta,
            "distance": dist
        })

    return dense_docs, best_distance


def log_query(question, best_distance, metas, dimensions):
    log = {
        "question": question,
        "best_distance": float(best_distance),
        "files": [m["file"] for m in metas],
        "dimensions": dimensions,
        "time": str(datetime.now())
    }

    os.makedirs("evaluation", exist_ok=True)
    
    with open(os.path.join("evaluation", "logs.jsonl"), "a") as f:
        f.write(json.dumps(log) + "\n")