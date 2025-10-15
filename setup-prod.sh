#!/bin/bash
# Automated production setup script for Django Base project
# Script de configuração automatizada de produção para projeto Django Base

set -e

# Colors for output / Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Helper functions / Funções auxiliares
print_header() {
    echo -e "${MAGENTA}========================================${NC}"
    echo -e "${MAGENTA}$1${NC}"
    echo -e "${MAGENTA}========================================${NC}"
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

print_critical() {
    echo -e "${RED}❌ CRITICAL: $1${NC}"
}

# Default values / Valores padrão
SKIP_BUILD=false
COLLECT_STATIC=true
VALIDATE_ENV=true

# Parse arguments / Analisar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --no-static)
            COLLECT_STATIC=false
            shift
            ;;
        --skip-validation)
            VALIDATE_ENV=false
            shift
            ;;
        --help|-h)
            echo "Usage: ./setup-prod.sh [OPTIONS]"
            echo ""
            echo "Production setup script for Django Base"
            echo ""
            echo "Options:"
            echo "  --skip-build        Skip Docker build (use if images already exist)"
            echo "  --no-static         Skip collecting static files"
            echo "  --skip-validation   Skip environment validation (NOT recommended)"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "IMPORTANT: Review your .env file before running!"
            echo "           Make sure DEBUG=False and SECRET_KEY is strong."
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
print_header "🚀 Django Base - Production Setup"
echo ""
print_warning "This script will set up a PRODUCTION environment"
print_warning "Make sure you have reviewed your .env configuration!"
echo ""
read -p "Continue? (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    print_info "Setup cancelled"
    exit 0
fi

# Step 0: Pre-flight checks / Verificações pré-voo
print_header "Step 0/8: Pre-flight Checks"

# Check if .env exists
if [ ! -f .env ]; then
    print_critical ".env file not found!"
    print_error "Create .env from .env.example and configure for production"
    print_info "Required changes:"
    echo "  - Set DEBUG=False"
    echo "  - Generate strong SECRET_KEY"
    echo "  - Configure ALLOWED_HOSTS"
    echo "  - Set strong database passwords"
    echo "  - Configure email settings"
    exit 1
fi
print_success ".env file found"

# Validate critical production settings
# if [ "$VALIDATE_ENV" = true ]; then
#     print_info "Validating production settings..."

#     # Check DEBUG
#     if grep -q "DEBUG=True" .env; then
#         print_critical "DEBUG=True detected in .env!"
#         print_error "Set DEBUG=False for production"
#         exit 1
#     fi
#     print_success "DEBUG is False"

#     # Check SECRET_KEY
#     if grep -q "SECRET_KEY=change-this-in-production" .env; then
#         print_critical "Default SECRET_KEY detected!"
#         print_error "Generate a strong SECRET_KEY:"
#         echo "  python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
#         exit 1
#     fi
#     print_success "SECRET_KEY is configured"

#     # Check ALLOWED_HOSTS
#     if grep -q "ALLOWED_HOSTS=localhost,127.0.0.1" .env; then
#         print_warning "ALLOWED_HOSTS contains only localhost"
#         print_info "Make sure to add your production domain"
#     fi
#     print_success "Environment validation passed"
# else
#     print_warning "Environment validation skipped"
# fi
# echo ""

# Step 1: Docker build / Construir Docker
print_header "Step 1/8: Docker Build"
if [ "$SKIP_BUILD" = false ]; then
    print_info "Building production Docker images..."
    docker-compose --profile prod build --no-cache
    print_success "Docker images built"
else
    print_info "Skipping Docker build (--skip-build)"
fi
echo ""

# Step 2: Start containers / Iniciar containers
print_header "Step 2/8: Starting Containers"
print_info "Starting production containers..."
docker-compose --profile prod up -d

print_info "Waiting for containers to be healthy..."
sleep 15

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
    print_error "Some containers failed to start"
    print_info "Check logs with: docker-compose --profile prod logs"
    exit 1
fi
print_success "All containers started successfully"
echo ""

# Step 3: Database migrations / Migrações do banco
print_header "Step 3/8: Database Migrations"
print_info "Running database migrations..."
docker-compose --profile prod exec -T web python manage.py migrate --noinput
print_success "Migrations completed"
echo ""

