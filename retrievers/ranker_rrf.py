from collections import defaultdict

def rrf(rank_lists, k=60):
    scores = defaultdict(float)

    for ranked in rank_lists:
        for rank, doc_id in enumerate(ranked):
            scores[doc_id] += 1 / (k + rank + 1)

    return sorted(scores, key=lambda d: scores[d], reverse=True)