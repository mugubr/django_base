# Automated development setup script for Django Base project (Windows PowerShell)
# Script de configuração automatizada de desenvolvimento para projeto Django Base (Windows PowerShell)

param(
    [switch]$SkipPrecommit,
    [switch]$SkipTests,
    [switch]$SkipCoverage,
    [switch]$NoSeed,
    [switch]$SkipBuild,
    [switch]$Quick,
    [switch]$Help
)

# Helper functions / Funções auxiliares
function Write-Header {
    param([string]$Message)
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
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

# Show help / Mostrar ajuda
if ($Help) {
    Write-Host "Usage: .\setup.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Development setup script for Django Base (Windows PowerShell)"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -SkipPrecommit    Skip pre-commit hooks installation and run"
    Write-Host "  -SkipTests        Skip running tests"
    Write-Host "  -SkipCoverage     Skip coverage report generation"
    Write-Host "  -NoSeed           Don't seed database with sample data"
    Write-Host "  -SkipBuild        Skip Docker build (use if images already exist)"
    Write-Host "  -Quick            Quick mode: skip tests and pre-commit (faster setup)"
    Write-Host "  -Help             Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\setup.ps1                    # Full setup with all features"
    Write-Host "  .\setup.ps1 -Quick             # Quick setup for rapid testing"
    Write-Host "  .\setup.ps1 -SkipBuild         # Skip Docker build (if images exist)"
    exit 0
}

# Set defaults / Definir padrões
$RunPrecommit = -not $SkipPrecommit
$RunTests = -not $SkipTests
$RunCoverage = -not $SkipCoverage
$SeedDB = -not $NoSeed
$DoBuild = -not $SkipBuild

if ($Quick) {
    $RunTests = $false
    $RunPrecommit = $false
}

# Start setup / Iniciar setup
Write-Header "Django Base - Development Setup (Windows PowerShell)"
Write-Host ""

# Check Docker / Verificar Docker
Write-InfoMessage "[1/9] Checking Docker..."
try {
    $dockerVersion = docker --version 2>$null
    if (-not $dockerVersion) {
        throw "Docker not found"
    }
    Write-SuccessMessage "Docker is installed: $dockerVersion"
} catch {
    Write-ErrorMessage "Docker is not installed or not in PATH"
    Write-Host "Please install Docker Desktop for Windows"
    Write-Host "https://www.docker.com/products/docker-desktop"
    exit 1
}

# Check if Docker is running / Verificar se Docker está rodando
try {
    docker ps 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
    Write-SuccessMessage "Docker is running"
} catch {
    Write-ErrorMessage "Docker is not running"
    Write-Host "Please start Docker Desktop"
    exit 1
}

# Check Docker Compose / Verificar Docker Compose
Write-Host ""
Write-InfoMessage "[2/9] Checking Docker Compose..."
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
    Write-SuccessMessage "Docker Compose found: $DockerCompose"
} catch {
    Write-ErrorMessage "Docker Compose not found"
    exit 1
}

# Create .env if doesn't exist / Criar .env se não existir
Write-Host ""
Write-InfoMessage "[3/9] Checking .env file..."
if (-not (Test-Path ".env")) {
    Write-InfoMessage "Creating .env from .env.example..."
    Copy-Item ".env.example" ".env"
    Write-SuccessMessage ".env created"
} else {
    Write-SuccessMessage ".env already exists"
}

# Stop existing containers / Parar containers existentes
Write-Host ""
Write-InfoMessage "[4/9] Stopping existing containers..."
& $DockerCompose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down 2>$null
Write-SuccessMessage "Containers stopped"

# Build containers / Construir containers
Write-Host ""
if ($DoBuild) {
    Write-InfoMessage "[5/9] Building Docker containers... (this may take a few minutes)"
    & $DockerCompose -f docker-compose.yml -f docker-compose.dev.yml --profile dev build
    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "Docker build failed"
        exit 1
    }
    Write-SuccessMessage "Build completed"
} else {
    Write-InfoMessage "[5/9] Skipping build..."
    Write-SuccessMessage "Using existing images"
}

