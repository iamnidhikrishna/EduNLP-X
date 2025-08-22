# EduNLP-X: AI-Powered Educational Platform

EduNLP-X is an intelligent educational platform that leverages Natural Language Processing (NLP) and Large Language Models (LLMs) to provide personalized tutoring, content ingestion, quiz generation, and comprehensive student analytics.

## 🚀 Features

- **AI-Powered Tutoring**: Subject-specific AI tutors with adaptive learning
- **Content Ingestion**: Multi-format document processing (PDF, DOCX, TXT, videos)
- **Quiz Generation**: Automated quiz creation and evaluation
- **Student Analytics**: Comprehensive progress tracking and insights
- **Multi-Role Support**: Students, teachers, administrators, and parents
- **Real-time Chat**: Interactive AI-powered educational conversations

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   AI/ML Layer   │
│                 │    │                  │    │                 │
│ - React/Next.js │◄─►│ - FastAPI        │◄──►│ - LangChain     │
│ - Streamlit MVP │    │ - PostgreSQL     │    │ - Ollama/OpenAI │
│ - TypeScript    │    │ - Redis Cache    │    │ - ChromaDB      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                         │                         │
         └────────────────────────┼────────────────────────┘
                                  │
                           ┌────────▼────────┐
                           │  Infrastructure │
                           │                 │
                           │ - Docker        │
                           │ - AWS/Railway   │
                           │ - CI/CD         │
                           └─────────────────┘
```

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React/Next.js, Streamlit | User interface, responsive design |
| Backend | FastAPI, Python | REST API, business logic |
| Database | PostgreSQL, Redis | Data persistence, caching |
| AI/ML | LangChain, Ollama, OpenAI | NLP processing, chat functionality |
| Vector DB | ChromaDB, Pinecone | Document embeddings, semantic search |
| Auth | JWT, OAuth2 | Authentication, authorization |
| Payment | Razorpay | Payment processing |
| Storage | AWS S3, Local | File storage, media assets |
| Deployment | Docker, Railway/AWS | Containerization, cloud hosting |

## 📁 Project Structure

```
edunlp-x/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── alembic/           # Database migrations
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── ai_services/           # AI/ML components
│   ├── models/
│   ├── embeddings/
│   └── processors/
├── streamlit_app/         # Streamlit MVP
├── docker/                # Docker configurations
├── docs/                  # Documentation
└── tests/                 # Test suites
```

## 🚦 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd edunlp-x
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   # Start PostgreSQL and Redis with Docker
   docker-compose up -d postgres redis
   
   # Run database migrations
   alembic upgrade head
   ```

4. **Start Backend**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. **Access the Application**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

### Docker Setup

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d
```

## 📊 User Roles

- **Super Admin**: Platform-wide access and management
- **Admin**: Institution-level management and oversight
- **Principal**: Academic oversight and administration
- **Teacher**: Content creation and student management
- **Accountant**: Financial management and reporting
- **Coordinator**: Student management and inventory
- **Student**: Learning activities and progress tracking
- **Parent**: Student progress monitoring

## 🔐 Security Features

- JWT-based authentication with secure token handling
- Role-based access control (RBAC)
- Data encryption at rest and in transit
- Input validation and sanitization
- Rate limiting and abuse prevention
- GDPR compliance ready
- Regular security updates (see `SECURITY_UPDATES.md`)
- Automated vulnerability scanning

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Run all tests with coverage
make test
```

## 🚀 Deployment

### Development
- Local development with Docker Compose
- Hot reloading for both frontend and backend

### Production
- Railway/AWS deployment
- Auto-scaling configuration
- CI/CD with GitHub Actions
- Comprehensive monitoring and logging

## 📈 Development Phases

- **Phase 0**: Project Setup & Infrastructure ✅
- **Phase 1**: Authentication & Authorization System
- **Phase 2**: Core AI Chatbot Development
- **Phase 3**: Content Management System
- **Phase 4**: Quiz Generation & Assessment
- **Phase 5**: Advanced AI Features
- **Phase 6**: Payment Integration & CRM
- **Phase 7**: Analytics & Reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, email support@edunlpx.com or join our Slack channel.

## 🙏 Acknowledgments

- LangChain community for excellent AI tools
- FastAPI for the robust web framework
- React team for the frontend framework
