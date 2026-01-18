# 🔧 Environment Variables Setup

## Local Development

Create a `.env` file in this directory with:

```env
# Server Configuration
PORT=8000
HOST=0.0.0.0

# Python Configuration
PYTHON_ENV=production

# FAISS Configuration
DIMENSION=3072

# Logging
LOG_LEVEL=info
```

## Railway Deployment

**No environment variables required!**

Railway will use default values from the code.

Optional variables you can add:
- `PORT` - Railway sets this automatically
- `PYTHON_ENV` - Defaults to `production`

## Environment Variables Explained

- `PORT`: Port to run the service (default: 8000)
- `HOST`: Host to bind to (default: 0.0.0.0)
- `DIMENSION`: Vector dimension for embeddings (3072 for Gemini)
- `LOG_LEVEL`: Logging level (info, debug, warning, error)
