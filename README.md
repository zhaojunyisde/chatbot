# FastAPI Microservice with JWT Authentication & Chat History

A production-ready FastAPI microservice with JWT authentication and chat history functionality, featuring a modular architecture for scalability and maintainability.

## Features

- **FastAPI framework** for high-performance API endpoints
- **JWT-based authentication** system with secure password hashing
- **Chat history functionality** with user-to-bot conversations
- **Rate limiting** to prevent abuse (100 req/min service-wide, 10 req/min per user)
- **Modular architecture** with separate auth and chat modules
- **In-memory storage** for users and chat history (easily replaceable with databases)
- **Docker and Docker Compose** support for containerization
- **CORS middleware** configured for cross-origin requests
- **Auto-generated API documentation** (Swagger UI & ReDoc)
- **Health check** endpoint for monitoring
- **User registration and login** with bcrypt password hashing

## Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.10+ (for local development)

## Quick Start with Docker

1. Clone or navigate to this repository

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Generate a secure secret key and update `.env`:
```bash
openssl rand -hex 32
```

4. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file and configure your secret key

4. Run the application:
```bash
python main.py
# OR
uvicorn main:app --reload
```

## Project Structure

```
chatbot/
├── main.py                    # FastAPI app initialization and router registration
├── auth/                      # Authentication module
│   ├── __init__.py
│   ├── models.py             # User, Token, UserCreate Pydantic models
│   ├── database.py           # In-memory user database
│   ├── utils.py              # Password hashing, JWT token utilities
│   ├── dependencies.py       # FastAPI authentication dependencies
│   └── routes.py             # Auth endpoints (/token, /register, etc.)
├── chat/                      # Chat functionality module
│   ├── __init__.py
│   ├── models.py             # Chat message Pydantic models
│   ├── database.py           # In-memory chat history storage
│   ├── utils.py              # Bot response generator, message utilities
│   └── routes.py             # Chat endpoints (/chat, /chat/history)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## API Endpoints

### Public Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /register` - Register a new user
- `POST /token` - Login and get access token

### Protected Endpoints (Require Authentication)

**Authentication:**
- `GET /users/me` - Get current user information
- `GET /protected` - Example protected route

**Chat:**
- `POST /chat` - Send a message to the chatbot and get a response (rate limited)
- `GET /chat/history` - Retrieve chat history (supports `?limit=N` parameter)
- `GET /chat/rate-limit` - Check current rate limit status
- `DELETE /chat/history` - Clear all chat history for the current user

## API Documentation

Once the application is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "email": "test@example.com",
    "full_name": "Test User"
  }'
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Access Protected Endpoint

```bash
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Send a Chat Message

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "hello"
  }'
```

Response:
```json
{
  "id": "f97f0f98-11a2-4056-9f80-2a97a361939c",
  "username": "testuser",
  "role": "bot",
  "content": "Hello! How can I help you today?",
  "timestamp": "2025-11-16T23:32:29.593340"
}
```

### 5. Get Chat History

```bash
# Get all chat history
curl -X GET "http://localhost:8000/chat/history" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get last 10 messages
curl -X GET "http://localhost:8000/chat/history?limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "messages": [
    {
      "id": "7b96c039-c80d-4a83-b40c-275fc476427e",
      "username": "testuser",
      "role": "user",
      "content": "hello",
      "timestamp": "2025-11-16T23:32:29.593325"
    },
    {
      "id": "f97f0f98-11a2-4056-9f80-2a97a361939c",
      "username": "testuser",
      "role": "bot",
      "content": "Hello! How can I help you today?",
      "timestamp": "2025-11-16T23:32:29.593340"
    }
  ],
  "total": 2
}
```

### 6. Clear Chat History

```bash
curl -X DELETE "http://localhost:8000/chat/history" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Check Rate Limit Status

```bash
curl -X GET "http://localhost:8000/chat/rate-limit" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "global": {
    "current": 5,
    "limit": 100,
    "remaining": 95,
    "window": "1 minute"
  },
  "user": {
    "current": 5,
    "limit": 10,
    "remaining": 5,
    "window": "1 minute"
  }
}
```

## Rate Limiting

The chat API implements dual-layer rate limiting to ensure fair usage and prevent abuse:

### Limits

- **Service-wide**: 100 requests per minute across all users
- **Per-user**: 10 requests per minute per user

### How It Works

- Rate limits are enforced on the `POST /chat` endpoint
- Limits use a sliding window of 1 minute
- When a limit is exceeded, you'll receive an HTTP 429 error
- Old requests are automatically cleaned up after the time window

### Rate Limit Response

When you exceed your rate limit:

```json
{
  "detail": {
    "error": "User rate limit exceeded",
    "message": "You have reached your limit of 10 requests per minute. Please try again later.",
    "retry_after": 60,
    "current_usage": 10,
    "limit": 10
  }
}
```

### Checking Your Usage

Use the `GET /chat/rate-limit` endpoint to check your current rate limit status at any time. This helps you monitor your usage and avoid hitting limits.

### Default Admin User

For testing, a default admin user is available:
- **Username**: `admin`
- **Password**: `admin123`

## Docker Commands

Build the image:
```bash
docker-compose build
```

Run in detached mode:
```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop the service:
```bash
docker-compose down
```

## Architecture & Design

### Modular Structure

The application follows a modular architecture with clear separation of concerns:

- **`auth/`**: Handles all authentication-related functionality
  - User models and database
  - Password hashing and JWT token management
  - Authentication dependencies for route protection

- **`chat/`**: Manages chat functionality
  - Chat message models and storage
  - Bot response generation (customizable)
  - Chat history management

- **`main.py`**: Minimal entry point that registers routes and configures the app

### Bot Response Customization

The bot response logic is located in `chat/utils.py` in the `generate_bot_response()` function. You can easily replace this with:
- LLM integration (OpenAI, Anthropic Claude, etc.)
- Rule-based chatbot logic
- Integration with existing chatbot services

## Security Notes

1. **Change the `SECRET_KEY` in production** - use a strong, random key generated with `openssl rand -hex 32`
2. **Update CORS settings** in `main.py` to restrict allowed origins (currently set to `["*"]`)
3. **Replace in-memory databases** with real databases (PostgreSQL, MySQL, MongoDB, etc.)
4. **Enable HTTPS** in production
5. **Implement advanced rate limiting** (e.g., different tiers, dynamic limits)
6. **Implement proper logging and monitoring**
7. **Use environment variables** for all sensitive configuration

## Next Steps

### Database Integration
- Replace `auth/database.py` with a real user database
- Replace `chat/database.py` with a real chat storage solution
- Consider PostgreSQL for relational data or MongoDB for document storage

### Enhanced Features
- Implement refresh tokens for better security
- Add role-based access control (RBAC)
- Add conversation sessions to group related chat messages
- Implement message search and filtering
- Add message reactions or ratings
- Support file uploads in chat

### Production Readiness
- Set up automated testing (pytest)
- Configure CI/CD pipeline
- Add comprehensive logging with structured logs
- Implement monitoring and alerting
- Enhance rate limiting (Redis-based distributed rate limiting for multi-instance deployments)
- Set up database migrations (Alembic)
- Configure production WSGI server (Gunicorn)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
