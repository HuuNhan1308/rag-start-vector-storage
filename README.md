# 🐍 Vector Storage Service

FastAPI service for vector storage and similarity search using FAISS.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8000
```

Visit: http://localhost:8000/docs for API documentation

## 📦 API Endpoints

### POST /add_vector
Add vectors to the index
```json
{
  "vectors": [[0.1, 0.2, ...], [0.3, 0.4, ...]],
  "texts": ["text 1", "text 2"]
}
```

### POST /search
Search for similar vectors
```json
{
  "vector": [0.1, 0.2, ...],
  "k": 5
}
```

### GET /debug
Get index information

### POST /clear
Clear all vectors

## 🐳 Docker

```bash
# Build
docker build -t vector-storage .

# Run
docker run -p 8000:8000 vector-storage
```

## 🌐 Deploy to Railway

1. Push this repo to GitHub
2. Create new project on Railway.app
3. Connect GitHub repo
4. Railway auto-detects Dockerfile and deploys!

## 📝 Environment Variables

See `.env.example` for all available variables.

For Railway, no env vars are required (uses defaults).

## 🔧 Tech Stack

- Python 3.11
- FastAPI
- FAISS (Facebook AI Similarity Search)
- NumPy
- Uvicorn

## 📄 License

MIT
