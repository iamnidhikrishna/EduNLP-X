# EduNLP-X Development Guide

## Overview

EduNLP-X is an AI-powered educational platform built with modern technologies to provide personalized learning experiences. This guide covers the development setup, architecture, and contribution guidelines.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+ (optional, can use Docker)
- Redis 7+ (optional, can use Docker)

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd edunlp-x

# Copy environment configuration
cp .env.example .env
# Edit .env file with your configuration

# Set up environment (installs all dependencies)
make setup
```

### 2. Development with Docker (Recommended)

```bash
# Start all services
make dev

# Or manually with docker-compose
docker-compose up --build
```

### 3. Manual Development Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start database services
docker-compose up -d postgres redis

# Run migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Streamlit MVP
```bash
cd streamlit_app

# Install dependencies
pip install -r requirements.txt

# Start Streamlit app
streamlit run main.py
```

## Architecture Overview

### Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI + Python 3.11 | REST API, business logic |
| **Database** | PostgreSQL 15 | Primary data storage |
| **Cache** | Redis 7 | Session storage, caching |
| **Frontend** | Next.js + React + TypeScript | User interface |
| **AI/ML** | LangChain + Ollama/OpenAI | NLP processing, chat |
| **Vector DB** | ChromaDB | Document embeddings, search |
| **Container** | Docker + Docker Compose | Development environment |

### Directory Structure

```
edunlp-x/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API route handlers
│   │   ├── core/           # Core configuration and utilities
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── services/       # Business logic layer
│   │   ├── schemas/        # Pydantic request/response models
│   │   └── utils/          # Helper utilities
│   ├── alembic/           # Database migration scripts
│   └── requirements.txt    # Python dependencies
├── frontend/              # Next.js frontend application
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── pages/         # Next.js pages/routes
│   │   └── services/      # API client services
│   └── package.json       # Node.js dependencies
├── streamlit_app/         # Streamlit MVP interface
├── ai_services/           # AI/ML processing modules
├── docker/                # Docker configuration files
├── docs/                  # Project documentation
└── tests/                 # Test suites
```

## Development Workflow

### 1. Database Migrations

```bash
# Create new migration
make migration MSG="Description of changes"

# Apply migrations
make migrate

# Rollback migration
make migrate-down
```

### 2. Running Tests

```bash
# Run all tests
make test

# Run backend tests only
cd backend && pytest -v

# Run with coverage
cd backend && pytest --cov=app --cov-report=html
```

### 3. Code Quality

```bash
# Format and lint code
make lint

# Manual formatting
cd backend && black app/
cd backend && flake8 app/
cd backend && mypy app/
```

### 4. Docker Operations

```bash
# Build containers
make build

# Start services
make up

# Stop services
make down

# View logs
make logs

# Restart services
make restart
```

## API Development

### Adding New Endpoints

1. **Create/Update Models** (if needed)
   ```python
   # backend/app/models/your_model.py
   from app.models.base import BaseModel
   
   class YourModel(BaseModel):
       __tablename__ = "your_table"
       # Define columns
   ```

2. **Create Schemas**
   ```python
   # backend/app/schemas/your_schema.py
   from pydantic import BaseModel
   
   class YourSchema(BaseModel):
       # Define fields
   ```

3. **Create Service**
   ```python
   # backend/app/services/your_service.py
   class YourService:
       def __init__(self, db: AsyncSession):
           self.db = db
       
       async def your_method(self):
           # Business logic
   ```

4. **Create Endpoints**
   ```python
   # backend/app/api/endpoints/your_endpoint.py
   from fastapi import APIRouter, Depends
   
   router = APIRouter()
   
   @router.post("/your-endpoint")
   async def your_endpoint():
       # Endpoint logic
   ```

5. **Register Router**
   ```python
   # backend/app/api/__init__.py
   from app.api.endpoints import your_endpoint
   
   api_router.include_router(
       your_endpoint.router, 
       prefix="/your-prefix", 
       tags=["Your Tag"]
   )
   ```

### Authentication

Use the `get_current_user` dependency for protected endpoints:

```python
from app.api.endpoints.auth import get_current_user

