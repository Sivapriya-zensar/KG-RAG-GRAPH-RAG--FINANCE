"""
rag_engine.py
-------------
Embeds synthetic financial documents using sentence-transformers
and indexes them in a FAISS flat (exact) index for top-k retrieval.
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from synthetic_data import DOCUMENTS

# ─────────────────────────────────────────────
# Model + Index Initialisation (runs once at import)
# ─────────────────────────────────────────────
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = SentenceTransformer(MODEL_NAME)

# Embed all documents
_doc_embeddings: np.ndarray = _model.encode(
    DOCUMENTS, convert_to_numpy=True, normalize_embeddings=True
)

# Build FAISS index (inner product on L2-normalised vectors = cosine similarity)
_dim = _doc_embeddings.shape[1]
_index = faiss.IndexFlatIP(_dim)
_index.add(_doc_embeddings.astype(np.float32))

print(f"[RAG] Indexed {len(DOCUMENTS)} documents | dim={_dim}")


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────

def embed_query(query: str) -> np.ndarray:
    """
    Embed a single query string and L2-normalise it.
    Returns shape (1, dim) float32 array.
    """
    vec = _model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    return vec.astype(np.float32)


def retrieve_top_k(query: str, k: int = 3) -> list[dict]:
    """
    Retrieve the top-k most similar documents for a given query.

    Returns:
        List of dicts: [{rank, score, text}, ...]
    """
    query_vec = embed_query(query)
    scores, indices = _index.search(query_vec, k)

    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0]), start=1):
        if idx < 0 or idx >= len(DOCUMENTS):
            continue
        results.append({
            "rank": rank,
            "score": float(score),
            "text": DOCUMENTS[idx],
        })
    return results


def get_docs_text(query: str, k: int = 5) -> str:
    """
    Retrieve high-confidence documents only. Filter out low-relevance results.
    This prevents generic/off-topic documents from overshadowing KG facts.
    """
    results = retrieve_top_k(query, k)
    # Only include documents with reasonable confidence
    filtered = [r for r in results if r['score'] > 0.35]
    if not filtered:
        return "(No relevant supplementary documents found)"
    # Return top 3 filtered results
    lines = [f"[Ref {r['rank']}] {r['text']}" for r in filtered[:3]]
    return "\n".join(lines)
