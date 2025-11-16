# FastAPI Microservice with JWT Authentication

A production-ready FastAPI microservice with JWT authentication, containerized with Docker.

## Features

- FastAPI framework for high-performance API endpoints
- JWT-based authentication system
- Password hashing with bcrypt
- Docker and Docker Compose support
- CORS middleware configured
- Auto-generated API documentation (Swagger UI)
- Health check endpoint
- User registration and login

## Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+ (for local development)

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
uvicorn main:app --reload
```

## API Endpoints

### Public Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /register` - Register a new user
- `POST /token` - Login and get access token

### Protected Endpoints (Require Authentication)

- `GET /users/me` - Get current user information
- `GET /protected` - Example protected route

## API Documentation

Once the application is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage Examples

### Register a New User

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

### Login and Get Token

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

### Access Protected Endpoint

```bash
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Default Admin User

For testing, a default admin user is available:
- Username: `admin`
- Password: `admin123`

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

## Project Structure

```
.
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Security Notes

1. Change the `SECRET_KEY` in production - use a strong, random key
2. Update CORS settings in `main.py` to restrict allowed origins
3. In production, replace the fake database with a real database (PostgreSQL, MySQL, MongoDB, etc.)
4. Enable HTTPS in production
5. Consider adding rate limiting
6. Implement proper logging and monitoring

## Next Steps

- Add a real database (PostgreSQL, MongoDB, etc.)
- Implement refresh tokens
- Add role-based access control (RBAC)
- Set up automated testing
- Add more API endpoints for your use case
- Configure CI/CD pipeline
- Set up logging and monitoring

## License

MIT
