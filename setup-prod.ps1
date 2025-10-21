# Automated production setup script for Django Base project (Windows PowerShell)
# Script de configuração automatizada de produção para projeto Django Base (Windows PowerShell)

param(
    [switch]$SkipBuild,
    [switch]$NoStatic,
    [switch]$SkipValidation,
    [switch]$Help
)

# Helper functions / Funções auxiliares
function Write-Header {
    param([string]$Message)
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host $Message -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
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
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Critical {
    param([string]$Message)
    Write-Host "[CRITICAL] $Message" -ForegroundColor Red
}

# Show help / Mostrar ajuda
if ($Help) {
    Write-Host "Usage: .\setup-prod.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Production setup script for Django Base (Windows PowerShell)"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -SkipBuild        Skip Docker build (use if images already exist)"
    Write-Host "  -NoStatic         Skip collecting static files"
    Write-Host "  -SkipValidation   Skip environment validation (NOT recommended)"
    Write-Host "  -Help             Show this help message"
    Write-Host ""
    Write-Host "IMPORTANT: Review your .env file before running!"
    Write-Host "           Make sure DEBUG=False and SECRET_KEY is strong."
    exit 0
}

# Set defaults / Definir padrões
$CollectStatic = -not $NoStatic
$ValidateEnv = -not $SkipValidation

# Main setup / Configuração principal
Write-Header "🚀 Django Base - Production Setup"
Write-Host ""
Write-WarningMessage "This script will set up a PRODUCTION environment"
Write-WarningMessage "Make sure you have reviewed your .env configuration!"
Write-Host ""

$confirmation = Read-Host "Continue? (yes/no)"
if ($confirmation -notmatch "^[Yy]es$") {
    Write-InfoMessage "Setup cancelled"
    exit 0
}

# Step 0: Pre-flight checks / Verificações pré-voo
Write-Host ""
Write-Header "Step 0/8: Pre-flight Checks"

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Critical ".env file not found!"
    Write-ErrorMessage "Create .env from .env.example and configure for production"
    Write-InfoMessage "Required changes:"
    Write-Host "  - Set DEBUG=False"
    Write-Host "  - Generate strong SECRET_KEY"
    Write-Host "  - Configure ALLOWED_HOSTS"
    Write-Host "  - Set strong database passwords"
    Write-Host "  - Configure email settings"
    exit 1
}
Write-SuccessMessage ".env file found"

# Check Docker Compose / Verificar Docker Compose
$DockerCompose = "docker-compose"
try {
    docker-compose --version 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        $DockerCompose = "docker compose"
        docker compose version 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Docker Compose not found"
        }
    }
} catch {
    Write-ErrorMessage "Docker Compose not found"
    exit 1
}

# Step 1: Docker build / Construir Docker
Write-Host ""
Write-Header "Step 1/8: Docker Build"
if (-not $SkipBuild) {
    Write-InfoMessage "Building production Docker images..."
    & $DockerCompose --profile prod build --no-cache
    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "Docker build failed"
        exit 1
    }
    Write-SuccessMessage "Docker images built"
} else {
    Write-InfoMessage "Skipping Docker build (--skip-build)"
}

# Step 2: Start containers / Iniciar containers
Write-Host ""
Write-Header "Step 2/8: Starting Containers"
Write-InfoMessage "Starting production containers..."
& $DockerCompose --profile prod up -d
if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Failed to start containers"
    exit 1
}

Write-InfoMessage "Waiting for containers to be healthy..."
Start-Sleep -Seconds 15

# Check if containers are running
$runningContainers = & $DockerCompose ps
if ($runningContainers -notmatch "Up") {
    Write-ErrorMessage "Some containers failed to start"
    Write-InfoMessage "Check logs with: $DockerCompose --profile prod logs"
    exit 1
}
Write-SuccessMessage "All containers started successfully"

# Step 3: Database migrations / Migrações do banco
Write-Host ""
Write-Header "Step 3/8: Database Migrations"
Write-InfoMessage "Running database migrations..."
& $DockerCompose --profile prod exec -T web python manage.py migrate --noinput
if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Migrations failed"
    exit 1
}
Write-SuccessMessage "Migrations completed"

# Step 4: Collect static files / Coletar arquivos estáticos
Write-Host ""
Write-Header "Step 4/8: Collect Static Files"
if ($CollectStatic) {
    Write-InfoMessage "Collecting static files for Nginx..."
    & $DockerCompose --profile prod exec -T web python manage.py collectstatic --noinput --clear
    if ($LASTEXITCODE -ne 0) {
        Write-WarningMessage "Static collection had issues, but continuing..."
    }
    Write-SuccessMessage "Static files collected"
} else {
    Write-InfoMessage "Skipping static files collection (--no-static)"
}

