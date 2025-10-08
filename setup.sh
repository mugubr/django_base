#!/bin/bash
# Automated setup script for Django Base project
# Script de configuração automatizada para projeto Django Base

set -e

# Colors for output / Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions / Funções auxiliares
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
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
    echo -e "${BLUE}ℹ $1${NC}"
}

# Default values / Valores padrão
ENVIRONMENT="dev"
RUN_PRECOMMIT=true
RUN_TESTS=true
RUN_COVERAGE=true
SEED_DB=true
SKIP_BUILD=false

# Parse arguments / Analisar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --prod)
            ENVIRONMENT="prod"
            shift
            ;;
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
        --help|-h)
            echo "Usage: ./setup.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --prod              Set up production environment (default: dev)"
            echo "  --skip-precommit    Skip pre-commit hooks installation and run"
            echo "  --skip-tests        Skip running tests"
            echo "  --skip-coverage     Skip coverage report generation"
            echo "  --no-seed           Don't seed database with sample data"
            echo "  --skip-build        Skip Docker build (use if images already exist)"
            echo "  --help, -h          Show this help message"
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
print_header "Django Base - Automated Setup"
print_info "Environment: $ENVIRONMENT"
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
    print_info "Building Docker images..."
    if [ "$ENVIRONMENT" = "prod" ]; then
        docker-compose --profile prod build
    else
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev build
    fi
    print_success "Docker images built"
else
    print_info "Skipping Docker build (--skip-build)"
fi

print_info "Starting containers..."
if [ "$ENVIRONMENT" = "prod" ]; then
    docker-compose --profile prod up -d
else
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d
fi

# Wait for containers to be healthy / Aguardar containers ficarem healthy
print_info "Waiting for containers to be healthy..."
sleep 10
print_success "Containers started"
echo ""

# Step 3: Run migrations / Executar migrações
print_header "Step 3/7: Database Migrations"
print_info "Running migrations..."
if [ "$ENVIRONMENT" = "dev" ]; then
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec -T web python manage.py migrate --noinput
else
    docker-compose --profile prod exec -T web python manage.py migrate --noinput
fi
print_success "Migrations completed"
echo ""

# Step 4: Create superuser / Criar superusuário
print_header "Step 4/7: Superuser Creation"
if [ "$ENVIRONMENT" = "dev" ]; then
    print_info "Creating superuser (admin/admin)..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec -T web python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('✓ Superuser created: admin/admin')
else:
    print('ℹ Superuser already exists')
EOF
    print_success "Superuser ready"
else
    print_warning "Superuser creation skipped in production (create manually)"
fi
echo ""

# Step 5: Seed database / Popular banco
print_header "Step 5/7: Database Seeding"
if [ "$SEED_DB" = true ] && [ "$ENVIRONMENT" = "dev" ]; then
    print_info "Seeding database..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec -T web python manage.py shell << 'EOF'
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
    if [ "$ENVIRONMENT" = "prod" ]; then
        print_info "Database seeding skipped in production"
    else
        print_info "Skipping database seeding (--no-seed)"
    fi
fi
echo ""

# Step 6: Compile translations / Compilar traduções
print_header "Step 6/7: Compile Translations"
if [ "$ENVIRONMENT" = "dev" ]; then
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec -T web python manage.py compilemessages
else
    docker-compose --profile prod exec -T web python manage.py compilemessages
fi
print_success "Translations compiled"
echo ""

# Step 7: Tests and Coverage / Testes e Cobertura
print_header "Step 7/7: Tests and Coverage"
if [ "$RUN_TESTS" = true ] && [ "$ENVIRONMENT" = "dev" ]; then
    print_info "Running tests..."
    if [ "$RUN_COVERAGE" = true ]; then
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec -T web coverage run manage.py test core
        print_success "Tests completed"

        print_info "Generating coverage report..."
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec -T web coverage report
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec -T web coverage html
        print_success "Coverage report generated (htmlcov/index.html)"
    else
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec -T web python manage.py test core
        print_success "Tests completed"
    fi
else
    if [ "$ENVIRONMENT" = "prod" ]; then
        print_info "Tests skipped in production mode"
    else
        print_info "Tests skipped (--skip-tests)"
    fi
fi
echo ""

# Final summary / Resumo final
print_header "Setup Complete!"
echo ""
print_success "All steps completed successfully!"
echo ""
print_info "Access points / Pontos de acesso:"
echo "  - Application: http://localhost:8000"
echo "  - Admin Panel: http://localhost:8000/admin"
echo "  - API Docs: http://localhost:8000/api/docs/"
echo "  - Health Check: http://localhost:8000/health-status/"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3000"
echo ""
print_info "Credentials / Credenciais:"
echo "  - Superuser: admin / admin"
echo "  - Grafana: admin / admin"
echo ""
print_info "Useful commands / Comandos úteis:"
if [ "$ENVIRONMENT" = "dev" ]; then
    echo "  - View logs: docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f web"
    echo "  - Stop: docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down"
    echo "  - Shell: docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web bash"
else
    echo "  - View logs: docker-compose logs -f web"
    echo "  - Stop: docker-compose --profile prod down"
    echo "  - Shell: docker-compose exec web bash"
fi
echo ""
print_success "Happy coding! / Bom trabalho!"
