#!/bin/bash
# Automated Kubernetes setup script for Django Base project
# Script de configuração automatizada do Kubernetes para projeto Django Base

set -e

# Colors - GREEN for Kubernetes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions / Funções auxiliares
print_header() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}========================================${NC}"
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
    echo -e "${GREEN}ℹ $1${NC}"
}

# Default values / Valores padrão
ENVIRONMENT="dev"
IMAGE_TAG="dev-latest"
BUILD_IMAGE=true
SKIP_DEPLOY=false

# Parse arguments / Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --prod)
            ENVIRONMENT="prod"
            IMAGE_TAG="v1.2.0"
            shift
            ;;
        --skip-build)
            BUILD_IMAGE=false
            shift
            ;;
        --skip-deploy)
            SKIP_DEPLOY=true
            shift
            ;;
        --help)
            echo "Usage: ./setup-k8s.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --prod            Deploy to production environment (default: dev)"
            echo "  --skip-build      Skip Docker image build"
            echo "  --skip-deploy     Only build image, don't deploy to k8s"
            echo "  --help            Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./setup-k8s.sh                    # Deploy to dev"
            echo "  ./setup-k8s.sh --prod             # Deploy to production"
            echo "  ./setup-k8s.sh --skip-build       # Deploy without rebuilding image"
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
print_header "☸️ Django Base - Kubernetes Setup"
print_info "Environment: $ENVIRONMENT"
print_info "Image Tag: django-base:$IMAGE_TAG"
echo ""

# Step 0: Pre-flight checks / Verificações pré-voo
print_header "Step 0/6: Pre-flight Checks"

# Check if kubectl is installed (Windows compatible)
# Add common Windows paths to PATH first
export PATH="/c/ProgramData/chocolatey/bin:/c/Program Files/Docker/Docker/resources/bin:$PATH"

# Determine which kubectl command to use (with or without .exe)
KUBECTL_CMD="kubectl"
if kubectl.exe version --client >/dev/null 2>&1; then
    KUBECTL_CMD="kubectl.exe"
    print_success "kubectl is installed"
elif kubectl version --client >/dev/null 2>&1; then
    KUBECTL_CMD="kubectl"
    print_success "kubectl is installed"
else
    print_error "kubectl not found! Please install kubectl first."
    print_info "Windows: choco install kubernetes-cli"
    print_info "Linux: sudo apt-get install kubectl"
    print_info "Mac: brew install kubectl"
    exit 1
fi

# Check if kubectl can connect to cluster
if ! $KUBECTL_CMD cluster-info > /dev/null 2>&1; then
    print_error "Cannot connect to Kubernetes cluster!"
    print_info "Make sure you have a running cluster (minikube, docker-desktop, etc.)"
    print_info "For minikube: minikube start"
    print_info "For Docker Desktop: Enable Kubernetes in settings"
    exit 1
fi
print_success "Connected to Kubernetes cluster"

# Check if Docker is running (for image build)
if [ "$BUILD_IMAGE" = true ]; then
    # Determine which docker command to use (with or without .exe)
    DOCKER_CMD="docker"
    if docker.exe info > /dev/null 2>&1; then
        DOCKER_CMD="docker.exe"
        print_success "Docker is running"
    elif docker info > /dev/null 2>&1; then
        DOCKER_CMD="docker"
        print_success "Docker is running"
    else
        print_error "Docker is not running!"
        print_info "Please start Docker Desktop and try again"
        print_info "Or use --skip-build if you already have the image built"
        exit 1
    fi
fi

echo ""

# Step 1: Build Docker Image / Construir imagem Docker
print_header "Step 1/6: Docker Image Build"

if [ "$BUILD_IMAGE" = true ]; then
    print_info "Building Docker image: django-base:$IMAGE_TAG..."

    $DOCKER_CMD build -t django-base:$IMAGE_TAG .

    # Also tag as latest for the specific environment
    $DOCKER_CMD tag django-base:$IMAGE_TAG django-base:latest

    print_success "Docker image built successfully"
    print_info "Image: django-base:$IMAGE_TAG"
else
    print_info "Skipping Docker build (--skip-build)"
fi

echo ""

if [ "$SKIP_DEPLOY" = true ]; then
    print_success "Image built successfully! Skipping Kubernetes deployment (--skip-deploy)"
    exit 0
fi

# Step 2: Verify Kustomization / Verificar Kustomization
print_header "Step 2/6: Verify Kustomization"

print_info "Verifying kustomization configuration..."

# Just verify the file exists, don't try to modify it (sed doesn't work well on Windows)
if [ -f "k8s/$ENVIRONMENT/kustomization.yaml" ]; then
    print_success "Kustomization file found for $ENVIRONMENT"
    print_info "Using image: django-base:$IMAGE_TAG"
else
    print_error "Kustomization file not found for $ENVIRONMENT!"
    exit 1
fi

echo ""

# Step 3: Create/Update Namespace / Criar/Atualizar Namespace
print_header "Step 3/6: Namespace Setup"

if $KUBECTL_CMD get namespace django-base > /dev/null 2>&1; then
    print_info "Namespace 'django-base' already exists"