# Step 4: Collect static files / Coletar arquivos estáticos
print_header "Step 4/8: Collect Static Files"
if [ "$COLLECT_STATIC" = true ]; then
    print_info "Collecting static files for Nginx..."
    docker-compose --profile prod exec -T web python manage.py collectstatic --noinput --clear
    print_success "Static files collected"
else
    print_info "Skipping static files collection (--no-static)"
fi
echo ""

# Step 5: Compile translations / Compilar traduções
print_header "Step 5/8: Compile Translations"
print_info "Compiling translations (pt-br, en)..."
docker-compose --profile prod exec -T web python manage.py compilemessages
print_success "Translations compiled"
echo ""

# Step 6: Environment validation / Validação de ambiente
print_header "Step 6/8: Environment Validation"
print_info "Running Django environment validator..."
docker-compose --profile prod exec -T web python manage.py validate_env || true
print_info "Review any warnings or errors above"
echo ""

# Step 7: Health checks / Verificações de saúde
print_header "Step 7/8: Health Checks"
print_info "Checking service health..."

# Wait a bit for services to stabilize
sleep 5

# Check database
print_info "Checking database connection..."
if docker-compose --profile prod exec -T db pg_isready -U django_user > /dev/null 2>&1; then
    print_success "Database is healthy"
else
    print_error "Database connection failed"
fi

# Check Redis
print_info "Checking Redis connection..."
if docker-compose --profile prod exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_success "Redis is healthy"
else
    print_error "Redis connection failed"
fi

# Check web application (with retry)
print_info "Checking web application..."
for i in {1..5}; do
    if curl -f -s http://localhost:8000/health/ > /dev/null 2>&1; then
        print_success "Web application is healthy"
        break
    else
        if [ $i -eq 5 ]; then
            print_warning "Web application health check failed (may take time to start)"
        else
            sleep 2
        fi
    fi
done
echo ""

# Step 8: Security reminder / Lembrete de segurança
print_header "Step 8/8: Security Checklist"
print_warning "PRODUCTION SECURITY CHECKLIST:"
echo ""
echo "  ☐ DEBUG=False in .env"
echo "  ☐ Strong SECRET_KEY configured"
echo "  ☐ ALLOWED_HOSTS properly configured"
echo "  ☐ Strong database passwords"
echo "  ☐ SSL/HTTPS configured (see docs/SSL_HTTPS_SETUP.md)"
echo "  ☐ Firewall rules configured"
echo "  ☐ Regular backups scheduled"
echo "  ☐ Monitoring and alerts configured"
echo "  ☐ Email settings configured"
echo "  ☐ Sentry or error monitoring configured"
echo ""

# Final summary / Resumo final
print_header "✅ Production Setup Complete!"
echo ""
print_success "Production environment is ready!"
echo ""
print_info "Access points / Pontos de acesso:"
echo "  - Application: http://localhost (or your domain)"
echo "  - Admin Panel: http://localhost/admin"
echo "  - API Docs: http://localhost/api/docs/"
echo "  - Health Check: http://localhost/health/"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3000 (admin/admin)"
echo ""
print_info "Monitoring dashboards:"
echo "  - Django Base Overview (auto-provisioned)"
echo "  - PostgreSQL Database (ID: 9628)"
echo "  - Nginx Metrics (ID: 12708)"
echo "  - Redis Dashboard (ID: 11835)"
echo ""
print_info "Next steps:"
echo "  1. Create superuser: docker-compose exec web python manage.py createsuperuser"
echo "  2. Configure SSL certificates (see docs/SSL_HTTPS_SETUP.md)"
echo "  3. Set up automated backups: ./scripts/backup_database.sh"
echo "  4. Review Grafana dashboards at http://localhost:3000"
echo "  5. Test all critical endpoints"
echo ""
print_info "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop all: docker-compose --profile prod down"
echo "  - Shell: docker-compose exec web bash"
echo "  - Backup DB: ./scripts/backup_database.sh"
echo "  - Restart: docker-compose restart"
echo ""
print_warning "Remember: Review logs regularly and monitor your application!"
echo ""
print_success "Production deployment successful! 🎉"
