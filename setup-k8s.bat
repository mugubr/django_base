@echo off
REM Automated Kubernetes setup script for Django Base project (Windows)
REM Script de configuração automatizada do Kubernetes para projeto Django Base (Windows)

setlocal enabledelayedexpansion

REM Default values / Valores padrão
set ENVIRONMENT=dev
set IMAGE_TAG=dev-latest
set BUILD_IMAGE=true
set SKIP_DEPLOY=false

REM Parse arguments / Processar argumentos
:parse_args
if "%~1"=="" goto start_setup
if /i "%~1"=="--prod" (
    set ENVIRONMENT=prod
    set IMAGE_TAG=v1.2.0
    shift
    goto parse_args
)
if /i "%~1"=="--skip-build" (
    set BUILD_IMAGE=false
    shift
    goto parse_args
)
if /i "%~1"=="--skip-deploy" (
    set SKIP_DEPLOY=true
    shift
    goto parse_args
)
if /i "%~1"=="--help" goto show_help

echo Unknown option: %~1
echo Use --help for usage information
exit /b 1

:show_help
echo Usage: setup-k8s.bat [OPTIONS]
echo.
echo Kubernetes setup script for Django Base (Windows)
echo.
echo Options:
echo   --prod            Deploy to production environment (default: dev)
echo   --skip-build      Skip Docker image build
echo   --skip-deploy     Only build image, don't deploy to k8s
echo   --help            Show this help message
echo.
echo Examples:
echo   setup-k8s.bat                    # Deploy to dev
echo   setup-k8s.bat --prod             # Deploy to production
echo   setup-k8s.bat --skip-build       # Deploy without rebuilding image
exit /b 0

:start_setup
echo ========================================
echo Django Base - Kubernetes Setup
echo ========================================
echo Environment: %ENVIRONMENT%
echo Image Tag: django-base:%IMAGE_TAG%
echo.

REM Step 0: Pre-flight checks
echo ========================================
echo Step 0/6: Pre-flight Checks
echo ========================================

REM Check if kubectl is installed
set KUBECTL_CMD=kubectl.exe
kubectl.exe version --client >nul 2>&1
if errorlevel 1 (
    set KUBECTL_CMD=kubectl
    kubectl version --client >nul 2>&1
    if errorlevel 1 (
        echo ERROR: kubectl not found! Please install kubectl first.
        echo Windows: choco install kubernetes-cli
        echo Or download from: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
        exit /b 1
    )
)
echo OK: kubectl is installed

REM Check if kubectl can connect to cluster
%KUBECTL_CMD% cluster-info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot connect to Kubernetes cluster!
    echo Make sure you have a running cluster (minikube, docker-desktop, etc.)
    echo For minikube: minikube start
    echo For Docker Desktop: Enable Kubernetes in settings
    exit /b 1
)
echo OK: Connected to Kubernetes cluster

REM Check if Docker is running (for image build)
if "%BUILD_IMAGE%"=="true" (
    docker version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Docker is not running!
        echo Please start Docker Desktop and try again
        echo Or use --skip-build if you already have the image built
        exit /b 1
    )
    echo OK: Docker is running
)

echo.

REM Step 1: Build Docker Image
echo ========================================
echo Step 1/6: Docker Image Build
echo ========================================

if "%BUILD_IMAGE%"=="true" (
    echo Building Docker image: django-base:%IMAGE_TAG%...
    docker build -t django-base:%IMAGE_TAG% .
    if errorlevel 1 (
        echo ERROR: Docker build failed
        exit /b 1
    )

    REM Also tag as latest for the specific environment
    docker tag django-base:%IMAGE_TAG% django-base:latest

    echo OK: Docker image built successfully
    echo Image: django-base:%IMAGE_TAG%
) else (
    echo Skipping Docker build (--skip-build)
)

echo.

if "%SKIP_DEPLOY%"=="true" (
    echo OK: Image built successfully! Skipping Kubernetes deployment (--skip-deploy)
    exit /b 0
)

REM Step 2: Verify Kustomization
echo ========================================
echo Step 2/6: Verify Kustomization
echo ========================================

echo Verifying kustomization configuration...

if exist k8s\%ENVIRONMENT%\kustomization.yaml (
    echo OK: Kustomization file found for %ENVIRONMENT%
    echo Using image: django-base:%IMAGE_TAG%
) else (
    echo ERROR: Kustomization file not found for %ENVIRONMENT%!
    exit /b 1
)

echo.

REM Step 3: Create/Update Namespace
echo ========================================
echo Step 3/6: Namespace Setup
echo ========================================

