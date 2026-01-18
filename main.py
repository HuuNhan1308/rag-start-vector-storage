from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import faiss
import os

app = FastAPI()

# CORS Configuration (Optional - chỉ cần nếu có browser gọi trực tiếp)
# Nếu chỉ có Express server gọi thì không cần, nhưng thêm vào cho an toàn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production, nên chỉ định cụ thể domain của Express server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Authentication
API_KEY = os.getenv("API_KEY", "your-secret-api-key-change-this")  # Đổi trong production!
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key từ header"""
    if api_key is None or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key"
        )
    return api_key

DIMENSION = 3072  # Gemini embedding
index = faiss.IndexFlatL2(DIMENSION)
documents = []

@app.get("/")
def root():
    """Health check endpoint - không cần API key"""
    return {"status": "ok", "service": "FAISS Vector Storage"}

@app.post("/add_vector")
def add_vector(payload: dict, api_key: str = Security(verify_api_key)):
    clear();

    vector = np.array(payload["vectors"]).astype("float32")
    texts = payload["texts"]

    index.add(vector)
    documents.extend(texts)
    return {"status": "added", "count": len(texts)}


@app.post("/search")
def search_vector(payload: dict, api_key: str = Security(verify_api_key)):
    query_vector = np.array([payload["vector"]]).astype("float32")
    k = payload.get("k", 5)

    distances, indices = index.search(query_vector, k)
    results = [documents[i] for i in indices[0]]

    return {"results": results, "distances": distances.tolist(), "indices": indices.tolist()}

@app.get("/debug")
def debug(api_key: str = Security(verify_api_key)):
    return {
        "total_vectors_in_index": index.ntotal,
        "total_documents": len(documents),
        "dimension": DIMENSION
    }

@app.post("/clear")
def clear(api_key: str = Security(verify_api_key)):
    index.reset()
    documents.clear()
    return {"status": "cleared"}

