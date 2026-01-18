# 🔌 Integration Guide - How to Call from Express Server

## 📋 Prerequisites

1. Deploy FastAPI vector storage service (Railway/Docker)
2. Set `API_KEY` environment variable
3. Get the service URL

## 🚀 Express Server Integration

### 1. Using Fetch (Node.js 18+)

```javascript
// config.js
export const VECTOR_STORAGE_URL = process.env.VECTOR_STORAGE_URL || 'http://localhost:8000';
export const VECTOR_STORAGE_API_KEY = process.env.VECTOR_STORAGE_API_KEY;

// vectorService.js
async function addVectors(vectors, texts) {
  const response = await fetch(`${VECTOR_STORAGE_URL}/add_vector`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': VECTOR_STORAGE_API_KEY
    },
    body: JSON.stringify({ vectors, texts })
  });
  
  if (!response.ok) {
    throw new Error(`Failed to add vectors: ${response.status}`);
  }
  
  return await response.json();
}

async function searchVector(vector, k = 5) {
  const response = await fetch(`${VECTOR_STORAGE_URL}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': VECTOR_STORAGE_API_KEY
    },
    body: JSON.stringify({ vector, k })
  });
  
  if (!response.ok) {
    throw new Error(`Failed to search: ${response.status}`);
  }
  
  return await response.json();
}

async function clearVectors() {
  const response = await fetch(`${VECTOR_STORAGE_URL}/clear`, {
    method: 'POST',
    headers: {
      'X-API-Key': VECTOR_STORAGE_API_KEY
    }
  });
  
  return await response.json();
}

export { addVectors, searchVector, clearVectors };
```

### 2. Using Axios

```javascript
import axios from 'axios';

const vectorClient = axios.create({
  baseURL: process.env.VECTOR_STORAGE_URL || 'http://localhost:8000',
  headers: {
    'X-API-Key': process.env.VECTOR_STORAGE_API_KEY
  }
});

// Add vectors
async function addVectors(vectors, texts) {
  const { data } = await vectorClient.post('/add_vector', { vectors, texts });
  return data;
}

// Search
async function searchVector(vector, k = 5) {
  const { data } = await vectorClient.post('/search', { vector, k });
  return data;
}

// Clear
async function clearVectors() {
  const { data } = await vectorClient.post('/clear');
  return data;
}

export { addVectors, searchVector, clearVectors };
```

### 3. Usage Example in Express Route

```javascript
import express from 'express';
import { addVectors, searchVector } from './vectorService.js';

const app = express();
app.use(express.json());

// Endpoint để nhận query từ user và search vector
app.post('/api/rag/search', async (req, res) => {
  try {
    const { query, embedding } = req.body;
    
    // embedding là vector từ Gemini/OpenAI
    const results = await searchVector(embedding, 5);
    
    res.json({
      success: true,
      query,
      results: results.results,
      distances: results.distances
    });
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// Endpoint để add documents
app.post('/api/rag/add-documents', async (req, res) => {
  try {
    const { embeddings, texts } = req.body;
    
    const result = await addVectors(embeddings, texts);
    
    res.json({
      success: true,
      message: `Added ${result.count} documents`
    });
  } catch (error) {
    console.error('Add error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

app.listen(3000, () => {
  console.log('Express server running on port 3000');
});
```

## 🔐 Environment Variables for Express

Create `.env` file in your Express project:

```env
# Vector Storage Service
VECTOR_STORAGE_URL=https://your-vector-storage.railway.app
VECTOR_STORAGE_API_KEY=your-super-secret-api-key-here

# Must match the API_KEY set in FastAPI service
```

## 🧪 Testing

```javascript
// test.js
import { addVectors, searchVector } from './vectorService.js';

// Test add vectors
const testVectors = [
  Array(3072).fill(0.1),
  Array(3072).fill(0.2)
];
const testTexts = ['Document 1', 'Document 2'];

await addVectors(testVectors, testTexts);
console.log('✅ Vectors added');

// Test search
const queryVector = Array(3072).fill(0.15);
const results = await searchVector(queryVector, 2);
console.log('✅ Search results:', results);
```

## 🛡️ Security Best Practices

1. **Never commit API keys to Git**
   - Use `.env` files
   - Add `.env` to `.gitignore`

2. **Rotate API keys periodically**
   ```bash
   # Generate strong API key
   openssl rand -hex 32
   ```

3. **Use different keys for dev/staging/production**

4. **Monitor API usage**
   - Add logging in Express
   - Track failed authentication attempts

## ⚠️ Error Handling

```javascript
async function safeSearchVector(vector, k = 5) {
  try {
    return await searchVector(vector, k);
  } catch (error) {
    if (error.response?.status === 403) {
      console.error('❌ Invalid API Key!');
      throw new Error('Authentication failed');
    }
    if (error.response?.status === 500) {
      console.error('❌ Vector service error');
      throw new Error('Service unavailable');
    }
    throw error;
  }
}
```

## 🎯 Complete Flow Example

```javascript
// RAG Flow: User Query → Embedding → Vector Search → Context → LLM

import { GoogleGenerativeAI } from '@google/generative-ai';
import { searchVector } from './vectorService.js';

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

async function ragQuery(userQuery) {
  // 1. Generate embedding for user query
  const embeddingModel = genAI.getGenerativeModel({ 
    model: 'text-embedding-004' 
  });
  const result = await embeddingModel.embedContent(userQuery);
  const queryEmbedding = result.embedding.values;
  
  // 2. Search similar vectors
  const searchResults = await searchVector(queryEmbedding, 3);
  const context = searchResults.results.join('\n\n');
  
  // 3. Generate answer with LLM
  const chatModel = genAI.getGenerativeModel({ 
    model: 'gemini-2.0-flash-exp' 
  });
  const prompt = `Context:\n${context}\n\nQuestion: ${userQuery}\n\nAnswer:`;
  const answer = await chatModel.generateContent(prompt);
  
  return {
    answer: answer.response.text(),
    sources: searchResults.results,
    distances: searchResults.distances
  };
}

// Usage
const response = await ragQuery('What is FAISS?');
console.log(response.answer);
```

## 🔗 Resources

- FastAPI Docs: Your Vector Storage URL + `/docs`
- Express.js: https://expressjs.com
- Axios: https://axios-http.com