@router.get("/protected")
async def protected_endpoint(
    current_user: User = Depends(get_current_user)
):
    return {"user": current_user.email}
```

## Frontend Development

### Adding New Pages

1. Create page component in `frontend/src/pages/`
2. Use TypeScript for type safety
3. Follow React best practices
4. Use Tailwind CSS for styling

### API Integration

```typescript
// frontend/src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

export const yourService = {
  getData: () => api.get('/your-endpoint'),
  postData: (data: YourType) => api.post('/your-endpoint', data),
};
```

## AI/ML Integration

### Adding New AI Features

1. **Create AI Service**
   ```python
   # ai_services/your_ai_service.py
   from langchain.chat_models import ChatOllama
   
   class YourAIService:
       def __init__(self):
           self.model = ChatOllama(model="llama2")
       
       async def process(self, input_data):
           # AI processing logic
   ```

2. **Integrate with API**
   ```python
   # In your API endpoint
   ai_service = YourAIService()
   result = await ai_service.process(data)
   ```

## Testing

### Backend Testing

```python
# tests/unit/test_your_feature.py
import pytest
from fastapi.testclient import TestClient

def test_your_endpoint(client: TestClient):
    response = client.post("/api/v1/your-endpoint", json={})
    assert response.status_code == 200
```

### Frontend Testing

```typescript
// frontend/src/__tests__/YourComponent.test.tsx
import { render, screen } from '@testing-library/react';
import YourComponent from '../components/YourComponent';

test('renders your component', () => {
  render(<YourComponent />);
  expect(screen.getByText('Expected Text')).toBeInTheDocument();
});
```

## Deployment

### Development Deployment

```bash
# Deploy to staging
make deploy-staging
```

### Production Deployment

1. **Environment Configuration**
   - Set production environment variables
   - Configure database connections
   - Set up monitoring and logging

2. **Docker Deployment**
   ```bash
   # Build production images
   docker-compose -f docker-compose.prod.yml build
   
   # Deploy to production
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Cloud Deployment** (Railway/AWS)
   - Configure cloud provider settings
   - Set up CI/CD pipeline
   - Configure monitoring and alerts

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose ps postgres
   
   # Check logs
   docker-compose logs postgres
   ```

2. **Migration Issues**
   ```bash
   # Reset database (development only)
   make clean-db
   make setup-db
   ```

3. **Docker Issues**
   ```bash
   # Clean Docker resources
   docker system prune -f
   
   # Rebuild containers
   make build
   ```

### Performance Optimization

1. **Database Optimization**
   - Add appropriate indexes
   - Use database query analysis
   - Implement connection pooling

2. **API Optimization**
   - Use async/await properly
   - Implement caching with Redis
   - Add pagination for large datasets

3. **Frontend Optimization**
   - Use React Query for API caching
   - Implement lazy loading
   - Optimize bundle size

## Contributing

### Code Style

- **Python**: Follow PEP 8, use Black formatter
- **TypeScript**: Use ESLint and Prettier
- **Git**: Use conventional commit messages

### Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and add tests
4. Ensure all tests pass
5. Submit pull request with description

### Code Review Guidelines

- Ensure code quality and test coverage
- Check for security vulnerabilities (see Security section below)
- Verify API documentation updates
- Test functionality manually

## Security

### Dependency Security

The project uses automated security scanning to identify vulnerabilities in dependencies. See `SECURITY_UPDATES.md` for the latest security updates.

**Security Update Process:**
1. Run security audit: `npm audit` (frontend) and `pip-audit` (backend)
2. Review vulnerability reports
3. Update affected packages to secure versions
4. Test for breaking changes
5. Update security documentation

**Tools for Security:**
```bash
# Install security audit tools
pip install pip-audit
npm install -g npm-audit

# Run security audits
pip-audit --requirement backend/requirements.txt
npm audit --prefix frontend
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

## Support

For development questions and support:
- Create an issue in the repository
- Check existing documentation
- Review code examples in the codebase
