from sentence_transformers import SentenceTransformer
import chromadb

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma = chromadb.Client()
collection = chroma.get_or_create_collection("codebase")

def retrieve(query, k=5):
    emb = embed_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=emb,
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    print("\n[DEBUG] Retrieved files:")
    for m in metas:
        print(m["file"])

    context = ""
    for d, m in zip(docs, metas):
        context += f"\nFILE: {m['file']}\nCODE:\n{d}\n"

    return context