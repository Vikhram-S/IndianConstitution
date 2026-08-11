"""Semantic Search — IndianConstitution Library.

Uses sentence-transformers embeddings for contextual retrieval
beyond keyword matching.

Requires: pip install "indianconstitution[ai]"
"""

from indianconstitution import get_constitution

ic = get_constitution()

# ─────────────────────────────────────────────────────────────────────────
# Contextual / semantic search
# ─────────────────────────────────────────────────────────────────────────
queries = [
    "protection against arbitrary state action",
    "children's education rights",
    "freedom of speech and media",
]

for query in queries:
    print(f"\n{'-' * 60}")
    print(f"Query: {query}")
    print(f"{'-' * 60}")

    try:
        results = ic.semantic_search(query, top_k=5)
        for r in results:
            print(f"  [{r.number}] {r.title}  (score: {r.score:.4f})")
    except ImportError as e:
        print(f"  [Notice] {e}")
