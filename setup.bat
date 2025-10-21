@echo off
REM Automated development setup script for Django Base project (Windows)
REM Script de configuração automatizada de desenvolvimento para projeto Django Base (Windows)

setlocal enabledelayedexpansion

REM Colors are not directly supported in batch, but we can use echo for formatting
REM Cores não são diretamente suportadas em batch, mas podemos usar echo para formatação

REM Default values / Valores padrão
set RUN_PRECOMMIT=true
set RUN_TESTS=true
set RUN_COVERAGE=true
set SEED_DB=true
set SKIP_BUILD=false
set QUICK_MODE=false

REM Parse arguments / Analisar argumentos
:parse_args
if "%~1"=="" goto start_setup
if /i "%~1"=="--skip-precommit" (
    set RUN_PRECOMMIT=false
    shift
    goto parse_args
)
if /i "%~1"=="--skip-tests" (
    set RUN_TESTS=false
    shift
    goto parse_args
)
if /i "%~1"=="--skip-coverage" (
    set RUN_COVERAGE=false
    shift
    goto parse_args
)
if /i "%~1"=="--no-seed" (
    set SEED_DB=false
    shift
    goto parse_args
)
if /i "%~1"=="--skip-build" (
    set SKIP_BUILD=true
    shift
    goto parse_args
)
if /i "%~1"=="--quick" (
    set QUICK_MODE=true
    set RUN_TESTS=false
    set RUN_PRECOMMIT=false
    shift
    goto parse_args
)
if /i "%~1"=="--help" goto show_help
if /i "%~1"=="-h" goto show_help

echo Unknown option: %~1
echo Use --help for usage information
exit /b 1

:show_help
echo Usage: setup.bat [OPTIONS]
echo.
echo Development setup script for Django Base (Windows)
echo.
echo Options:
echo   --skip-precommit    Skip pre-commit hooks installation and run
echo   --skip-tests        Skip running tests
echo   --skip-coverage     Skip coverage report generation
echo   --no-seed           Don't seed database with sample data
echo   --skip-build        Skip Docker build (use if images already exist)
echo   --quick             Quick mode: skip tests and pre-commit (faster setup)
echo   --help, -h          Show this help message
echo.
echo Examples:
echo   setup.bat                    # Full setup with all features
echo   setup.bat --quick            # Quick setup for rapid testing
echo   setup.bat --skip-build       # Skip Docker build (if images exist)
exit /b 0

:start_setup
echo ========================================
echo Django Base - Development Setup (Windows)
echo ========================================
echo.

REM Check Docker is running / Verificar se Docker está rodando
echo [1/9] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop for Windows
    echo https://www.docker.com/products/docker-desktop
    exit /b 1
)

docker ps >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running
    echo Please start Docker Desktop
    exit /b 1
)
echo OK: Docker is running

REM Check Docker Compose / Verificar Docker Compose
echo.
echo [2/9] Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    REM Try docker compose v2
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Docker Compose not found
        exit /b 1
    )
    set "DOCKER_COMPOSE=docker compose"
) else (
    set "DOCKER_COMPOSE=docker-compose"
)
echo OK: Docker Compose found

REM Create .env if doesn't exist / Criar .env se não existir
echo.
echo [3/9] Checking .env file...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env >nul
    echo OK: .env created
) else (
    echo OK: .env already exists
)

REM Stop existing containers / Parar containers existentes
echo.
echo [4/9] Stopping existing containers...
%DOCKER_COMPOSE% -f docker-compose.yml -f docker-compose.dev.yml --profile dev down >nul 2>&1
echo OK: Containers stopped

REM Build containers / Construir containers
if "%SKIP_BUILD%"=="false" (
    echo.
    echo [5/9] Building Docker containers... (this may take a few minutes)
    %DOCKER_COMPOSE% -f docker-compose.yml -f docker-compose.dev.yml --profile dev build
    if errorlevel 1 (
        echo ERROR: Docker build failed
        exit /b 1
    )
    echo OK: Build completed
) else (
    echo.
    echo [5/9] Skipping build...
    echo OK: Using existing images
)

REM Start containers / Iniciar containers
echo.
echo [6/9] Starting containers...
%DOCKER_COMPOSE% -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d
if errorlevel 1 (
    echo ERROR: Failed to start containers
    exit /b 1
)
echo OK: Containers started

REM Wait for database / Aguardar banco de dados
echo.
echo [7/9] Waiting for database to be ready...
timeout /t 10 /nobreak >nul
echo OK: Database ready

REM Create migrations / Criar migrations
echo.
echo [8/10] Creating database migrations...
%DOCKER_COMPOSE% exec -T web python manage.py makemigrations
if errorlevel 1 (
    echo WARNING: No new migrations to create
)
echo OK: Migrations created

REM Run migrations / Executar migrations
echo.
echo [9/10] Running database migrations...
%DOCKER_COMPOSE% exec -T web python manage.py migrate
if errorlevel 1 (
    echo WARNING: Migrations had some issues, but continuing...
)
echo OK: Migrations completed

REM Create superuser / Criar superuser
echo.
echo Creating superuser (if not exists)...
%DOCKER_COMPOSE% exec -T web python manage.py create_superuser_if_none_exists
echo OK: Superuser check completed

REM Seed database / Popular banco
if "%SEED_DB%"=="true" (
    echo.
    echo Seeding database with sample data...
    %DOCKER_COMPOSE% exec -T web python manage.py seed_database
    echo OK: Database seeded
)

REM Collect static files / Coletar arquivos estáticos
echo.
echo Collecting static files...
%DOCKER_COMPOSE% exec -T web python manage.py collectstatic --noinput >nul
echo OK: Static files collected

REM Install pre-commit hooks / Instalar hooks pre-commit
if "%RUN_PRECOMMIT%"=="true" (
    echo.
    echo [10/10] Setting up pre-commit hooks...
    if exist .git (
        %DOCKER_COMPOSE% exec -T web pre-commit install
        %DOCKER_COMPOSE% exec -T web pre-commit run --all-files
        echo OK: Pre-commit hooks installed
    ) else (
        echo WARNING: Not a git repository, skipping pre-commit
    )
) else (
    echo.
    echo [10/10] Skipping pre-commit setup...
)

REM Run tests / Executar testes
if "%RUN_TESTS%"=="true" (
    echo.
    echo Running tests...
    %DOCKER_COMPOSE% exec -T web python manage.py test src
    if "%RUN_COVERAGE%"=="true" (
        echo.
        echo Generating coverage report...
        %DOCKER_COMPOSE% exec -T web coverage run manage.py test src
        %DOCKER_COMPOSE% exec -T web coverage report
    )
)

REM Success message / Mensagem de sucesso
echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Your Django Base project is now running!
echo.
echo Access points:
echo   - Django App:     http://localhost:8000
echo   - Django Admin:   http://localhost:8000/admin
echo   - API Docs:       http://localhost:8000/api/docs/
echo   - Grafana:        http://localhost:3000 (admin/admin)
echo   - Prometheus:     http://localhost:9090
echo.
echo Default credentials:
echo   - Username: admin
echo   - Password: admin
echo.
echo Useful commands:
echo   - View logs:      %DOCKER_COMPOSE% -f docker-compose.yml -f docker-compose.dev.yml logs -f
echo   - Stop:           %DOCKER_COMPOSE% -f docker-compose.yml -f docker-compose.dev.yml --profile dev down
echo   - Restart:        %DOCKER_COMPOSE% -f docker-compose.yml -f docker-compose.dev.yml --profile dev restart
echo   - Shell:          %DOCKER_COMPOSE% exec web bash
echo.

endlocal
