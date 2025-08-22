#!/bin/bash

# EduNLP-X Deployment Script
# This script handles deployment to different environments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default values
ENVIRONMENT="development"
SKIP_TESTS=false
SKIP_BUILD=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -e, --environment ENV    Deployment environment (development|staging|production)"
            echo "  --skip-tests            Skip running tests"
            echo "  --skip-build            Skip building containers"
            echo "  -h, --help              Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option $1"
            exit 1
            ;;
    esac
done

print_status "Starting deployment to $ENVIRONMENT environment..."

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Docker is installed and running
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    # Check if Docker Compose is available
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if environment file exists
    if [[ ! -f ".env" ]]; then
        print_warning ".env file not found, copying from .env.example"
        cp .env.example .env
        print_warning "Please update .env file with your configuration"
    fi
    
    print_success "Prerequisites check passed"
}

# Run tests
run_tests() {
    if [[ "$SKIP_TESTS" == "true" ]]; then
        print_warning "Skipping tests as requested"
        return
    fi
    
    print_status "Running tests..."
    
    # Backend tests
    print_status "Running backend tests..."
    if ! make test-backend; then
        print_error "Backend tests failed"
        exit 1
    fi
    
    print_success "All tests passed"
}

# Build containers
build_containers() {
    if [[ "$SKIP_BUILD" == "true" ]]; then
        print_warning "Skipping container build as requested"
        return
    fi
    
    print_status "Building Docker containers..."
    
    case $ENVIRONMENT in
        "development")
            docker-compose build
            ;;
        "staging"|"production")
            docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
            ;;
        *)
            print_error "Unknown environment: $ENVIRONMENT"
            exit 1
            ;;
    esac
    
    print_success "Containers built successfully"
}

# Deploy to development
deploy_development() {
    print_status "Deploying to development environment..."
    
    # Start services
    docker-compose up -d postgres redis chromadb
    
    # Wait for database to be ready
    print_status "Waiting for database to be ready..."
    sleep 10
    
    # Run database migrations
    print_status "Running database migrations..."
    docker-compose exec -T backend alembic upgrade head
    
    # Start all services
    docker-compose up -d
    
    # Health check
    print_status "Performing health checks..."
    sleep 15
    
    if curl -f http://localhost:8001/health &> /dev/null; then
        print_success "Backend health check passed"
    else
        print_error "Backend health check failed"
        exit 1
    fi
    
    print_success "Development deployment completed!"
    print_status "Services available at:"
    echo "  - Backend API: http://localhost:8001"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Streamlit MVP: http://localhost:8501"
    echo "  - API Docs: http://localhost:8001/docs"
}

# Deploy to staging
deploy_staging() {
    print_status "Deploying to staging environment..."
    
    # Add staging-specific deployment logic here
    # This might involve:
    # - Building production images
    # - Pushing to container registry
    # - Deploying to staging server
    # - Running smoke tests
    
    print_warning "Staging deployment logic needs to be implemented"
    print_status "Please configure your staging environment deployment"
}

# Deploy to production
deploy_production() {
    print_status "Deploying to production environment..."
    
    # Production deployment safety checks
    read -p "Are you sure you want to deploy to production? (yes/no): " confirm
    if [[ $confirm != "yes" ]]; then
        print_warning "Production deployment cancelled"
        exit 0
    fi
    
    # Add production deployment logic here
    # This might involve:
    # - Final tests
    # - Blue-green deployment
    # - Database migrations
    # - Health checks
    # - Rollback capability
    
    print_warning "Production deployment logic needs to be implemented"
    print_status "Please configure your production environment deployment"
}

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    # Add cleanup logic if needed
}

# Set trap for cleanup
trap cleanup EXIT

# Main deployment flow
main() {
    print_status "EduNLP-X Deployment Script"
    print_status "Environment: $ENVIRONMENT"
    print_status "Skip Tests: $SKIP_TESTS"
    print_status "Skip Build: $SKIP_BUILD"
    echo ""
    
    check_prerequisites
    run_tests
    build_containers
    
    case $ENVIRONMENT in
        "development")
            deploy_development
            ;;
        "staging")
            deploy_staging
            ;;
        "production")
            deploy_production
            ;;
        *)
            print_error "Unknown environment: $ENVIRONMENT"
            exit 1
            ;;
    esac
}

# Run main function
main
