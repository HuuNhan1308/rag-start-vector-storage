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

# Security - API Key Authentication (IMPORTANT!)
API_KEY=your-secret-api-key-change-this-in-production

# CORS (Optional - comma separated origins)
# ALLOWED_ORIGINS=https://your-express-app.com,https://your-frontend.com
```

## Railway Deployment

**⚠️ IMPORTANT: Set API_KEY for security!**

Required variables:
- `API_KEY` - Your secret API key to protect endpoints

Optional variables:
- `PORT` - Railway sets this automatically
- `PYTHON_ENV` - Defaults to `production`
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins for CORS

## Environment Variables Explained

- `PORT`: Port to run the service (default: 8000)
- `HOST`: Host to bind to (default: 0.0.0.0)
- `DIMENSION`: Vector dimension for embeddings (3072 for Gemini)
- `LOG_LEVEL`: Logging level (info, debug, warning, error)
- `API_KEY`: Secret key to authenticate requests (default: "your-secret-api-key-change-this")
- `ALLOWED_ORIGINS`: CORS allowed origins, comma-separated (default: "*")