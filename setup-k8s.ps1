# Automated Kubernetes setup script for Django Base project (Windows PowerShell)
# Script de configuração automatizada do Kubernetes para projeto Django Base (Windows PowerShell)

param(
    [switch]$Prod,
    [switch]$SkipBuild,
    [switch]$SkipDeploy,
    [switch]$Help
)

# Helper functions / Funções auxiliares
function Write-Header {
    param([string]$Message)
    Write-Host "========================================" -ForegroundColor Green
    Write-Host $Message -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
}

function Write-SuccessMessage {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-ErrorMessage {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-WarningMessage {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-InfoMessage {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

# Show help / Mostrar ajuda
if ($Help) {
    Write-Host "Usage: .\setup-k8s.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Kubernetes setup script for Django Base (Windows PowerShell)"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Prod             Deploy to production environment (default: dev)"
    Write-Host "  -SkipBuild        Skip Docker image build"
    Write-Host "  -SkipDeploy       Only build image, don't deploy to k8s"
    Write-Host "  -Help             Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\setup-k8s.ps1                    # Deploy to dev"
    Write-Host "  .\setup-k8s.ps1 -Prod              # Deploy to production"
    Write-Host "  .\setup-k8s.ps1 -SkipBuild         # Deploy without rebuilding image"
    exit 0
}

# Set environment based on flags
$Environment = if ($Prod) { "prod" } else { "dev" }
$ImageTag = if ($Prod) { "v1.2.0" } else { "dev-latest" }
$BuildImage = -not $SkipBuild

# Main setup / Configuração principal
Write-Header "☸️ Django Base - Kubernetes Setup"
Write-InfoMessage "Environment: $Environment"
Write-InfoMessage "Image Tag: django-base:$ImageTag"
Write-Host ""

# Step 0: Pre-flight checks / Verificações pré-voo
Write-Header "Step 0/6: Pre-flight Checks"

# Check if kubectl is installed
$KubectlCmd = $null
try {
    kubectl.exe version --client 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $KubectlCmd = "kubectl.exe"
        Write-SuccessMessage "kubectl is installed"
    }
} catch {
    try {
        kubectl version --client 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $KubectlCmd = "kubectl"
            Write-SuccessMessage "kubectl is installed"
        }
    } catch {
        Write-ErrorMessage "kubectl not found! Please install kubectl first."
        Write-InfoMessage "Windows: choco install kubernetes-cli"
        Write-InfoMessage "Or download from: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/"
        exit 1
    }
}

if (-not $KubectlCmd) {
    Write-ErrorMessage "kubectl not found! Please install kubectl first."
    Write-InfoMessage "Windows: choco install kubernetes-cli"
    exit 1
}

# Check if kubectl can connect to cluster
try {
    & $KubectlCmd cluster-info 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Cannot connect to cluster"
    }
    Write-SuccessMessage "Connected to Kubernetes cluster"
} catch {
    Write-ErrorMessage "Cannot connect to Kubernetes cluster!"
    Write-InfoMessage "Make sure you have a running cluster (minikube, docker-desktop, etc.)"
    Write-InfoMessage "For minikube: minikube start"
    Write-InfoMessage "For Docker Desktop: Enable Kubernetes in settings"
    exit 1
}

# Check if Docker is running (for image build)
if ($BuildImage) {
    try {
        docker version 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-SuccessMessage "Docker is running"
        } else {
            throw "Docker not running"
        }
    } catch {
        Write-ErrorMessage "Docker is not running!"
        Write-InfoMessage "Please start Docker Desktop and try again"
        Write-InfoMessage "Or use -SkipBuild if you already have the image built"
        exit 1
    }
}

Write-Host ""

# Step 1: Build Docker Image / Construir imagem Docker
Write-Header "Step 1/6: Docker Image Build"

if ($BuildImage) {
    Write-InfoMessage "Building Docker image: django-base:$ImageTag..."

    docker build -t "django-base:$ImageTag" .
    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "Docker build failed"
        exit 1
    }

    # Also tag as latest for the specific environment
    docker tag "django-base:$ImageTag" django-base:latest

    Write-SuccessMessage "Docker image built successfully"
    Write-InfoMessage "Image: django-base:$ImageTag"
} else {
    Write-InfoMessage "Skipping Docker build (-SkipBuild)"
}

Write-Host ""

if ($SkipDeploy) {
    Write-SuccessMessage "Image built successfully! Skipping Kubernetes deployment (-SkipDeploy)"
    exit 0
}

# Step 2: Verify Kustomization / Verificar Kustomization
Write-Header "Step 2/6: Verify Kustomization"

Write-InfoMessage "Verifying kustomization configuration..."

if (Test-Path "k8s\$Environment\kustomization.yaml") {
    Write-SuccessMessage "Kustomization file found for $Environment"
    Write-InfoMessage "Using image: django-base:$ImageTag"
} else {
    Write-ErrorMessage "Kustomization file not found for $Environment!"
    exit 1
}

Write-Host ""

# Step 3: Create/Update Namespace / Criar/Atualizar Namespace
Write-Header "Step 3/6: Namespace Setup"

try {
    & $KubectlCmd get namespace django-base 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-InfoMessage "Namespace 'django-base' already exists"
    } else {
        throw "Namespace not found"
    }
} catch {
    Write-InfoMessage "Creating namespace 'django-base'..."
    & $KubectlCmd create namespace django-base
    if ($LASTEXITCODE -eq 0) {
        Write-SuccessMessage "Namespace created"
    } else {
        Write-ErrorMessage "Failed to create namespace"
        exit 1
    }
}

