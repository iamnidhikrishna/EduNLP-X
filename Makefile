# EduNLP-X Development Makefile
# Common development tasks and utilities

.PHONY: help install setup-db dev test clean build deploy

# Default target
help:
    @echo "EduNLP-X Development Commands:"
    @echo ""
    @echo "Setup Commands:"
    @echo "  make install     - Install all dependencies"
    @echo "  make setup-db    - Initialize database and run migrations"
    @echo "  make dev         - Start development servers"
    @echo ""
    @echo "Development Commands:"
    @echo "  make test        - Run all tests with coverage"
    @echo "  make test-unit   - Run unit tests only"
    @echo "  make test-integration - Run integration tests only"
    @echo "  make test-backend - Run backend tests with coverage"
    @echo "  make lint        - Run linting and formatting"
    @echo "  make migration   - Create new database migration"
    @echo "  make migrate     - Run database migrations"
    @echo ""
    @echo "Docker Commands:"
    @echo "  make build       - Build all Docker containers"
    @echo "  make up          - Start all services with Docker Compose"
    @echo "  make down        - Stop all services"
    @echo "  make logs        - View logs from all services"
    @echo ""
    @echo "Security Commands:"
    @echo "  make security-audit   - Run security audit on dependencies"
    @echo "  make security-update  - Show security update instructions"
    @echo ""
    @echo "Utility Commands:"
    @echo "  make clean       - Clean up temporary files and caches"
    @echo "  make backup      - Backup database"
    @echo "  make restore     - Restore database from backup"

# Installation and Setup
install:
    @echo "Installing backend dependencies..."
    cd backend && pip install -r requirements.txt
    @echo "Installing frontend dependencies..."
    cd frontend && npm install
    @echo "Installing streamlit dependencies..."
    cd streamlit_app && pip install -r requirements.txt

setup-db:
    @echo "Setting up database..."
    docker-compose up -d postgres redis
    @echo "Waiting for database to be ready..."
    sleep 10
    @echo "Running database migrations..."
    cd backend && alembic upgrade head
    @echo "Database setup complete!"

# Development
dev:
    @echo "Starting development environment..."
    docker-compose up --build

dev-backend:
    @echo "Starting backend development server..."
    cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
    @echo "Starting frontend development server..."
    cd frontend && npm run dev

dev-streamlit:
    @echo "Starting Streamlit development server..."
    cd streamlit_app && streamlit run main.py

# Testing
test:
    @echo "Running all tests..."
    cd backend && pytest -v --cov=app --cov-report=html --cov-report=term
    @echo "Tests complete!"

test-unit:
    @echo "Running unit tests..."
    cd backend && pytest tests/unit -v

test-integration:
    @echo "Running integration tests..."
    cd backend && pytest tests/integration -v

test-watch:
    @echo "Running tests in watch mode..."
    cd backend && pytest-watch

test-backend:
    @echo "Running backend tests..."
    cd backend && pytest -v --cov=app --cov-report=term-missing

lint:
    @echo "Running linting and formatting..."
    cd backend && black app/
    cd backend && flake8 app/
    cd backend && mypy app/

# Database Operations
migration:
    @echo "Creating new migration..."
    cd backend && alembic revision --autogenerate -m "$(MSG)"

migrate:
    @echo "Running database migrations..."
    cd backend && alembic upgrade head

migrate-down:
    @echo "Rolling back last migration..."
    cd backend && alembic downgrade -1

# Docker Operations
build:
    @echo "Building Docker containers..."
    docker-compose build

up:
    @echo "Starting all services..."
    docker-compose up -d

down:
    @echo "Stopping all services..."
    docker-compose down

logs:
    @echo "Viewing logs from all services..."
    docker-compose logs -f

restart:
    @echo "Restarting all services..."
    docker-compose restart

# Security
security-audit:
    @echo "Running security audit..."
    @echo "Backend dependencies:"
    cd backend && pip-audit --requirement requirements.txt --format=table || echo "pip-audit not installed, run: pip install pip-audit"
    @echo "Streamlit dependencies:"
    cd streamlit_app && pip-audit --requirement requirements.txt --format=table || echo "pip-audit not installed"
    @echo "Frontend dependencies:"
    cd frontend && npm audit || echo "npm not available"

security-update:
    @echo "Updating dependencies to latest secure versions..."
    @echo "Please review SECURITY_UPDATES.md for manual update instructions"
    @echo "This process requires manual review of breaking changes"

# Utilities
clean:
    @echo "Cleaning up..."
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    find . -type f -name "*.log" -delete
    rm -rf backend/htmlcov/
    rm -rf backend/.coverage
    rm -rf backend/.pytest_cache/
    @echo "Cleanup complete!"

backup:
    @echo "Creating database backup..."
    docker-compose exec postgres pg_dump -U edunlpx_user edunlpx_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
    @echo "Backup created!"

restore:
    @echo "Restoring database from backup..."
    @echo "Usage: make restore BACKUP_FILE=backup_filename.sql"
    docker-compose exec -T postgres psql -U edunlpx_user -d edunlpx_db < $(BACKUP_FILE)

# Health checks
health:
    @echo "Checking service health..."
    @echo "Backend: $(shell curl -s http://localhost:8001/health | jq -r .status)"
    @echo "Frontend: $(shell curl -s http://localhost:3000 > /dev/null && echo 'OK' || echo 'ERROR')"
    @echo "Database: $(shell docker-compose exec postgres pg_isready -U edunlpx_user && echo 'OK' || echo 'ERROR')"
    @echo "Redis: $(shell docker-compose exec redis redis-cli ping)"

# Environment setup
env:
    @echo "Setting up environment file..."
    cp .env.example .env
    @echo "Please update .env file with your configuration"

# Full setup (for new developers)
setup: env install build setup-db
    @echo "Full setup complete!"
    @echo "Run 'make dev' to start development servers"
