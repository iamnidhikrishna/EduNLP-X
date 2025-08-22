# EduNLP-X API Documentation

## Overview

The EduNLP-X API is built with FastAPI and provides comprehensive endpoints for managing users, content, AI-powered chat, quizzes, and analytics. All endpoints follow REST conventions and return JSON responses.

## Base URL

```
Development: http://localhost:8001/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Token Endpoints

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "phone_number": "+1234567890"
}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### POST /auth/login
Authenticate user and get access tokens.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "role": "student"
  }
}
```

#### POST /auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "access_token": "new_access_token",
  "refresh_token": "new_refresh_token",
  "token_type": "bearer"
}
```

#### GET /auth/me
Get current user information.

**Headers:**
```http
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "profile": {
    "learning_level": "intermediate",
    "preferred_subjects": ["python", "mathematics"]
  }
}
```

## User Management

### GET /users/profile
Get current user's detailed profile.

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "profile": {
    "learning_level": "intermediate",
    "learning_style": "visual",
    "preferred_subjects": ["python", "dbms"],
    "progress_data": {},
    "performance_metrics": {}
  }
}
```

### PUT /users/profile
Update user profile information.

**Request Body:**
```json
{
  "learning_level": "advanced",
  "learning_style": "kinesthetic",
  "preferred_subjects": ["python", "psychology"],
  "bio": "Computer science student"
}
```

### GET /users/dashboard
Get user dashboard data with progress and statistics.

**Response:**
```json
{
  "stats": {
    "total_quiz_attempts": 15,
    "average_score": 85.5,
    "study_time_hours": 45.2,
    "subjects_studied": 5
  },
  "recent_activity": [],
  "progress": {
    "python": 75,
    "mathematics": 60
  }
}
```

## Content Management

### POST /content/upload
Upload and process educational content.

**Request:**
```http
POST /content/upload
Content-Type: multipart/form-data
Authorization: Bearer <access_token>

file: <pdf_file>
subject: "python"
difficulty: "intermediate"
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Python Basics",
  "subject": "python",
  "content_type": "pdf",
  "status": "processing",
  "file_size": 1024000,
  "uploaded_at": "2024-01-01T00:00:00Z"
}
```

### GET /content/list
List available content items.

