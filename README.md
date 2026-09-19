# GateFlow — Lightweight API Gateway & Rate Limiter

GateFlow is a lightweight API gateway built with FastAPI and PostgreSQL. It authenticates clients using API keys, applies per-client rate limiting, routes requests to downstream services, and records request activity for monitoring and debugging.

## Features

- API key generation and authentication
- SHA-256 hashing of API keys before database storage
- Configurable request routing
- HTTP proxying to downstream services using HTTPX
- Per-client token-bucket rate limiting
- Rate-limit response headers
- PostgreSQL-backed request logging
- Handles common gateway responses:
  - `200 OK`
  - `404 Not Found`
  - `429 Too Many Requests`
  - `502 Bad Gateway`
- Health-check endpoint
- Automated tests using pytest

## Architecture

```text
                    ┌─────────────────────┐
                    │       Client        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      GateFlow       │
                    │    API Gateway      │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
          API Key Auth    Rate Limiter   Route Resolver
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Downstream APIs    │
                    │                     │
                    │  User Service       │
                    │  Order Service      │
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │                     │
                    │  API Keys           │
                    │  Request Logs       │
                    └─────────────────────┘
```

## Tech Stack

- **Python 3.10**
- **FastAPI**
- **Uvicorn**
- **PostgreSQL**
- **SQLAlchemy**
- **psycopg**
- **HTTPX**
- **pytest**

## Project Structure

```text
GateFlow/
│
├── app/
│   ├── config.py
│   ├── database.py
│   ├── gateway.py
│   ├── main.py
│   ├── models.py
│   ├── rate_limiter.py
│   ├── routes.py
│   └── security.py
│
├── create_tables.py
├── downstream.py
├── requirements.txt
├── test_auth.py
├── test_gateway.py
├── test_logging.py
├── test_rate_limiter.py
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Gateway health check |
| POST | `/api-keys` | Generate a new API key |
| GET | `/protected` | Test API-key authentication |
| GET | `/api/{service}` | Route request to a downstream service |

### Example Routes

```text
/api/users  →  http://127.0.0.1:9001/users
/api/orders →  http://127.0.0.1:9001/orders
```

## Rate Limiting

GateFlow uses a token-bucket algorithm for rate limiting.

Default configuration:

```text
Capacity: 5 requests
Refill rate: 0.5 tokens/second
```

Rate limiting is applied per API key.

When the limit is exceeded, GateFlow returns:

```text
429 Too Many Requests
```

along with rate-limit headers such as:

```text
X-RateLimit-Limit
X-RateLimit-Remaining
Retry-After
```

## Error Handling

GateFlow handles common request failures at the gateway level.

### Route not found

```text
404 Not Found
```

### Rate limit exceeded

```text
429 Too Many Requests
```

### Downstream service unavailable

```text
502 Bad Gateway
```

This prevents an unavailable downstream service from producing an unhandled application error in the gateway.

## Request Logging

GateFlow records request information in PostgreSQL, including:

- API key ID
- HTTP method
- Request path
- Status code
- Response time
- Timestamp

This provides a basic audit trail for gateway requests.

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd GateFlow
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scriptsctivate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Create a PostgreSQL database named:

```text
gateflow
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/gateflow
```

### 5. Create database tables

```bash
python create_tables.py
```

### 6. Start the downstream service

```bash
uvicorn downstream:app --port 9001 --reload
```

### 7. Start GateFlow

In another terminal:

```bash
uvicorn app.main:app --reload
```

The gateway will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run the complete automated test suite:

```bash
pytest
```

Current test suite:

```text
10 tests passed
```

## Security Notes

- Plaintext API keys are not stored in PostgreSQL.
- API keys are hashed using SHA-256 before database storage.
- Database credentials are loaded through environment variables.
- `.env` is excluded from version control.

## Future Improvements

Possible future improvements include:

- Redis-backed distributed rate limiting
- Async HTTP requests
- More configurable routing
- Authentication and authorization improvements
- Metrics and observability
- Containerized deployment
- Distributed gateway deployment

## Status

**Version 1.0 — Completed**

GateFlow currently provides API-key authentication, request routing, per-client rate limiting, downstream proxying, error handling, and PostgreSQL request logging with automated tests.