else
    print_info "Creating namespace 'django-base'..."
    $KUBECTL_CMD create namespace django-base
    print_success "Namespace created"
fi

echo ""

# Step 4: Deploy to Kubernetes / Deploy no Kubernetes
print_header "Step 4/6: Kubernetes Deployment"

print_info "Applying Kubernetes manifests for $ENVIRONMENT environment..."

# Apply the kustomization
$KUBECTL_CMD apply -k k8s/$ENVIRONMENT/

print_success "Kubernetes resources created/updated"

echo ""

# Step 5: Wait for deployments / Aguardar deployments
print_header "Step 5/6: Wait for Deployments"

print_info "Deployments are starting... This may take a few minutes on first run."
print_info "Kubernetes is pulling Docker images and creating volumes..."
echo ""

print_info "Waiting for PostgreSQL to be ready (timeout: 5 minutes)..."
if $KUBECTL_CMD wait --for=condition=available --timeout=300s deployment/$ENVIRONMENT-postgres -n django-base 2>/dev/null; then
    print_success "PostgreSQL is ready"
else
    print_warning "PostgreSQL deployment timeout - check status with: kubectl get pods -n django-base"
fi

print_info "Waiting for Redis to be ready (timeout: 3 minutes)..."
if $KUBECTL_CMD wait --for=condition=available --timeout=180s deployment/$ENVIRONMENT-redis -n django-base 2>/dev/null; then
    print_success "Redis is ready"
else
    print_warning "Redis deployment timeout - check status with: kubectl get pods -n django-base"
fi

print_info "Waiting for Django to be ready (timeout: 5 minutes)..."
if $KUBECTL_CMD wait --for=condition=available --timeout=300s deployment/$ENVIRONMENT-django-web -n django-base 2>/dev/null; then
    print_success "Django is ready"
else
    print_warning "Django deployment timeout - check status with: kubectl get pods -n django-base"
fi

echo ""
print_info "Note: If timeouts occurred, pods may still be starting. Check their status with:"
print_info "kubectl get pods -n django-base -w"

echo ""

# Step 6: Post-deployment info / Informações pós-deployment
print_header "Step 6/6: Deployment Information"

echo ""
print_success "Kubernetes deployment initiated successfully!"
echo ""

print_info "Deployment summary / Resumo do deployment:"
echo "  - Environment: $ENVIRONMENT"
echo "  - Namespace: django-base"
echo "  - Image: django-base:$IMAGE_TAG"
echo ""

print_info "Check deployment status / Verificar status do deployment:"
echo "  kubectl get all -n django-base"
echo "  kubectl get pods -n django-base -w"
echo ""

print_info "View logs / Ver logs:"
echo "  kubectl logs -n django-base -l app=django,component=web --tail=50 -f"
echo ""

# Final summary / Resumo final
print_header "✅ Kubernetes Setup Complete!"
echo ""

print_info "Access application / Acessar aplicação:"
echo "  # Port forward to localhost"
echo "  kubectl port-forward -n django-base svc/$ENVIRONMENT-nginx-service 8000:80"
echo ""
echo "  # Then access / Depois acesse: http://localhost:8000"
echo ""

if minikube version > /dev/null 2>&1; then
    if minikube status > /dev/null 2>&1; then
        print_info "Minikube detected / Minikube detectado:"
        echo "  minikube service $ENVIRONMENT-nginx-service -n django-base"
        echo ""
    fi
fi

print_info "Common operations / Operações comuns:"
echo "  # Create superuser / Criar superusuário"
echo "  kubectl exec -it -n django-base deployment/$ENVIRONMENT-django-web -- /app/.venv/bin/python manage.py createsuperuser"
echo ""
echo "  # Run migrations / Executar migrações"
echo "  kubectl exec -it -n django-base deployment/$ENVIRONMENT-django-web -- /app/.venv/bin/python manage.py migrate"
echo ""
echo "  # Shell access / Acesso ao shell"
echo "  kubectl exec -it -n django-base deployment/$ENVIRONMENT-django-web -- /bin/sh"
echo ""

print_info "Quick commands / Comandos rápidos:"
echo "  - View status: make k8s-status"
echo "  - View logs: make k8s-logs"
echo "  - Port forward: make k8s-port-forward"
echo "  - Shell access: make k8s-shell"
echo "  - Create superuser: make k8s-migrate"
echo ""

print_info "Cleanup / Limpeza:"
echo "  # Delete all resources / Deletar todos os recursos"
echo "  kubectl delete namespace django-base"
echo ""
echo "  # Or delete specific environment / Ou deletar ambiente específico"
echo "  kubectl delete -k k8s/$ENVIRONMENT/"
echo ""

print_info "Next steps / Próximos passos:"
echo "  1. Wait for all pods to be Running (kubectl get pods -n django-base -w)"
echo "  2. Port forward to access the application"
echo "  3. Create a superuser for Django admin"
echo "  4. Check the k8s/README.md for troubleshooting"
echo ""

print_success "Happy deploying! ☸️ / Bom deploy! ☸️"
