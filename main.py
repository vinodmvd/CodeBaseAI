from dotenv import load_dotenv
load_dotenv()

import os

from app.ingest import read_code_files
from retrievers.dense_embed import EmbeddingModel
from retrievers.vector_db import upsert_vector, dense_retrieve, log_query
from retrievers.sparse_search import build_sparse_from_chunks, bm25_query
from retrievers.ranker_rrf import rrf
from app.chat import ask


def main():

    embed_model = EmbeddingModel()
    repo_path = input("Enter path to codebase: ").strip()
    repo_path = os.path.abspath(repo_path)

    print("\nIndexing repository...")
    chunks = read_code_files(repo_path)
    print(f"Total chunks: {len(chunks)}")

    #Dense Vector
    embeddings = embed_model.embedding_text(chunks)
    upsert_vector(chunks, embeddings)
    
    #Sparse Vector
    build_sparse_from_chunks(chunks)
    
    print("Indexing complete.\n")

    print("You can now ask questions about the codebase.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("> ")
        if question.lower() == "exit":
            break
        
        top_k = 5
        #dense search
        embeddings_retrieve = embed_model.embedding_text(question)
        dimensions = len(embeddings_retrieve)
        dense_docs, best_distance = dense_retrieve(embeddings_retrieve, k=5)
        
        #distance score check
        metadata = [value["meta"] for value in dense_docs]
        log_query(question, best_distance, metadata, dimensions)
        
        #sparse search
        sparse_docs = bm25_query(question, k=15)
                
        # Convert to ranked id lists
        dense_ranked = [doc["doc_id"] for doc in dense_docs]
        sparse_ranked = [doc["doc_id"] for doc in sparse_docs]

        # RRF Fusion
        fused_ids = rrf([dense_ranked, sparse_ranked])
        top_ids = fused_ids[:top_k]

        # Retrieve final documents
        doc_lookup = {doc["doc_id"]: doc for doc in dense_docs + sparse_docs}
        final_docs = [doc_lookup[id_] for id_ in fused_ids if id_ in doc_lookup]
        
        ask(question, final_docs)


if __name__ == "__main__":
    main()