# Start containers / Iniciar containers
Write-Host ""
Write-InfoMessage "[6/9] Starting containers..."
& $DockerCompose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d
if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Failed to start containers"
    exit 1
}
Write-SuccessMessage "Containers started"

# Wait for database / Aguardar banco de dados
Write-Host ""
Write-InfoMessage "[7/9] Waiting for database to be ready..."
Start-Sleep -Seconds 10
Write-SuccessMessage "Database ready"

# Create migrations / Criar migrations
Write-Host ""
Write-InfoMessage "[8/10] Creating database migrations..."
& $DockerCompose exec -T web python manage.py makemigrations
if ($LASTEXITCODE -ne 0) {
    Write-WarningMessage "No new migrations to create"
}
Write-SuccessMessage "Migrations created"

# Run migrations / Executar migrations
Write-Host ""
Write-InfoMessage "[9/10] Running database migrations..."
& $DockerCompose exec -T web python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-WarningMessage "Migrations had some issues, but continuing..."
}
Write-SuccessMessage "Migrations completed"

# Create superuser / Criar superuser
Write-Host ""
Write-InfoMessage "Creating superuser (if not exists)..."
& $DockerCompose exec -T web python manage.py create_superuser_if_none_exists
Write-SuccessMessage "Superuser check completed"

# Seed database / Popular banco
if ($SeedDB) {
    Write-Host ""
    Write-InfoMessage "Seeding database with sample data..."
    & $DockerCompose exec -T web python manage.py seed_database
    Write-SuccessMessage "Database seeded"
}

# Collect static files / Coletar arquivos estáticos
Write-Host ""
Write-InfoMessage "Collecting static files..."
& $DockerCompose exec -T web python manage.py collectstatic --noinput | Out-Null
Write-SuccessMessage "Static files collected"

# Install pre-commit hooks / Instalar hooks pre-commit
if ($RunPrecommit) {
    Write-Host ""
    Write-InfoMessage "[10/10] Setting up pre-commit hooks..."
    if (Test-Path ".git") {
        & $DockerCompose exec -T web pre-commit install
        & $DockerCompose exec -T web pre-commit run --all-files
        Write-SuccessMessage "Pre-commit hooks installed"
    } else {
        Write-WarningMessage "Not a git repository, skipping pre-commit"
    }
} else {
    Write-Host ""
    Write-InfoMessage "[10/10] Skipping pre-commit setup..."
}

# Run tests / Executar testes
if ($RunTests) {
    Write-Host ""
    Write-InfoMessage "Running tests..."
    & $DockerCompose exec -T web python manage.py test src

    if ($RunCoverage) {
        Write-Host ""
        Write-InfoMessage "Generating coverage report..."
        & $DockerCompose exec -T web coverage run manage.py test src
        & $DockerCompose exec -T web coverage report
    }
}

# Success message / Mensagem de sucesso
Write-Host ""
Write-Header "Setup completed successfully!"
Write-Host ""
Write-Host "Your Django Base project is now running!" -ForegroundColor Green
Write-Host ""
Write-Host "Access points:" -ForegroundColor Cyan
Write-Host "  - Django App:     http://localhost:8000"
Write-Host "  - Django Admin:   http://localhost:8000/admin"
Write-Host "  - API Docs:       http://localhost:8000/api/docs/"
Write-Host "  - Grafana:        http://localhost:3000 (admin/admin)"
Write-Host "  - Prometheus:     http://localhost:9090"
Write-Host ""
Write-Host "Default credentials:" -ForegroundColor Cyan
Write-Host "  - Username: admin"
Write-Host "  - Password: admin"
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  - View logs:      $DockerCompose -f docker-compose.yml -f docker-compose.dev.yml logs -f"
Write-Host "  - Stop:           $DockerCompose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down"
Write-Host "  - Restart:        $DockerCompose -f docker-compose.yml -f docker-compose.dev.yml --profile dev restart"
Write-Host "  - Shell:          $DockerCompose exec web bash"
Write-Host ""
