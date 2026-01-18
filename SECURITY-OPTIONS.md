# 🔐 Security Options - Chỉ cho phép các URL cụ thể

## 🎯 Giải Pháp Đã Implement: API Key Authentication

### ✅ Hiện Tại: API Key (RECOMMENDED)

**Đã được implement trong `main.py`**

```python
# Trong main.py
API_KEY = os.getenv("API_KEY", "your-secret-api-key-change-this")

# Tất cả endpoints đều yêu cầu header:
# X-API-Key: your-secret-api-key
```

**Ưu điểm:**
- ✅ Đơn giản, dễ implement
- ✅ Hoàn hảo cho server-to-server communication
- ✅ Không cần database
- ✅ Performance cao

**Nhược điểm:**
- ⚠️ Nếu API key bị leak, cần rotate ngay
- ⚠️ Không phân quyền chi tiết (tất cả hoặc không)

**Cách sử dụng từ Express:**

```javascript
fetch('https://your-vector-storage.railway.app/search', {
  method: 'POST',
  headers: {
    'X-API-Key': process.env.VECTOR_STORAGE_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ vector: [...], k: 5 })
});
```

---

## 🔒 Các Giải Pháp Bảo Mật Khác (Nếu cần nâng cao)

### 1. IP Whitelist

Chỉ cho phép requests từ IP cụ thể:

```python
# main.py
from fastapi import Request

ALLOWED_IPS = os.getenv("ALLOWED_IPS", "127.0.0.1").split(",")

@app.middleware("http")
async def verify_ip(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="IP not allowed")
    return await call_next(request)
```

**Ưu điểm:**
- ✅ Rất an toàn
- ✅ Không cần gửi credentials

**Nhược điểm:**
- ❌ Khó quản lý với dynamic IPs
- ❌ Không work với Railway (IP thay đổi)
- ❌ Phức tạp khi có nhiều servers

**Khi nào dùng:** VPS/dedicated servers với static IPs

---

### 2. JWT Token

Token-based authentication với expiration:

```python
# pip install pyjwt

import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET", "your-jwt-secret")

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Ưu điểm:**
- ✅ Tokens có thời gian expire
- ✅ Có thể chứa metadata (user_id, permissions)
- ✅ Stateless

**Nhược điểm:**
- ❌ Phức tạp hơn API key
- ❌ Cần refresh token mechanism
- ❌ Overkill cho server-to-server

**Khi nào dùng:** Multi-tenant, cần phân quyền chi tiết

---

### 3. OAuth2 / API Gateway

Dùng service như Kong, AWS API Gateway:

```
Client → API Gateway (Auth) → FastAPI Service
```

**Ưu điểm:**
- ✅ Enterprise-grade security
- ✅ Rate limiting, monitoring built-in
- ✅ Centralized authentication

**Nhược điểm:**
- ❌ Rất phức tạp
- ❌ Tốn chi phí
- ❌ Overkill cho small projects

**Khi nào dùng:** Large-scale production systems

---

### 4. Mutual TLS (mTLS)

Client và server đều verify certificates:

```python
# Trong Dockerfile/deployment
# Cần SSL certificates cho cả client và server
```

**Ưu điểm:**
- ✅ Bảo mật cao nhất
- ✅ Không cần gửi credentials trong request

**Nhược điểm:**
- ❌ Rất phức tạp setup
- ❌ Certificate management overhead
- ❌ Không phù hợp với serverless

**Khi nào dùng:** Banking, government systems

---

### 5. HMAC Signature

Sign requests với shared secret:

```python
import hmac
import hashlib

def verify_signature(request: Request):
    signature = request.headers.get("X-Signature")
    payload = await request.body()
    
    expected = hmac.new(
        SECRET_KEY.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=403, detail="Invalid signature")
```

**Express client:**

```javascript
const crypto = require('crypto');

const payload = JSON.stringify({ vector: [...] });
const signature = crypto
  .createHmac('sha256', SECRET_KEY)
  .update(payload)
  .digest('hex');

