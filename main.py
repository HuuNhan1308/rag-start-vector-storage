from fastapi import FastAPI
import numpy as np
import faiss

app = FastAPI()

DIMENSION = 3072  # Gemini embedding
index = faiss.IndexFlatL2(DIMENSION)
documents = []

@app.post("/add_vector")
def add_vector(payload: dict):
    clear();

    vector = np.array(payload["vectors"]).astype("float32")
    texts = payload["texts"]

    index.add(vector)
    documents.extend(texts)
    return {"status": "added", "count": len(texts)}


@app.post("/search")
def search_vector(payload: dict):
    query_vector = np.array([payload["vector"]]).astype("float32")
    k = payload.get("k", 5)

    distances, indices = index.search(query_vector, k)
    results = [documents[i] for i in indices[0]]

    return {"results": results, "distances": distances.tolist(), "indices": indices.tolist()}

@app.get("/debug")
def debug():
    return {
        "total_vectors_in_index": index.ntotal,
        "total_documents": len(documents),
        "dimension": DIMENSION
    }

@app.post("/clear")
def clear():
    index.reset()
    documents.clear()
    return {"status": "cleared"}

