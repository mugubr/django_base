# JWT Authentication Guide / Guia de Autenticação JWT

## Overview / Visão Geral

This project uses **JSON Web Tokens (JWT)** for API authentication via
**djangorestframework-simplejwt**. Este projeto usa **JSON Web Tokens (JWT)**
para autenticação de API via **djangorestframework-simplejwt**.

JWT provides stateless authentication, where tokens are signed and verified
without server-side storage. JWT fornece autenticação stateless, onde tokens são
assinados e verificados sem armazenamento no servidor.

---

## Features / Recursos

- ✅ **Access & Refresh Tokens** / **Tokens de Acesso e Refresh**
- ✅ **Token Rotation** / **Rotação de Tokens**
- ✅ **Token Blacklisting** / **Blacklist de Tokens**
- ✅ **Configurable Expiration** / **Expiração Configurável**
- ✅ **Bearer Authentication** / **Autenticação Bearer**

---

## Configuration / Configuração

### Environment Variables / Variáveis de Ambiente

Add to your `.env` file: Adicione ao seu arquivo `.env`:

```env
# JWT Token Lifetimes / Tempo de Vida dos Tokens JWT
JWT_ACCESS_TOKEN_MINUTES=60        # Access token: 60 minutes / Token de acesso: 60 minutos
JWT_REFRESH_TOKEN_DAYS=7           # Refresh token: 7 days / Token de refresh: 7 dias
```

### Settings / Configurações

JWT settings are configured in `src/django_base/settings/base.py`: Configurações
JWT estão em `src/django_base/settings/base.py`:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

---

## API Endpoints / Endpoints da API

### 1. Obtain Token / Obter Token

**Endpoint:** `POST /api/token/`

**Description:** Authenticate and receive access + refresh tokens.
**Descrição:** Autentique e receba tokens de acesso + refresh.

**Request:**

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }'
```

**Response:**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Token Lifetimes / Tempo de Vida dos Tokens:**

- **Access Token:** 60 minutes (default) / 60 minutos (padrão)
- **Refresh Token:** 7 days (default) / 7 dias (padrão)

---

### 2. Refresh Token / Renovar Token

**Endpoint:** `POST /api/token/refresh/`

**Description:** Get a new access token using refresh token. **Descrição:**
Obtenha um novo token de acesso usando o token de refresh.

**Request:**

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Response:**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." // New refresh token if rotation enabled
}
```

**Note:** With `ROTATE_REFRESH_TOKENS=True`, you receive a new refresh token,
and the old one is blacklisted. **Nota:** Com `ROTATE_REFRESH_TOKENS=True`, você
recebe um novo token de refresh e o antigo é adicionado à blacklist.

---

### 3. Verify Token / Verificar Token

**Endpoint:** `POST /api/token/verify/`

**Description:** Check if a token is valid. **Descrição:** Verifique se um token
é válido.

**Request:**

```bash
curl -X POST http://localhost:8000/api/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Response:**

- **200 OK:** Token is valid / Token é válido
- **401 Unauthorized:** Token is invalid or expired / Token é inválido ou
  expirado

---

## Using JWT Tokens / Usando Tokens JWT

### Authorization Header / Header de Autorização

Include the access token in the `Authorization` header: Inclua o token de acesso
no header `Authorization`:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Example: Authenticated API Request / Exemplo: Requisição Autenticada

```bash
curl -X GET http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response:**

```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Product 1",
      "price": "99.99"
    }
  ]
}
```

---

## JavaScript/Frontend Example / Exemplo JavaScript/Frontend

### 1. Login and Store Tokens / Login e Armazenar Tokens

```javascript
// Login
async function login(username, password) {
  const response = await fetch("http://localhost:8000/api/token/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();

  // Store tokens in localStorage
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);

  return data;
}
```

### 2. Make Authenticated Requests / Fazer Requisições Autenticadas

```javascript
// Authenticated API call
async function fetchProducts() {
  const accessToken = localStorage.getItem("access_token");

  const response = await fetch("http://localhost:8000/api/v1/products/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });

  if (response.status === 401) {
    // Token expired, refresh it
    await refreshToken();
    return fetchProducts(); // Retry request
  }

  return await response.json();
}
```

### 3. Refresh Token / Renovar Token

```javascript
// Refresh access token
async function refreshToken() {
  const refreshToken = localStorage.getItem("refresh_token");

  const response = await fetch("http://localhost:8000/api/token/refresh/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ refresh: refreshToken }),
  });

  if (!response.ok) {
    // Refresh token is invalid/expired, logout user
    logout();
    throw new Error("Session expired");
  }

  const data = await response.json();

  // Update tokens
  localStorage.setItem("access_token", data.access);
  if (data.refresh) {
    localStorage.setItem("refresh_token", data.refresh);
  }

  return data;
}
```

### 4. Logout / Sair

```javascript
// Logout
function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  // Redirect to login page
  window.location.href = "/login";
}
```

---

## Python/Client Example / Exemplo Python/Cliente