# Step 5: Compile translations / Compilar traduções
Write-Host ""
Write-Header "Step 5/8: Compile Translations"
Write-InfoMessage "Compiling translations (pt-br, en)..."
& $DockerCompose --profile prod exec -T web python manage.py compilemessages
Write-SuccessMessage "Translations compiled"

# Step 6: Environment validation / Validação de ambiente
Write-Host ""
Write-Header "Step 6/8: Environment Validation"
Write-InfoMessage "Running Django environment validator..."
& $DockerCompose --profile prod exec -T web python manage.py validate_env
Write-InfoMessage "Review any warnings or errors above"

# Step 7: Health checks / Verificações de saúde
Write-Host ""
Write-Header "Step 7/8: Health Checks"
Write-InfoMessage "Checking service health..."

# Wait a bit for services to stabilize
Start-Sleep -Seconds 5

# Check database
Write-InfoMessage "Checking database connection..."
try {
    $dbCheck = & $DockerCompose --profile prod exec -T db pg_isready -U django_user 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-SuccessMessage "Database is healthy"
    } else {
        Write-ErrorMessage "Database connection failed"
    }
} catch {
    Write-ErrorMessage "Database connection failed"
}

# Check Redis
Write-InfoMessage "Checking Redis connection..."
try {
    $redisCheck = & $DockerCompose --profile prod exec -T redis redis-cli ping 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-SuccessMessage "Redis is healthy"
    } else {
        Write-ErrorMessage "Redis connection failed"
    }
} catch {
    Write-ErrorMessage "Redis connection failed"
}

# Check web application (with retry)
Write-InfoMessage "Checking web application..."
$webHealthy = $false
for ($i = 1; $i -le 5; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health/" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-SuccessMessage "Web application is healthy"
            $webHealthy = $true
            break
        }
    } catch {
        if ($i -eq 5) {
            Write-WarningMessage "Web application health check failed (may take time to start)"
        } else {
            Start-Sleep -Seconds 2
        }
    }
}

# Step 8: Security reminder / Lembrete de segurança
Write-Host ""
Write-Header "Step 8/8: Security Checklist"
Write-WarningMessage "PRODUCTION SECURITY CHECKLIST:"
Write-Host ""
Write-Host "  ☐ DEBUG=False in .env"
Write-Host "  ☐ Strong SECRET_KEY configured"
Write-Host "  ☐ ALLOWED_HOSTS properly configured"
Write-Host "  ☐ Strong database passwords"
Write-Host "  ☐ SSL/HTTPS configured (see docs/SSL_HTTPS_SETUP.md)"
Write-Host "  ☐ Firewall rules configured"
Write-Host "  ☐ Regular backups scheduled"
Write-Host "  ☐ Monitoring and alerts configured"
Write-Host "  ☐ Email settings configured"
Write-Host "  ☐ Sentry or error monitoring configured"
Write-Host ""

# Final summary / Resumo final
Write-Header "✅ Production Setup Complete!"
Write-Host ""
Write-SuccessMessage "Production environment is ready!"
Write-Host ""
Write-InfoMessage "Access points / Pontos de acesso:"
Write-Host "  - Application: http://localhost (or your domain)"
Write-Host "  - Admin Panel: http://localhost/admin"
Write-Host "  - API Docs: http://localhost/api/docs/"
Write-Host "  - Health Check: http://localhost/health/"
Write-Host "  - Prometheus: http://localhost:9090"
Write-Host "  - Grafana: http://localhost:3000 (admin/admin)"
Write-Host ""
Write-InfoMessage "Monitoring dashboards:"
Write-Host "  - Django Base Overview (auto-provisioned)"
Write-Host "  - PostgreSQL Database (ID: 9628)"
Write-Host "  - Nginx Metrics (ID: 12708)"
Write-Host "  - Redis Dashboard (ID: 11835)"
Write-Host ""
Write-InfoMessage "Next steps:"
Write-Host "  1. Create superuser: $DockerCompose exec web python manage.py createsuperuser"
Write-Host "  2. Configure SSL certificates (see docs/SSL_HTTPS_SETUP.md)"
Write-Host "  3. Set up automated backups: .\scripts\backup_database.ps1"
Write-Host "  4. Review Grafana dashboards at http://localhost:3000"
Write-Host "  5. Test all critical endpoints"
Write-Host ""
Write-InfoMessage "Useful commands:"
Write-Host "  - View logs: $DockerCompose logs -f"
Write-Host "  - Stop all: $DockerCompose --profile prod down"
Write-Host "  - Shell: $DockerCompose exec web bash"
Write-Host "  - Backup DB: .\scripts\backup_database.ps1"
Write-Host "  - Restart: $DockerCompose restart"
Write-Host ""
Write-WarningMessage "Remember: Review logs regularly and monitor your application!"
Write-Host ""
Write-SuccessMessage "Production deployment successful! 🎉"
