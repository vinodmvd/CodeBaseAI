import pickle
import re
from pathlib import Path
import hashlib

from rank_bm25 import BM25Okapi

file_dir = Path(__file__).resolve().parents[1]/"data"

STOPWORDS = {
    "what","is","the","for","a","an","of","to","and","in","on","with",
    "be","are","was","were","this","that"
}

def tokenize(text: str):
    words = re.findall(r"\b\w+\b", text.lower())
    return [w for w in words if w not in STOPWORDS]

def make_id(text, file_path):
    raw = file_path + text
    return hashlib.md5(raw.encode()).hexdigest()

def build_sparse_from_chunks(chunks):
    structured_dict = {}
    tokenized_data = []

    for chunk in chunks:
        text = chunk["text"]
        file_path = chunk["file"]

        doc_id = make_id(text, file_path)

        structured_dict[doc_id] = {
            "text": text,
            "file": file_path
        }

        tokenized_data.append(tokenize(text))

    bm25 = BM25Okapi(tokenized_data)

    with open(file_dir / "bm25.pkl", "wb") as f:
        pickle.dump((bm25, structured_dict), f)

    print("Sparse vector stored")


def bm25_query(query, k=5):
    with open(file_dir / "bm25.pkl", "rb") as f:
        bm25, structured_dict = pickle.load(f)

    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    sorted_scores = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )[:k]

    doc_ids = list(structured_dict.keys())

    results = []
    for idx, score in sorted_scores:
        doc_id = doc_ids[idx]

        results.append({
            "doc_id": doc_id,
            "score": score,
            "text": structured_dict[doc_id]["text"],
            "meta": structured_dict[doc_id]
        })

    return results