Write-Host ""

# Step 4: Deploy to Kubernetes / Deploy no Kubernetes
Write-Header "Step 4/6: Kubernetes Deployment"

Write-InfoMessage "Applying Kubernetes manifests for $Environment environment..."

& $KubectlCmd apply -k "k8s\$Environment\"
if ($LASTEXITCODE -eq 0) {
    Write-SuccessMessage "Kubernetes resources created/updated"
} else {
    Write-ErrorMessage "Failed to apply Kubernetes manifests"
    exit 1
}

Write-Host ""

# Step 5: Wait for deployments / Aguardar deployments
Write-Header "Step 5/6: Wait for Deployments"

Write-InfoMessage "Deployments are starting... This may take a few minutes on first run."
Write-InfoMessage "Kubernetes is pulling Docker images and creating volumes..."
Write-Host ""

Write-InfoMessage "Waiting for PostgreSQL to be ready (timeout: 5 minutes)..."
try {
    & $KubectlCmd wait --for=condition=available --timeout=300s "deployment/$Environment-postgres" -n django-base 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-SuccessMessage "PostgreSQL is ready"
    } else {
        Write-WarningMessage "PostgreSQL deployment timeout - check status with: kubectl get pods -n django-base"
    }
} catch {
    Write-WarningMessage "PostgreSQL deployment timeout - check status with: kubectl get pods -n django-base"
}

Write-InfoMessage "Waiting for Redis to be ready (timeout: 3 minutes)..."
try {
    & $KubectlCmd wait --for=condition=available --timeout=180s "deployment/$Environment-redis" -n django-base 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-SuccessMessage "Redis is ready"
    } else {
        Write-WarningMessage "Redis deployment timeout - check status with: kubectl get pods -n django-base"
    }
} catch {
    Write-WarningMessage "Redis deployment timeout - check status with: kubectl get pods -n django-base"
}

Write-InfoMessage "Waiting for Django to be ready (timeout: 5 minutes)..."
try {
    & $KubectlCmd wait --for=condition=available --timeout=300s "deployment/$Environment-django-web" -n django-base 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-SuccessMessage "Django is ready"
    } else {
        Write-WarningMessage "Django deployment timeout - check status with: kubectl get pods -n django-base"
    }
} catch {
    Write-WarningMessage "Django deployment timeout - check status with: kubectl get pods -n django-base"
}

Write-Host ""
Write-InfoMessage "Note: If timeouts occurred, pods may still be starting. Check their status with:"
Write-InfoMessage "kubectl get pods -n django-base -w"

Write-Host ""

# Step 6: Post-deployment info / Informações pós-deployment
Write-Header "Step 6/6: Deployment Information"

Write-Host ""
Write-SuccessMessage "Kubernetes deployment initiated successfully!"
Write-Host ""

Write-InfoMessage "Deployment summary / Resumo do deployment:"
Write-Host "  - Environment: $Environment"
Write-Host "  - Namespace: django-base"
Write-Host "  - Image: django-base:$ImageTag"
Write-Host ""

Write-InfoMessage "Check deployment status / Verificar status do deployment:"
Write-Host "  kubectl get all -n django-base"
Write-Host "  kubectl get pods -n django-base -w"
Write-Host ""

Write-InfoMessage "View logs / Ver logs:"
Write-Host "  kubectl logs -n django-base -l app=django,component=web --tail=50 -f"
Write-Host ""

# Final summary / Resumo final
Write-Header "✅ Kubernetes Setup Complete!"
Write-Host ""

Write-InfoMessage "Access application / Acessar aplicação:"
Write-Host "  # Port forward to localhost"
Write-Host "  kubectl port-forward -n django-base svc/$Environment-nginx-service 8000:80"
Write-Host ""
Write-Host "  # Then access / Depois acesse: http://localhost:8000"
Write-Host ""

# Check if minikube is available
try {
    minikube version 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        minikube status 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-InfoMessage "Minikube detected / Minikube detectado:"
            Write-Host "  minikube service $Environment-nginx-service -n django-base"
            Write-Host ""
        }
    }
} catch {
    # Minikube not available, skip
}

Write-InfoMessage "Common operations / Operações comuns:"
Write-Host "  # Create superuser / Criar superusuário"
Write-Host "  kubectl exec -it -n django-base deployment/$Environment-django-web -- /app/.venv/bin/python manage.py createsuperuser"
Write-Host ""
Write-Host "  # Run migrations / Executar migrações"
Write-Host "  kubectl exec -it -n django-base deployment/$Environment-django-web -- /app/.venv/bin/python manage.py migrate"
Write-Host ""
Write-Host "  # Shell access / Acesso ao shell"
Write-Host "  kubectl exec -it -n django-base deployment/$Environment-django-web -- /bin/sh"
Write-Host ""

Write-InfoMessage "Cleanup / Limpeza:"
Write-Host "  # Delete all resources / Deletar todos os recursos"
Write-Host "  kubectl delete namespace django-base"
Write-Host ""
Write-Host "  # Or delete specific environment / Ou deletar ambiente específico"
Write-Host "  kubectl delete -k k8s\$Environment\"
Write-Host ""

Write-InfoMessage "Next steps / Próximos passos:"
Write-Host "  1. Wait for all pods to be Running (kubectl get pods -n django-base -w)"
Write-Host "  2. Port forward to access the application"
Write-Host "  3. Create a superuser for Django admin"
Write-Host "  4. Check the k8s\README.md for troubleshooting"
Write-Host ""

Write-SuccessMessage "Happy deploying! ☸️ / Bom deploy! ☸️"