```python
import requests

# Configuration
API_BASE_URL = "http://localhost:8000"

# 1. Obtain tokens
def login(username: str, password: str):
    response = requests.post(
        f"{API_BASE_URL}/api/token/",
        json={"username": username, "password": password}
    )
    response.raise_for_status()
    return response.json()

# 2. Make authenticated request
def get_products(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{API_BASE_URL}/api/v1/products/",
        headers=headers
    )
    response.raise_for_status()
    return response.json()

# 3. Refresh token
def refresh_access_token(refresh_token: str):
    response = requests.post(
        f"{API_BASE_URL}/api/token/refresh/",
        json={"refresh": refresh_token}
    )
    response.raise_for_status()
    return response.json()

# Usage
if __name__ == "__main__":
    # Login
    tokens = login("admin", "admin")
    access_token = tokens["access"]
    refresh_token = tokens["refresh"]

    # Get products
    products = get_products(access_token)
    print(products)

    # Refresh token when needed
    new_tokens = refresh_access_token(refresh_token)
    access_token = new_tokens["access"]
```

---

## Security Best Practices / Melhores Práticas de Segurança

### 1. Token Storage / Armazenamento de Tokens

**Frontend:**

- **❌ DO NOT** store tokens in `localStorage` for highly sensitive apps (XSS
  risk) / **NÃO** armazene tokens em `localStorage` para apps altamente
  sensíveis (risco XSS)
- **✅ PREFER** HTTP-only cookies for web apps / **PREFIRA** cookies HTTP-only
  para web apps
- **✅ USE** secure storage for mobile apps (Keychain, Keystore) / **USE**
  armazenamento seguro para apps mobile

**Backend:**

- **✅** Keep `SECRET_KEY` secret and unique / Mantenha `SECRET_KEY` secreta e
  única
- **✅** Use environment variables for sensitive config / Use variáveis de
  ambiente para config sensível
- **✅** Enable token blacklisting / Habilite blacklist de tokens

### 2. Token Lifetimes / Tempo de Vida dos Tokens

**Recommendations / Recomendações:**

- **Access Token:** 15-60 minutes / 15-60 minutos
- **Refresh Token:** 7-30 days / 7-30 dias

**Tradeoffs / Trade-offs:**

- **Shorter tokens:** More secure, more frequent refreshes / Mais seguro, mais
  renovações
- **Longer tokens:** Better UX, less secure / Melhor UX, menos seguro

### 3. HTTPS Only / Apenas HTTPS

**Always use HTTPS in production!** Tokens can be intercepted on HTTP. **Sempre
use HTTPS em produção!** Tokens podem ser interceptados em HTTP.

### 4. Token Rotation / Rotação de Tokens

**Enabled by default:**

- `ROTATE_REFRESH_TOKENS=True`: New refresh token on each refresh
- `BLACKLIST_AFTER_ROTATION=True`: Old tokens are invalidated

---

## Troubleshooting / Solução de Problemas

### Error: "Token is invalid or expired" / Erro: "Token is invalid or expired"

**Cause / Causa:**

- Token has expired / Token expirou
- Token signature is invalid / Assinatura do token é inválida
- `SECRET_KEY` changed / `SECRET_KEY` mudou

**Solution / Solução:**

1. Refresh the access token using `/api/token/refresh/`
2. If refresh token is also expired, login again with `/api/token/`

### Error: "Given token not valid for any token type" / Erro: "Given token not valid for any token type"

**Cause / Causa:**

- Using refresh token where access token is expected (or vice versa)
- Usando token de refresh onde token de acesso é esperado (ou vice versa)

**Solution / Solução:**

- Use the correct token for each endpoint:
  - `/api/token/refresh/` → Refresh token
  - API endpoints → Access token

### Error: "Token contained no recognizable user identification" / Erro: "Token contained no recognizable user identification"

**Cause / Causa:**

- User was deleted but token is still valid
- Usuário foi deletado mas token ainda é válido

**Solution / Solução:**

- Re-authenticate to get a new token

---

## Testing JWT / Testando JWT

### Manual Testing / Teste Manual

```bash
# 1. Get tokens
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Save the access token
export ACCESS_TOKEN="your-access-token-here"

# 2. Use token
curl -X GET http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 3. Refresh token
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your-refresh-token-here"}'
```

### Swagger UI Testing / Testando no Swagger UI

1. Go to `http://localhost:8000/api/docs/`
2. Click **"Authorize"** button (🔒)
3. Enter: `Bearer your-access-token-here`
4. Click **"Authorize"**
5. All API requests will now include the token

---

## Migration from Session Auth / Migração da Autenticação de Sessão

Both **JWT** and **Session Authentication** are enabled by default: Tanto
**JWT** quanto **Autenticação de Sessão** estão habilitados por padrão:

```python
"DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT
    "rest_framework.authentication.SessionAuthentication",        # Session
],
```

**Recommendation / Recomendação:**

- **JWT:** For mobile apps, SPAs, external API consumers / Para apps mobile,
  SPAs, consumidores externos da API
- **Session:** For Django templates, admin panel / Para templates Django, painel
  admin

---

## Resources / Recursos

- **DRF Simple JWT Docs:**
  https://django-rest-framework-simplejwt.readthedocs.io/
- **JWT.io Debugger:** https://jwt.io/
- **RFC 7519 (JWT Spec):** https://tools.ietf.org/html/rfc7519

---

## Questions? / Dúvidas?

For questions or issues, create an issue on GitHub: Para perguntas ou problemas,
crie uma issue no GitHub:

https://github.com/mugubr/django-base/issues
