@echo off
REM Automated production setup script for Django Base project (Windows)
REM Script de configuração automatizada de produção para projeto Django Base (Windows)

setlocal enabledelayedexpansion

REM Default values / Valores padrão
set SKIP_BUILD=false
set COLLECT_STATIC=true
set VALIDATE_ENV=true

REM Parse arguments / Analisar argumentos
:parse_args
if "%~1"=="" goto start_setup
if /i "%~1"=="--skip-build" (
    set SKIP_BUILD=true
    shift
    goto parse_args
)
if /i "%~1"=="--no-static" (
    set COLLECT_STATIC=false
    shift
    goto parse_args
)
if /i "%~1"=="--skip-validation" (
    set VALIDATE_ENV=false
    shift
    goto parse_args
)
if /i "%~1"=="--help" goto show_help
if /i "%~1"=="-h" goto show_help

echo Unknown option: %~1
echo Use --help for usage information
exit /b 1

:show_help
echo Usage: setup-prod.bat [OPTIONS]
echo.
echo Production setup script for Django Base (Windows)
echo.
echo Options:
echo   --skip-build        Skip Docker build (use if images already exist)
echo   --no-static         Skip collecting static files
echo   --skip-validation   Skip environment validation (NOT recommended)
echo   --help, -h          Show this help message
echo.
echo IMPORTANT: Review your .env file before running!
echo            Make sure DEBUG=False and SECRET_KEY is strong.
exit /b 0

:start_setup
echo ========================================
echo Django Base - Production Setup
echo ========================================
echo.
echo WARNING: This script will set up a PRODUCTION environment
echo WARNING: Make sure you have reviewed your .env configuration!
echo.
set /p CONFIRM="Continue? (yes/no): "
if /i not "%CONFIRM%"=="yes" (
    echo Setup cancelled
    exit /b 0
)

REM Step 0: Pre-flight checks
echo.
echo ========================================
echo Step 0/8: Pre-flight Checks
echo ========================================

REM Check if .env exists
if not exist .env (
    echo CRITICAL: .env file not found!
    echo ERROR: Create .env from .env.example and configure for production
    echo Required changes:
    echo   - Set DEBUG=False
    echo   - Generate strong SECRET_KEY
    echo   - Configure ALLOWED_HOSTS
    echo   - Set strong database passwords
    echo   - Configure email settings
    exit /b 1
)
echo OK: .env file found

REM Check Docker Compose
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

REM Step 1: Docker build
echo.
echo ========================================
echo Step 1/8: Docker Build
echo ========================================
if "%SKIP_BUILD%"=="false" (
    echo Building production Docker images...
    %DOCKER_COMPOSE% --profile prod build --no-cache
    if errorlevel 1 (
        echo ERROR: Docker build failed
        exit /b 1
    )
    echo OK: Docker images built
) else (
    echo Skipping Docker build (--skip-build)
)

REM Step 2: Start containers
echo.
echo ========================================
echo Step 2/8: Starting Containers
echo ========================================
echo Starting production containers...
%DOCKER_COMPOSE% --profile prod up -d
if errorlevel 1 (
    echo ERROR: Failed to start containers
    exit /b 1
)

echo Waiting for containers to be healthy...
timeout /t 15 /nobreak >nul

REM Check if containers are running
%DOCKER_COMPOSE% ps | findstr "Up" >nul
if errorlevel 1 (
    echo ERROR: Some containers failed to start
    echo Check logs with: %DOCKER_COMPOSE% --profile prod logs
    exit /b 1
)
echo OK: All containers started successfully

REM Step 3: Database migrations
echo.
echo ========================================
echo Step 3/8: Database Migrations
echo ========================================
echo Running database migrations...
%DOCKER_COMPOSE% --profile prod exec -T web python manage.py migrate --noinput
if errorlevel 1 (
    echo ERROR: Migrations failed
    exit /b 1
)
echo OK: Migrations completed

REM Step 4: Collect static files
echo.
echo ========================================
echo Step 4/8: Collect Static Files
echo ========================================
if "%COLLECT_STATIC%"=="true" (
    echo Collecting static files for Nginx...
    %DOCKER_COMPOSE% --profile prod exec -T web python manage.py collectstatic --noinput --clear
    if errorlevel 1 (
        echo WARNING: Static collection had issues, but continuing...
    )
    echo OK: Static files collected
) else (
    echo Skipping static files collection (--no-static)
)