fetch(url, {
  method: 'POST',
  headers: {
    'X-Signature': signature,
    'Content-Type': 'application/json'
  },
  body: payload
});
```

**Ưu điểm:**
- ✅ Request tampering protection
- ✅ Không gửi secret qua network
- ✅ An toàn hơn simple API key

**Nhược điểm:**
- ❌ Phức tạp hơn
- ❌ Cần đồng bộ clocks
- ❌ Replay attack nếu không có nonce/timestamp

**Khi nào dùng:** Financial transactions, webhooks

---

## 🎯 Recommendation cho Project của Bạn

### Current Setup (API Key) là Đủ Tốt Vì:

1. ✅ **Server-to-Server**: Không có browser involvement
2. ✅ **Private Network**: Express và FastAPI có thể ở private network
3. ✅ **Simple & Fast**: Không overhead
4. ✅ **Easy to Rotate**: Chỉ cần update env var

### 🔄 Nâng Cấp Đề Nghị (Nếu Cần):

**Level 1 (Current):** API Key
- ✅ Deploy ngay được
- ✅ Đủ tốt cho production

**Level 2 (Better):** API Key + HTTPS + CORS restrictions
- Set `allow_origins` trong CORS
- Chỉ cho phép domain của Express server
- Bắt buộc HTTPS trong production

**Level 3 (Best):** API Key + IP Whitelist (nếu có static IP)
- Thêm IP whitelist middleware
- Chỉ accept requests từ Express server IP

**Level 4 (Overkill):** JWT/OAuth2
- Chỉ cần nếu có nhiều clients
- Hoặc cần phân quyền chi tiết

---

## 🚀 Quick Setup cho Level 2 (Recommended)

### 1. Update CORS trong `main.py`:

```python
# Thay vì allow_origins=["*"]
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type", "X-API-Key"],
)
```

### 2. Set Environment Variables on Railway:

```env
API_KEY=dKj8sL2mN9pQ4rT7vX1zC6bH3fY5wE0u  # Random strong key
ALLOWED_ORIGINS=https://your-express-app.com,https://your-express-app.railway.app
```

### 3. Generate Strong API Key:

```bash
# Linux/Mac
openssl rand -hex 32

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## ⚠️ Security Checklist

- [ ] Set strong API_KEY (not default)
- [ ] Limit CORS origins (not `*`)
- [ ] Use HTTPS in production
- [ ] Store API keys in `.env`, not code
- [ ] Add `.env` to `.gitignore`
- [ ] Rotate API keys periodically (every 90 days)
- [ ] Monitor failed auth attempts
- [ ] Add rate limiting (optional)
- [ ] Set up logging for security events

---

## 📊 Comparison Table

| Method | Complexity | Security | Performance | Server-to-Server | Cost |
|--------|-----------|----------|-------------|------------------|------|
| **API Key (Current)** | ⭐ Low | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ✅ Perfect | Free |
| IP Whitelist | ⭐⭐ Medium | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐⭐⭐ Excellent | ✅ Perfect | Free |
| JWT | ⭐⭐⭐ High | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐⭐ Good | ⚠️ OK | Free |
| HMAC Signature | ⭐⭐⭐ High | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Medium | ✅ Perfect | Free |
| OAuth2/Gateway | ⭐⭐⭐⭐⭐ Very High | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Medium | ✅ Perfect | $$$ |
| mTLS | ⭐⭐⭐⭐⭐ Very High | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good | ✅ Perfect | $$ |

---

## 🎓 Kết Luận

**Cho use case của bạn (Express → FastAPI):**

🏆 **API Key (đã implement) là lựa chọn tốt nhất!**

- Đơn giản
- An toàn đủ
- Performance cao
- Dễ maintain

**Next steps:**
1. ✅ Generate strong API key
2. ✅ Set trên Railway/Docker
3. ✅ Update Express code với API key
4. ✅ Test endpoints
5. ✅ Deploy!

Tham khảo `INTEGRATION-GUIDE.md` để xem cách integrate với Express server.