**Query Parameters:**
- `subject` (optional): Filter by subject
- `status` (optional): Filter by processing status
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Python Basics",
      "subject": "python",
      "content_type": "pdf",
      "status": "processed",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "pages": 3
  }
}
```

### GET /content/{content_id}
Get specific content item details.

**Response:**
```json
{
  "id": "uuid",
  "title": "Python Basics",
  "description": "Introduction to Python programming",
  "subject": "python",
  "content_type": "pdf",
  "status": "processed",
  "extracted_text": "Content text...",
  "summary": "This document covers...",
  "tags": ["programming", "basics"],
  "metadata": {
    "page_count": 50,
    "word_count": 10000
  }
}
```

### POST /content/{content_id}/summarize
Generate AI summary of content.

**Response:**
```json
{
  "summary": {
    "brief": "Short summary...",
    "detailed": "Detailed summary...",
    "key_points": ["Point 1", "Point 2", "Point 3"]
  },
  "generated_at": "2024-01-01T00:00:00Z"
}
```

## AI Chat

### POST /chat/sessions
Create new chat session.

**Request Body:**
```json
{
  "subject": "python",
  "title": "Python Learning Session"
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Python Learning Session",
  "subject": "python",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /chat/sessions
List user's chat sessions.

**Response:**
```json
{
  "sessions": [
    {
      "id": "uuid",
      "title": "Python Learning Session",
      "subject": "python",
      "message_count": 10,
      "last_message_at": "2024-01-01T12:00:00Z",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### POST /chat/sessions/{session_id}/messages
Send message in chat session.

**Request Body:**
```json
{
  "content": "Explain Python list comprehensions",
  "context_sources": ["content_id_1", "content_id_2"]
}
```

**Response:**
```json
{
  "user_message": {
    "id": "uuid",
    "content": "Explain Python list comprehensions",
    "role": "user",
    "created_at": "2024-01-01T12:00:00Z"
  },
  "ai_response": {
    "id": "uuid",
    "content": "List comprehensions in Python...",
    "role": "assistant",
    "sources": ["content_id_1"],
    "created_at": "2024-01-01T12:00:01Z"
  }
}
```

### GET /chat/sessions/{session_id}/messages
Get chat session messages.

**Response:**
```json
{
  "messages": [
    {
      "id": "uuid",
      "content": "Hello, I'd like to learn about Python",
      "role": "user",
      "created_at": "2024-01-01T12:00:00Z"
    },
    {
      "id": "uuid",
      "content": "Hello! I'm your AI tutor for Python...",
      "role": "assistant",
      "created_at": "2024-01-01T12:00:01Z"
    }
  ]
}
```

## Quiz Management

### POST /quiz/generate
Generate AI-powered quiz from content.

**Request Body:**
```json
{
  "subject": "python",
  "content_ids": ["uuid1", "uuid2"],
  "difficulty": "medium",
  "num_questions": 10,
  "question_types": ["multiple_choice", "true_false"],
  "time_limit_minutes": 30
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Python Quiz - Medium",
  "subject": "python",
  "difficulty": "medium",
  "total_questions": 10,
  "time_limit_minutes": 30,
  "questions": [
    {
      "id": "uuid",
      "question_text": "What is a Python list?",
      "question_type": "multiple_choice",
      "options": [
        "A mutable sequence type",
        "An immutable sequence type",
        "A dictionary type",
        "A function type"
      ],
      "correct_answer": 0,
      "points": 1.0
    }
  ],
  "created_at": "2024-01-01T12:00:00Z"
}
```

### GET /quiz/list
List available quizzes.

**Query Parameters:**
- `subject` (optional): Filter by subject
- `difficulty` (optional): Filter by difficulty
- `created_by` (optional): Filter by creator

**Response:**
```json
{
  "quizzes": [
    {
      "id": "uuid",
      "title": "Python Basics Quiz",
      "subject": "python",
      "difficulty": "easy",
      "total_questions": 10,
      "pass_rate": 85.5,
      "attempts_count": 150,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### POST /quiz/{quiz_id}/attempt
Start a quiz attempt.

**Response:**
```json
{
  "attempt_id": "uuid",
  "quiz_id": "uuid",
  "started_at": "2024-01-01T12:00:00Z",
  "time_limit_minutes": 30,
  "questions": [
    {
      "id": "uuid",
      "question_text": "What is a Python list?",
      "question_type": "multiple_choice",
      "options": ["Option A", "Option B", "Option C", "Option D"]
    }
  ]
}
```

### POST /quiz/attempts/{attempt_id}/submit
Submit quiz attempt.

**Request Body:**
```json
{
  "answers": {
    "question_id_1": 0,
    "question_id_2": 1
  },
  "time_taken_seconds": 1200
}
```

**Response:**
```json
{
  "attempt_id": "uuid",
  "score": 8.5,
  "percentage": 85.0,
  "correct_answers": 8,
  "incorrect_answers": 2,
  "is_passed": true,
  "detailed_results": {
    "question_id_1": {
      "user_answer": 0,
      "correct_answer": 0,
      "is_correct": true,
      "points": 1.0
    }
  },
  "submitted_at": "2024-01-01T12:30:00Z"
}
```

## Analytics

### GET /analytics/dashboard
Get comprehensive analytics dashboard.

**Query Parameters:**
- `period` (optional): Time period (7d, 30d, 90d, 1y)
- `subject` (optional): Filter by subject

**Response:**
```json
{
  "overview": {
    "total_users": 1234,
    "active_sessions": 89,
    "quizzes_generated": 456,
    "content_items": 234
  },
  "user_engagement": {
    "daily_active_users": 145,
    "average_session_duration": 28.5,
    "retention_rate": 0.75
  },
  "learning_progress": {
    "subjects": {
      "python": {
        "learners": 456,
        "avg_progress": 65.2,
        "completion_rate": 0.78
      }
    }
  },
  "quiz_performance": {
    "average_score": 78.5,
    "pass_rate": 0.82,
    "improvement_rate": 0.15
  }
}
```

### GET /analytics/student/{student_id}
Get individual student analytics.

**Response:**
```json
{
  "student": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "progress": {
    "subjects": {
      "python": {
        "completion_percentage": 75,
        "time_spent_hours": 45.2,
        "quiz_average": 85.5,
        "last_activity": "2024-01-01T12:00:00Z"
      }
    }
  },
  "performance_trends": {
    "quiz_scores": [70, 75, 80, 85, 90],
    "study_time": [2.5, 3.0, 2.8, 4.1, 3.5]
  },
  "recommendations": [
    "Focus more on error handling concepts",
    "Practice more coding exercises"
  ]
}
```

## Error Handling

The API uses standard HTTP status codes and returns error details in JSON format:

```json
{
  "detail": "Error description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Rate Limiting

API endpoints are rate limited:
- **General endpoints**: 60 requests per minute
- **AI processing**: 10 requests per minute
- **File uploads**: 5 requests per minute

Rate limit headers:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page`: Page number (starts at 1)
- `limit`: Items per page (max 100)

**Response Format:**
```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 150,
    "pages": 15,
    "has_next": true,
    "has_prev": false
  }
}
```

## WebSocket Support

Real-time features use WebSocket connections:

### Chat WebSocket
```
ws://localhost:8001/ws/chat/{session_id}?token=<jwt_token>
```

**Message Format:**
```json
{
  "type": "message",
  "content": "Hello",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Quiz WebSocket
```
ws://localhost:8001/ws/quiz/{attempt_id}?token=<jwt_token>
```

**Message Types:**
- `question`: New question
- `answer`: Answer submission
- `time_warning`: Time running out
- `completion`: Quiz completed

## SDK and Client Libraries

### Python SDK
```python
from edunlpx_client import EduNLPXClient

client = EduNLPXClient(
    base_url="http://localhost:8001",
    api_key="your_api_key"
)

# Authenticate
client.auth.login("user@example.com", "password")

# Upload content
content = client.content.upload("document.pdf", subject="python")

# Generate quiz
quiz = client.quiz.generate(subject="python", difficulty="medium")
```

### JavaScript SDK
```javascript
import { EduNLPXClient } from '@edunlpx/client';

const client = new EduNLPXClient({
  baseURL: 'http://localhost:8001',
  apiKey: 'your_api_key'
});

// Authenticate
await client.auth.login('user@example.com', 'password');

// Start chat session
const session = await client.chat.createSession('python');
const response = await client.chat.sendMessage(session.id, 'Explain lists');
```

## Testing

The API includes comprehensive test coverage. Use the test client for integration testing:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_registration():
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 201
```

## OpenAPI Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`
- OpenAPI JSON: `http://localhost:8001/openapi.json`