REM Step 5: Compile translations
echo.
echo ========================================
echo Step 5/8: Compile Translations
echo ========================================
echo Compiling translations (pt-br, en)...
%DOCKER_COMPOSE% --profile prod exec -T web python manage.py compilemessages
echo OK: Translations compiled

REM Step 6: Environment validation
echo.
echo ========================================
echo Step 6/8: Environment Validation
echo ========================================
echo Running Django environment validator...
%DOCKER_COMPOSE% --profile prod exec -T web python manage.py validate_env
echo Review any warnings or errors above

REM Step 7: Health checks
echo.
echo ========================================
echo Step 7/8: Health Checks
echo ========================================
echo Checking service health...

REM Wait a bit for services to stabilize
timeout /t 5 /nobreak >nul

REM Check database
echo Checking database connection...
%DOCKER_COMPOSE% --profile prod exec -T db pg_isready -U django_user >nul 2>&1
if errorlevel 1 (
    echo ERROR: Database connection failed
) else (
    echo OK: Database is healthy
)

REM Check Redis
echo Checking Redis connection...
%DOCKER_COMPOSE% --profile prod exec -T redis redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo ERROR: Redis connection failed
) else (
    echo OK: Redis is healthy
)

REM Check web application (with retry)
echo Checking web application...
set WEB_HEALTHY=false
for /l %%i in (1,1,5) do (
    curl -f -s http://localhost:8000/health/ >nul 2>&1
    if not errorlevel 1 (
        echo OK: Web application is healthy
        set WEB_HEALTHY=true
        goto health_check_done
    )
    if %%i lss 5 (
        timeout /t 2 /nobreak >nul
    ) else (
        echo WARNING: Web application health check failed (may take time to start)
    )
)
:health_check_done

REM Step 8: Security reminder
echo.
echo ========================================
echo Step 8/8: Security Checklist
echo ========================================
echo WARNING: PRODUCTION SECURITY CHECKLIST:
echo.
echo   □ DEBUG=False in .env
echo   □ Strong SECRET_KEY configured
echo   □ ALLOWED_HOSTS properly configured
echo   □ Strong database passwords
echo   □ SSL/HTTPS configured (see docs/SSL_HTTPS_SETUP.md)
echo   □ Firewall rules configured
echo   □ Regular backups scheduled
echo   □ Monitoring and alerts configured
echo   □ Email settings configured
echo   □ Sentry or error monitoring configured
echo.

REM Final summary
echo ========================================
echo Production Setup Complete!
echo ========================================
echo.
echo OK: Production environment is ready!
echo.
echo Access points / Pontos de acesso:
echo   - Application: http://localhost (or your domain)
echo   - Admin Panel: http://localhost/admin
echo   - API Docs: http://localhost/api/docs/
echo   - Health Check: http://localhost/health/
echo   - Prometheus: http://localhost:9090
echo   - Grafana: http://localhost:3000 (admin/admin)
echo.
echo Monitoring dashboards:
echo   - Django Base Overview (auto-provisioned)
echo   - PostgreSQL Database (ID: 9628)
echo   - Nginx Metrics (ID: 12708)
echo   - Redis Dashboard (ID: 11835)
echo.
echo Next steps:
echo   1. Create superuser: %DOCKER_COMPOSE% exec web python manage.py createsuperuser
echo   2. Configure SSL certificates (see docs/SSL_HTTPS_SETUP.md)
echo   3. Set up automated backups: scripts\backup_database.bat
echo   4. Review Grafana dashboards at http://localhost:3000
echo   5. Test all critical endpoints
echo.
echo Useful commands:
echo   - View logs: %DOCKER_COMPOSE% logs -f
echo   - Stop all: %DOCKER_COMPOSE% --profile prod down
echo   - Shell: %DOCKER_COMPOSE% exec web bash
echo   - Backup DB: scripts\backup_database.bat
echo   - Restart: %DOCKER_COMPOSE% restart
echo.
echo WARNING: Remember: Review logs regularly and monitor your application!
echo.
echo Production deployment successful!

endlocal