%KUBECTL_CMD% get namespace django-base >nul 2>&1
if errorlevel 1 (
    echo Creating namespace 'django-base'...
    %KUBECTL_CMD% create namespace django-base
    if errorlevel 1 (
        echo ERROR: Failed to create namespace
        exit /b 1
    )
    echo OK: Namespace created
) else (
    echo Namespace 'django-base' already exists
)

echo.

REM Step 4: Deploy to Kubernetes
echo ========================================
echo Step 4/6: Kubernetes Deployment
echo ========================================

echo Applying Kubernetes manifests for %ENVIRONMENT% environment...

%KUBECTL_CMD% apply -k k8s\%ENVIRONMENT%\
if errorlevel 1 (
    echo ERROR: Failed to apply Kubernetes manifests
    exit /b 1
)
echo OK: Kubernetes resources created/updated

echo.

REM Step 5: Wait for deployments
echo ========================================
echo Step 5/6: Wait for Deployments
echo ========================================

echo Deployments are starting... This may take a few minutes on first run.
echo Kubernetes is pulling Docker images and creating volumes...
echo.

echo Waiting for PostgreSQL to be ready (timeout: 5 minutes)...
%KUBECTL_CMD% wait --for=condition=available --timeout=300s deployment/%ENVIRONMENT%-postgres -n django-base >nul 2>&1
if errorlevel 1 (
    echo WARNING: PostgreSQL deployment timeout - check status with: kubectl get pods -n django-base
) else (
    echo OK: PostgreSQL is ready
)

echo Waiting for Redis to be ready (timeout: 3 minutes)...
%KUBECTL_CMD% wait --for=condition=available --timeout=180s deployment/%ENVIRONMENT%-redis -n django-base >nul 2>&1
if errorlevel 1 (
    echo WARNING: Redis deployment timeout - check status with: kubectl get pods -n django-base
) else (
    echo OK: Redis is ready
)

echo Waiting for Django to be ready (timeout: 5 minutes)...
%KUBECTL_CMD% wait --for=condition=available --timeout=300s deployment/%ENVIRONMENT%-django-web -n django-base >nul 2>&1
if errorlevel 1 (
    echo WARNING: Django deployment timeout - check status with: kubectl get pods -n django-base
) else (
    echo OK: Django is ready
)

echo.
echo Note: If timeouts occurred, pods may still be starting. Check their status with:
echo kubectl get pods -n django-base -w

echo.

REM Step 6: Post-deployment info
echo ========================================
echo Step 6/6: Deployment Information
echo ========================================

echo.
echo OK: Kubernetes deployment initiated successfully!
echo.

echo Deployment summary / Resumo do deployment:
echo   - Environment: %ENVIRONMENT%
echo   - Namespace: django-base
echo   - Image: django-base:%IMAGE_TAG%
echo.

echo Check deployment status / Verificar status do deployment:
echo   kubectl get all -n django-base
echo   kubectl get pods -n django-base -w
echo.

echo View logs / Ver logs:
echo   kubectl logs -n django-base -l app=django,component=web --tail=50 -f
echo.

REM Final summary
echo ========================================
echo Kubernetes Setup Complete!
echo ========================================
echo.

echo Access application / Acessar aplicação:
echo   # Port forward to localhost
echo   kubectl port-forward -n django-base svc/%ENVIRONMENT%-nginx-service 8000:80
echo.
echo   # Then access / Depois acesse: http://localhost:8000
echo.

REM Check if minikube is available
minikube version >nul 2>&1
if not errorlevel 1 (
    minikube status >nul 2>&1
    if not errorlevel 1 (
        echo Minikube detected / Minikube detectado:
        echo   minikube service %ENVIRONMENT%-nginx-service -n django-base
        echo.
    )
)

echo Common operations / Operações comuns:
echo   # Create superuser / Criar superusuário
echo   kubectl exec -it -n django-base deployment/%ENVIRONMENT%-django-web -- /app/.venv/bin/python manage.py createsuperuser
echo.
echo   # Run migrations / Executar migrações
echo   kubectl exec -it -n django-base deployment/%ENVIRONMENT%-django-web -- /app/.venv/bin/python manage.py migrate
echo.
echo   # Shell access / Acesso ao shell
echo   kubectl exec -it -n django-base deployment/%ENVIRONMENT%-django-web -- /bin/sh
echo.

echo Cleanup / Limpeza:
echo   # Delete all resources / Deletar todos os recursos
echo   kubectl delete namespace django-base
echo.
echo   # Or delete specific environment / Ou deletar ambiente específico
echo   kubectl delete -k k8s\%ENVIRONMENT%\
echo.

echo Next steps / Próximos passos:
echo   1. Wait for all pods to be Running (kubectl get pods -n django-base -w)
echo   2. Port forward to access the application
echo   3. Create a superuser for Django admin
echo   4. Check the k8s\README.md for troubleshooting
echo.

echo Happy deploying! / Bom deploy!

endlocal
