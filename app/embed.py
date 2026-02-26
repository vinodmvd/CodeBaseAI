from sentence_transformers import SentenceTransformer
import chromadb

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma = chromadb.Client()
collection = chroma.get_or_create_collection("codebase")

def embed_and_store(chunks):
    texts = [c["text"] for c in chunks]
    embeddings = embed_model.encode(texts).tolist()

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[str(i)],
            embeddings=[emb],
            documents=[chunk["text"]],
            metadatas=[{"file": chunk["file"]}]
        )

    print("Stored in vector DB")