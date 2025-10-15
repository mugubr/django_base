#!/bin/bash
# Automated development setup script for Django Base project
# Script de configuração automatizada de desenvolvimento para projeto Django Base

set -e

# Colors for output / Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions / Funções auxiliares
print_header() {
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Default values / Valores padrão
RUN_PRECOMMIT=true
RUN_TESTS=true
RUN_COVERAGE=true
SEED_DB=true
SKIP_BUILD=false
QUICK_MODE=false

# Parse arguments / Analisar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-precommit)
            RUN_PRECOMMIT=false
            shift
            ;;
        --skip-tests)
            RUN_TESTS=false
            shift
            ;;
        --skip-coverage)
            RUN_COVERAGE=false
            shift
            ;;
        --no-seed)
            SEED_DB=false
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --quick)
            QUICK_MODE=true
            RUN_TESTS=false
            RUN_PRECOMMIT=false
            shift
            ;;
        --help|-h)
            echo "Usage: ./setup.sh [OPTIONS]"
            echo ""
            echo "Development setup script for Django Base"
            echo ""
            echo "Options:"
            echo "  --skip-precommit    Skip pre-commit hooks installation and run"
            echo "  --skip-tests        Skip running tests"
            echo "  --skip-coverage     Skip coverage report generation"
            echo "  --no-seed           Don't seed database with sample data"
            echo "  --skip-build        Skip Docker build (use if images already exist)"
            echo "  --quick             Quick mode: skip tests and pre-commit (faster setup)"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./setup.sh                    # Full setup with all features"
            echo "  ./setup.sh --quick            # Quick setup for rapid testing"
            echo "  ./setup.sh --skip-build       # Skip Docker build (if images exist)"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Main setup / Configuração principal
print_header "🚀 Django Base - Development Setup"
if [ "$QUICK_MODE" = true ]; then
    print_warning "Running in QUICK MODE (tests and pre-commit disabled)"
fi
echo ""

# Step 1: Check if .env exists / Verificar se .env existe
print_header "Step 1/7: Environment Configuration"
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_success ".env file created"
    print_warning "Please review and update .env file with your settings"
else
    print_success ".env file already exists"
fi
echo ""

# Step 2: Docker setup / Configuração Docker
print_header "Step 2/7: Docker Setup"
if [ "$SKIP_BUILD" = false ]; then
    print_info "Building Docker images (development)..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev build
    print_success "Docker images built"
else
    print_info "Skipping Docker build (--skip-build)"
fi

print_info "Starting development containers..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d

# Wait for containers to be healthy / Aguardar containers ficarem healthy
print_info "Waiting for containers to be healthy (10s)..."
sleep 10

# Check if containers are running / Verificar se containers estão rodando
if ! docker-compose ps | grep -q "Up"; then
    print_error "Some containers failed to start"
    print_info "Check logs with: make dev-logs"
    exit 1
fi
print_success "All containers started successfully"
echo ""

# Step 3: Run migrations / Executar migrações
print_header "Step 3/7: Database Migrations"
print_info "Creating migrations..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web python manage.py makemigrations || true
print_info "Running migrations..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web python manage.py migrate --noinput
print_success "Migrations completed"
echo ""

# Step 4: Create superuser / Criar superusuário
print_header "Step 4/7: Superuser Creation"
print_info "Creating development superuser (admin/admin)..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('✓ Superuser created: admin/admin')
else:
    print('ℹ Superuser already exists')
EOF
print_success "Superuser ready (admin/admin)"
echo ""

# Step 5: Seed database / Popular banco
print_header "Step 5/7: Database Seeding"
if [ "$SEED_DB" = true ]; then
    print_info "Seeding database with sample data..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web python manage.py shell << 'EOF'
from core.models import Product
if Product.objects.count() == 0:
    print('🌱 Seeding database...')
    import os
    os.system('python manage.py seed_database')
else:
    print('ℹ Database already has data')
EOF
    print_success "Database seeding completed"
else
    print_info "Skipping database seeding (--no-seed)"
fi
echo ""

# Step 6: Compile translations / Compilar traduções
print_header "Step 6/7: Compile Translations"
print_info "Updating translation files (pt-br, en)..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web python manage.py makemessages -l pt_BR -l en --ignore=.venv || true
print_info "Compiling translations..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web python manage.py compilemessages
print_success "Translations compiled successfully"
print_info "Supported languages: Português (Brasil), English"
echo ""

# Step 7: Tests, Coverage, and Pre-commit / Testes, Cobertura e Pre-commit
print_header "Step 7/7: Quality Checks (Tests & Pre-commit)"

# Run tests first
if [ "$RUN_TESTS" = true ]; then
    print_info "Running tests..."
    if [ "$RUN_COVERAGE" = true ]; then
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web coverage run manage.py test src
        print_success "Tests completed"

        print_info "Generating coverage report..."
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web coverage report
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web coverage html
        print_success "Coverage report generated (htmlcov/index.html)"
    else
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web python manage.py test src
        print_success "Tests completed"
    fi
else
    print_info "Tests skipped (--skip-tests or --quick)"
fi

# Then run pre-commit hooks
if [ "$RUN_PRECOMMIT" = true ]; then
    print_info "Installing pre-commit hooks..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web pre-commit install || true
    print_success "Pre-commit hooks installed"

    print_info "Running pre-commit hooks on all files..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec -T web pre-commit run --all-files || true
    print_success "Pre-commit check completed"
else
    print_info "Pre-commit hooks skipped (--skip-precommit or --quick)"
fi
echo ""

# Final summary / Resumo final
print_header "✅ Development Setup Complete!"
echo ""
print_success "All steps completed successfully!"
echo ""
print_info "Access points / Pontos de acesso:"
echo "  - Application: http://localhost:8000"
echo "  - Admin Panel: http://localhost:8000/admin"
echo "  - API Docs (Swagger): http://localhost:8000/api/docs/"
echo "  - API Docs (ReDoc): http://localhost:8000/api/redoc/"
echo "  - Health Check: http://localhost:8000/health-status/"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3000"
echo ""
print_info "Credentials / Credenciais:"
echo "  - Django Admin: admin / admin"
echo "  - Grafana: admin / admin"
echo ""
print_info "Available services / Serviços disponíveis:"
echo "  - Django (port 8000)"
echo "  - PostgreSQL (port 5432)"
echo "  - Redis (port 6379)"
echo "  - Prometheus (port 9090)"
echo "  - Grafana (port 3000)"
echo "  - PostgreSQL Exporter (port 9187)"
echo "  - Redis Exporter (port 9121)"
echo ""
print_info "Quick commands / Comandos rápidos:"
echo "  - View logs: make dev-logs"
echo "  - Stop all: make dev-down"
echo "  - Shell: make bash"
echo "  - Django shell: make shell"
echo "  - Run tests: make test"
echo "  - Coverage: make coverage-html"
echo "  - Format code: make format"
echo "  - Run linter: make lint"
echo ""
print_info "Next steps / Próximos passos:"
echo "  1. Access the application at http://localhost:8000"
echo "  2. Login to admin with: admin/admin"
echo "  3. Explore the API docs at http://localhost:8000/api/docs/"
echo "  4. Check Grafana dashboards at http://localhost:3000"
echo "  5. Review the README.md for more information"
echo ""
if [ "$QUICK_MODE" = true ]; then
    print_warning "Quick mode was used - remember to run tests before committing:"
    echo "  make test"
fi
echo ""
print_success "Happy coding! 🚀 / Bom trabalho! 🚀"
