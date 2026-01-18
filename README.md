# 🐍 Vector Storage Service

FastAPI service for vector storage and similarity search using FAISS.

## 📚 Documentation

- **[Integration Guide](INTEGRATION-GUIDE.md)** - How to call from Express/Node.js
- **[Security Options](SECURITY-OPTIONS.md)** - All security methods explained
- **[Environment Setup](ENV-SETUP.md)** - Environment variables configuration

## 🚀 Quick Start

### Local Development

```bash
# 1. Generate API Key (recommended)
python generate-api-key.py
# or: node generate-api-key.js

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server
uvicorn main:app --reload --port 8000
```

Visit: http://localhost:8000/docs for API documentation

**⚠️ Important:** All endpoints (except `/`) require API Key in `X-API-Key` header!

## 📦 API Endpoints

**⚠️ All endpoints (except `/`) require API Key in header:**

```bash
X-API-Key: your-secret-api-key
```

### GET /
Health check (no API key required)

### POST /add_vector
Add vectors to the index
```bash
curl -X POST http://localhost:8000/add_vector \
  -H "X-API-Key: your-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": [[0.1, 0.2, ...], [0.3, 0.4, ...]],
    "texts": ["text 1", "text 2"]
  }'
```

### POST /search
Search for similar vectors
```bash
curl -X POST http://localhost:8000/search \
  -H "X-API-Key: your-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, ...],
    "k": 5
  }'
```

### GET /debug
Get index information
```bash
curl http://localhost:8000/debug \
  -H "X-API-Key: your-secret-api-key"
```

### POST /clear
Clear all vectors
```bash
curl -X POST http://localhost:8000/clear \
  -H "X-API-Key: your-secret-api-key"
```

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

See `ENV-SETUP.md` for all available variables.

**⚠️ IMPORTANT for Production:**
```bash
API_KEY=your-super-secret-key-here
```

For Railway, set this in environment variables section.

## 🔧 Tech Stack

- Python 3.11
- FastAPI
- FAISS (Facebook AI Similarity Search)
- NumPy
- Uvicorn

## 📄 License

MIT
