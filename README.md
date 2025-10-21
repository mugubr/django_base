# Django Base (django_base) 🚀

[![CI Pipeline Status](https://github.com/mugubr/django_base/actions/workflows/ci.yml/badge.svg)](https://github.com/mugubr/django_base/actions/workflows/ci.yml)

🇬🇧 / 🇺🇸

## English

This is a modern, production-ready base project for Django development, fully
configured with Docker, security hardening, modular settings, and comprehensive
observability. The structure follows best practices for scalability,
maintainability, and professional deployment.

### 🛠️ Tech Stack

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django-rest-framework&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Ruff-D7B092?style=for-the-badge&logo=ruff&logoColor=black" alt="Ruff">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
</div>

#### Core Technologies

- **Web Server:** [Nginx](https://nginx.org/en/docs/) (with rate limiting, gzip,
  security headers)
- **Application Server:** [Gunicorn](https://docs.gunicorn.org/) (multi-worker
  WSGI)
- **Backend:** [Django](https://docs.djangoproject.com/) 5.2+,
  [Django REST Framework](https://www.django-rest-framework.org/)
- **Database:** [PostgreSQL](https://www.postgresql.org/docs/) 15 (with
  connection pooling)
- **Cache & Queue:** [Redis](https://redis.io/docs/) 7 (for caching, sessions,
  Django Q)
- **Package Manager:** [uv](https://docs.astral.sh/uv/) (blazing fast Python
  package manager)
- **Background Tasks:** [Django Q2](https://django-q2.readthedocs.io/)
  (`django-q2`)
- **API Features:** [CORS](https://pypi.org/project/django-cors-headers/),
  [DRF Spectacular](https://drf-spectacular.readthedocs.io/) (OpenAPI/Swagger),
  [django-filter](https://django-filter.readthedocs.io/)
- **Containerization:** [Docker](https://docs.docker.com/) &
  [Docker Compose](https://docs.docker.com/compose/) (multi-stage builds),
  [Kubernetes](https://kubernetes.io/docs/)
- **Code Quality:** [Ruff](https://docs.astral.sh/ruff/) linter/formatter,
  [pre-commit](https://pre-commit.com/) hooks,
  [Bandit](https://bandit.readthedocs.io/) security
- **Testing:**
  [django.test](https://docs.djangoproject.com/en/stable/topics/testing/) with
  [coverage](https://coverage.readthedocs.io/),
  [Factory Boy](https://factoryboy.readthedocs.io/)
- **Error Tracking:**
  [Sentry](https://docs.sentry.io/platforms/python/integrations/django/) for
  error monitoring and performance
- **Observability:** [Prometheus](https://prometheus.io/docs/) &
  [Grafana](https://grafana.com/docs/) dashboards with exporters
- **Configuration:**
  [python-decouple](https://pypi.org/project/python-decouple/) with
  comprehensive `.env` support
- **Development Tools:**
  [django-extensions](https://django-extensions.readthedocs.io/),
  [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/),
  [watchdog](https://python-watchdog.readthedocs.io/) for hot-reloading,
  [Makefile](https://www.gnu.org/software/make/manual/make.html) (60+ commands)
- **AI Assistant:** [Claude Code](https://docs.claude.com/claude-code)
  integration with custom agents and MCP server

### ✨ Key Features

#### Infrastructure & Architecture

- ✅ **Modular Settings:** Separate `base.py`, `dev.py`, `prod.py` for
  environment-specific config
- ✅ **Environment Validation:** Automatic validation of critical configuration
  on startup (prevents production misconfigurations)
- ✅ **Security Hardening:** HSTS, SSL redirect, secure cookies, modern security
  headers (Permissions-Policy, COOP, CORP), rate limiting
- ✅ **Production-Ready:** Multi-stage Docker builds, non-root user, health
  checks, SSL/HTTPS ready
- ✅ **Kubernetes Support:** Complete K8s manifests with Kustomize overlays for
  dev/prod environments
- ✅ **Database Backup System:** Professional backup/restore scripts with
  retention policies and integrity verification
- ✅ **Redis Integration:** Caching, session storage, task queue backend
- ✅ **Enhanced Observability:** Prometheus + Grafana with PostgreSQL, Redis,
  and Nginx exporters
- ✅ **Developer Productivity:** Makefile with 60+ commands (18 for Kubernetes)
- ✅ **Pre-commit Hooks:** 20+ hooks including Ruff, Bandit, detect-secrets,
  django-upgrade
- ✅ **CI/CD Ready:** GitHub Actions pipeline with linting and tests
- ✅ **Bilingual Documentation:** Full PT-BR/EN comments throughout codebase
- ✅ **Query Optimization:** All ViewSets optimized with
  select_related/prefetch_related
- ✅ **Dark Mode Support:** Elegant dark/light theme toggle with localStorage
  persistence
- ✅ **Internationalization (i18n):** Multi-language support (EN/PT-BR) with
  navbar language selector
- ✅ **Template Reorganization:** Clean, organized template structure following
  Django best practices
- ✅ **Soft Delete Pattern:** All models use soft deletion with mixins for data
  integrity
- ✅ **Cross-Platform Setup:** Windows support with PowerShell (.ps1) and Batch
  (.bat) scripts
- ✅ **Enhanced Project Info Page:** Complete technology stack documentation
  with links
- ✅ **Error Tracking:** Sentry integration with traces and profiling
- ✅ **Debug Toolbar:** django-debug-toolbar for development profiling
- ✅ **Test Factories:** Factory Boy for realistic test data generation
- ✅ **Integration Tests:** Complete API workflow testing
- ✅ **Claude Code Integration:** Custom agents (Django Expert, Code Reviewer,
  Backend Architect, Python Pro) + Memory MCP server

#### Portfolio Features (Authentication & User Management)

- ✅ **Complete Authentication System:** Login, register, logout, profile
  management
- ✅ **User Profiles:** Extended user model with avatar, bio, phone, location,
  website
- ✅ **5 Custom Forms:** LoginForm with remember_me, RegisterForm with
  validation, UserProfileForm, UserUpdateForm, ProductForm
- ✅ **Bootstrap 5 Templates:** Responsive UI with home, login, register,
  profile, product listing, product creation pages
- ✅ **Auto Profile Creation:** Django signals automatically create UserProfile
  when User is created
- ✅ **Product Management:** Full CRUD for products with category/tag filtering

#### Data Models & Relationships

- ✅ **4 Models:** Product, UserProfile, Category (hierarchical), Tag
- ✅ **Model Relationships:** OneToOne, ForeignKey, ManyToMany, Self-referencing
  FK
- ✅ **Soft Delete Pattern:** Deactivate instead of hard delete for data
  integrity
- ✅ **Business Logic:** Properties, custom methods, class methods on models
- ✅ **Model Validators:** Phone, CPF, image size/dimensions, dates, URLs

#### REST API & Documentation

- ✅ **API Documentation:** Auto-generated OpenAPI/Swagger with drf-spectacular
- ✅ **4 DRF ViewSets:** Product, Category, Tag, UserProfile with full CRUD
- ✅ **10 Serializers:** Detail and list serializers for all models
- ✅ **Custom Actions:** /tree/ for categories, /popular/ for tags, /me/ for
  profiles
- ✅ **Filtering & Search:** django-filter integration with search, ordering,
  pagination

#### Template System & UI Components

- ✅ **23 Template Tags & Filters:** currency, percentage, time_ago, file_size,
  badges, icons, alerts
- ✅ **Reusable Components:** Card component, pagination, responsive layouts
- ✅ **Product Pages:** Listing with filters (category, tags, price range) +
  creation form
- ✅ **Internationalization (i18n):** Full PT-BR/EN support with {% trans %}
  tags in all templates
- ✅ **Visual Health Check:** Beautiful health monitoring page with auto-refresh
  and real-time status
- ✅ **UI Enhancements:** Hover effects, auto-dismiss alerts, custom green theme
  (#198754)
- ✅ **Bootstrap 5.3 Green Theme:** Custom green primary color (#198754)
  replacing default blue
- ✅ **HTMX Support:** Dynamic interactions without JavaScript complexity

#### Developer Tools & Utilities

- ✅ **8 Custom Validators:** Phone, CPF, image validation, date validation,
  regex validators
- ✅ **15 Decorators:** Permissions, caching, logging, production-ready
  Redis-based rate limiting, AJAX, JSON response
- ✅ **13 Mixins:** Model mixins (timestamps, soft delete, user tracking) + view
  mixins (permissions, pagination, AJAX)
- ✅ **Django Signals:** Auto-creation of related models with error handling
- ✅ **Admin Customization:** Enhanced admin interface with custom fieldsets and
  filters

### 🏁 Running the Project (Docker)

#### 💻 Development Mode (`dev` profile)

This mode is for active development with hot-reloading, debug mode, and verbose
logging.

1. **Automated Setup (Recommended):**

   **Linux/macOS:**

   ```bash
   # Clone the repo and enter the directory / Clone o repo e entre no diretório
   git clone <your-repository-url> && cd django_base

   # Run automated setup script / Execute o script de configuração automatizada
   ./setup.sh
   ```

   **Windows (PowerShell - Recommended):**

   ```powershell
   # Clone the repo and enter the directory / Clone o repo e entre no diretório
   git clone <your-repository-url>
   cd django_base

   # Run automated setup script / Execute o script de configuração automatizada
   .\setup.ps1
   ```

   **Windows (Command Prompt):**

   ```cmd
   # Clone the repo and enter the directory / Clone o repo e entre no diretório
   git clone <your-repository-url>
   cd django_base

   # Run automated setup script / Execute o script de configuração automatizada
   setup.bat
   ```

   **This automatically handles:**
   - .env file creation
   - Docker build and startup
   - Database migrations
   - Superuser creation (admin/admin)
   - Database seeding
   - Translation compilation (PT-BR/EN)
   - Running tests with coverage

   **Available options / Opções disponíveis:**
   - `--quick` or `-Quick`: Skip tests and pre-commit (faster setup)
   - `--skip-build` or `-SkipBuild`: Skip Docker build (use if images exist)
   - `--help` or `-Help`: Show all available options

2. **Manual Setup (Alternative):**

   ```bash
   # Clone the repo and enter the directory
   git clone <your-repository-url> && cd django_base

   # Create the environment file
   cp .env.example .env

   # Build and start all services
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d --build

   # Run database migrations
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate

   # Create a superuser
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

   # Populate database with sample data
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py seed_database

   # Compile i18n translations
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py compilemessages
   ```

3. **To Start the Development Server:** _This command will attach to your
   terminal and show live logs. Press `Ctrl + C` to stop._

   ```bash
   # Start in foreground (with logs) / Inicie em primeiro plano (com logs)
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up

   # Or start in background / Ou inicie em background
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d
   ```

4. **To Stop the Development Server:**

   ```bash
   # Stop all services / Pare todos os serviços
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down
   ```

#### 🚀 Production Mode (`prod` profile)

This mode runs the production stack with Nginx, Gunicorn, Redis caching, and
security hardening.

1. **Automated Setup (Recommended):**

   **Linux/macOS:**

   ```bash
   # Configure .env for production first!
   # Configure .env para produção primeiro!
   cp .env.example .env
   # Edit .env: Set DEBUG=False, strong SECRET_KEY, ALLOWED_HOSTS, etc.
   # Edite .env: Defina DEBUG=False, SECRET_KEY forte, ALLOWED_HOSTS, etc.

   # Run automated production setup / Execute o script de configuração de produção
   ./setup-prod.sh
   ```

   **Windows (PowerShell - Recommended):**

   ```powershell
   # Configure .env for production first!
   Copy-Item .env.example .env
   # Edit .env: Set DEBUG=False, strong SECRET_KEY, ALLOWED_HOSTS, etc.

   # Run automated production setup / Execute o script de configuração de produção
   .\setup-prod.ps1
   ```

   **Windows (Command Prompt):**

   ```cmd
   # Configure .env for production first!
   copy .env.example .env
   # Edit .env: Set DEBUG=False, strong SECRET_KEY, ALLOWED_HOSTS, etc.

   # Run automated production setup / Execute o script de configuração automatizada
   setup-prod.bat
   ```

   **This automatically handles:**
   - Environment validation (DEBUG, SECRET_KEY, etc.)
   - Docker build and startup
   - Database migrations
   - Static files collection
   - Translation compilation
   - Health checks
   - Security checklist reminder

   **Available options / Opções disponíveis:**
   - `--skip-build` or `-SkipBuild`: Skip Docker build (use if images exist)
   - `--no-static` or `-NoStatic`: Skip collecting static files
   - `--help` or `-Help`: Show all available options

2. **Manual Setup (Alternative):**

   ```bash
   # Copy and edit .env with production values
   cp .env.example .env
   # IMPORTANT: Set DEBUG=False, configure SECRET_KEY, ALLOWED_HOSTS, etc.

   # Build and start all production services
   docker-compose --profile prod up -d --build

   # Run migrations
   docker-compose --profile prod exec web python manage.py migrate

   # Collect static files for Nginx
   docker-compose --profile prod exec web python manage.py collectstatic --no-input

   # Compile i18n translations
   docker-compose --profile prod exec web python manage.py compilemessages

   # Create superuser (manual)
   docker-compose --profile prod exec web python manage.py createsuperuser
   ```

3. **To Stop the Production Stack:**

   ```bash
   # Stop all services / Pare todos os serviços
   docker-compose --profile prod down
   # or / ou
   make prod-down
   ```

#### 🌐 Access Points

After starting, your environment will be available at:

**Frontend (Templates):**

- **Homepage:** `http://localhost:8000/`
- **Login:** `http://localhost:8000/login/`
- **Register:** `http://localhost:8000/register/`
- **Profile:** `http://localhost:8000/profile/` (requires authentication)
- **Products:** `http://localhost:8000/products/` (catalog with filters)
- **Create Product:** `http://localhost:8000/products/create/` (requires
  authentication)
- **Django Admin:** `http://localhost:8000/admin/`

**API (REST Framework):**

- **API Root:** `http://localhost:8000/api/v1/`
- **Products:** `http://localhost:8000/api/v1/products/`
- **Categories:** `http://localhost:8000/api/v1/categories/`
  - **Category Tree:** `http://localhost:8000/api/v1/categories/tree/`
- **Tags:** `http://localhost:8000/api/v1/tags/`
  - **Popular Tags:** `http://localhost:8000/api/v1/tags/popular/`
- **User Profiles:** `http://localhost:8000/api/v1/profiles/`
  - **My Profile:** `http://localhost:8000/api/v1/profiles/me/` (requires
    authentication)
- **API Info:** `http://localhost:8000/api/info/`

**Documentation:**

- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`
- **OpenAPI Schema:** `http://localhost:8000/api/schema/`

**Monitoring & Health:**

- **Health Check (API):** `http://localhost:8000/health/`
- **Health Check (Visual):** `http://localhost:8000/health-status/`
- **Prometheus Metrics:** `http://localhost:8000/metrics/metrics`
- **Prometheus:** `http://localhost:9090`
- **Grafana:** `http://localhost:3000` (default login: `admin`/`admin`)

**Test Credentials:**

- **Superuser:** `admin` / `admin123`
- **Test User:** `testuser` / `test123` (has UserProfile auto-created)

---

### 💻 Local Development (Without Docker)

#### Prerequisites

- Python 3.11+
- PostgreSQL server running locally
- Redis server running locally (optional, for caching/queue)
- `uv` installed (recommended) or `pip`

#### Steps

1. **Clone the repository and `cd` into it:**

   ```bash
   git clone <your-repository-url> && cd django_base
   ```

2. **Set up the environment file (`.env`):** Copy `.env.example` to `.env`.
   **Important:** Change `POSTGRES_HOST=db` to `POSTGRES_HOST=localhost` and
   `REDIS_HOST=redis` to `REDIS_HOST=localhost`.

   ```bash
   cp .env.example .env
   # Now edit .env and update database/redis hosts
   ```

3. **Install dependencies with `uv` (Recommended):**

   ```bash
   # Create a virtual environment
   uv venv

   # Activate it (macOS/Linux)
   source .venv/bin/activate

   # Activate it (Windows PowerShell)
   .venv\Scripts\Activate.ps1

   # or Windows (Command Prompt)
   .venv\Scripts\activate.bat

   # Install all dependencies (production + dev)
   uv sync --dev
   ```

4. **Run Migrations and Create Superuser:**

   ```bash
   # Set Django settings module for development
   export DJANGO_SETTINGS_MODULE=django_base.settings.dev  # Linux/macOS
   # or
   set DJANGO_SETTINGS_MODULE=django_base.settings.dev     # Windows CMD
   # or
   $env:DJANGO_SETTINGS_MODULE="django_base.settings.dev"  # Windows PowerShell

   # Run migrations
   python manage.py migrate

   # Create superuser
   python manage.py createsuperuser
   ```

5. **Run the Development Server:**

   ```bash
   # With django-extensions (enhanced debugger)
   python manage.py runserver_plus

   # Or standard runserver
   python manage.py runserver
   ```

---

### 📖 Development Workflow

#### Environment Settings

This project uses modular settings for different environments:

- **`settings/base.py`**: Shared configuration across all environments
- **`settings/dev.py`**: Development-specific settings (DEBUG=True, console
  email, dummy cache)
- **`settings/prod.py`**: Production settings (security hardening, Redis cache,
  logging)

To switch environments, set the `DJANGO_SETTINGS_MODULE` variable:

```bash
# Development (default)
export DJANGO_SETTINGS_MODULE=django_base.settings.dev

# Production
export DJANGO_SETTINGS_MODULE=django_base.settings.prod
```

#### How to Add a New Library

The `pyproject.toml` file is the source of truth for dependencies.

**With Docker:**

1. **Run the install command inside the `web` container:**

   ```bash
   # For a production dependency
   docker-compose exec web uv add "some-package"

   # For a development dependency (like a testing tool)
   docker-compose exec web uv add "some-dev-package" --dev
   ```

2. **To make the change permanent in the image**, rebuild it:

   ```bash
   docker-compose build
   ```

**Locally (without Docker):**

```bash
# For a production dependency
uv add "some-package"

# For a development dependency
uv add "some-dev-package" --dev
```

#### How to Create a New App

1. Ensure your **development** environment is running.
2. Execute the `startapp` command:

   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py startapp my_new_app
   ```

3. Move the new `my_new_app` folder into the `src/` directory.
4. Add `'my_new_app'` to `INSTALLED_APPS` in `src/django_base/settings/base.py`.
5. Create and configure the app's `urls.py`.

#### Pre-commit Hooks

This project uses comprehensive pre-commit hooks for code quality:

```bash
# Install pre-commit hooks (first time only)
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

Hooks include:

- **Ruff** (linting + formatting)
- **Bandit** (security linting)
- **detect-secrets** (prevent secret commits)
- **django-upgrade** (Django best practices)
- **markdownlint** (Markdown formatting)
- And 15+ more quality checks

---

### 🚀 Day-to-Day Commands (Docker)

#### Development Commands

```bash
# Start dev environment with live logs / Iniciar ambiente dev com logs ao vivo
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up

# Start in background / Iniciar em background
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d

# View logs / Ver logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f web

# Access container shell / Acessar shell do container
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web bash

# Run migrations / Executar migrações
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate

# Compile translations / Compilar traduções
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py compilemessages

# Create superuser / Criar superusuário
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Seed database with sample data / Popular banco com dados de exemplo
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py seed_database

# Seed and clear existing data / Popular e limpar dados existentes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py seed_database --clear

# Run tests / Executar testes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py test core

# Run tests with coverage / Executar testes com cobertura
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage run manage.py test core
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage report

# Run linting / Executar linting
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff check .

# Format code / Formatar código
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff format .

# Stop all services / Parar todos os serviços
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down
```

#### Production Commands

```bash
# Start production stack / Iniciar stack de produção
docker-compose --profile prod up -d

# View logs / Ver logs
docker-compose --profile prod logs -f

# Run migrations / Executar migrações
docker-compose --profile prod exec web python manage.py migrate

# Compile translations / Compilar traduções
docker-compose --profile prod exec web python manage.py compilemessages

# Collect static files / Coletar arquivos estáticos
docker-compose --profile prod exec web python manage.py collectstatic --no-input

# Access container shell / Acessar shell do container
docker-compose --profile prod exec web bash

# Restart services / Reiniciar serviços
docker-compose --profile prod restart

# Stop all services / Parar todos os serviços
docker-compose --profile prod down
```

#### Database Commands

```bash
# Professional backup with retention (RECOMMENDED) / Backup profissional com retenção (RECOMENDADO)
./scripts/backup_database.sh

# Restore from backup (interactive) / Restaurar de backup (interativo)
./scripts/restore_database.sh

# Restore specific backup / Restaurar backup específico
./scripts/restore_database.sh backup_django_db_20250112.sql.gz

# Manual backup (alternative) / Backup manual (alternativa)
docker-compose exec db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup.sql

# Manual restore (alternative) / Restauração manual (alternativa)
docker-compose exec -T db psql -U ${POSTGRES_USER} ${POSTGRES_DB} < backup.sql

# Access PostgreSQL shell / Acessar shell PostgreSQL
docker-compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# Check database is ready / Verificar se banco está pronto
docker-compose exec db pg_isready -U ${POSTGRES_USER}
```

**Note:** For complete backup/restore documentation, see `scripts/README.md`
**Nota:** Para documentação completa de backup/restore, veja `scripts/README.md`

#### Redis Commands

```bash
# Access Redis CLI / Acessar CLI do Redis
docker-compose exec redis redis-cli

# Ping Redis / Testar conexão Redis
docker-compose exec redis redis-cli ping

# Check Redis info / Verificar informações do Redis
docker-compose exec redis redis-cli INFO

# Flush all Redis data (CAREFUL!) / Limpar todos os dados Redis (CUIDADO!)
docker-compose exec redis redis-cli FLUSHALL
```

---

### ☸️ Kubernetes Deployment

This project includes complete Kubernetes manifests for deploying to any
Kubernetes cluster.

#### Quick Start

**Automated Setup (Recommended):**

**Linux/macOS:**

```bash
# Development setup (builds image + deploys)
./setup-k8s.sh

# Production setup (builds image + deploys)
./setup-k8s.sh --prod
```

**Windows (PowerShell - Recommended):**

```powershell
# Development setup (builds image + deploys)
.\setup-k8s.ps1

# Production setup (builds image + deploys)
.\setup-k8s.ps1 -Prod
```

**Windows (Command Prompt):**

```cmd
# Development setup (builds image + deploys)
setup-k8s.bat

# Production setup (builds image + deploys)
setup-k8s.bat --prod
```

**Available options / Opções disponíveis:**

- `--skip-build` or `-SkipBuild`: Skip Docker image build
- `--skip-deploy` or `-SkipDeploy`: Only build image, don't deploy
- `--help` or `-Help`: Show all available options

**Manual Deployment:**

```bash
# Deploy to development
make k8s-dev-deploy

# Deploy to production (requires confirmation)
make k8s-prod-deploy

# Check deployment status
make k8s-status

# View logs
make k8s-logs

# Access application via port forward
kubectl port-forward -n django-base svc/dev-nginx-service 8000:80
```

#### Features

- **Complete Manifests:** 12 base manifests (namespace, configmaps, secrets,
  PVCs, deployments, services, ingress)
- **Kustomize Overlays:** Separate configurations for dev and prod environments
- **Auto-Scaling Ready:** HPA configuration included
- **Health Checks:** Liveness and readiness probes for all services
- **Resource Limits:** CPU and memory limits defined
- **RBAC:** Prometheus service account with cluster role
- **Persistent Storage:** PVCs for PostgreSQL, Redis, static/media files,
  Prometheus, Grafana

#### Services Deployed

- Django web application (with init containers for migrations/collectstatic)
- PostgreSQL database
- Redis cache
- Nginx reverse proxy
- Prometheus monitoring
- Grafana dashboards

For complete Kubernetes documentation, see [`k8s/README.md`](k8s/README.md).

---

### 🧪 Testing

#### Run Tests (Docker)

```bash
# Run all tests / Executar todos os testes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py test core

# Run with coverage / Executar com cobertura
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage run manage.py test core
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage report

# Generate HTML coverage report / Gerar relatório HTML de cobertura
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage html
# Report available at: htmlcov/index.html / Relatório disponível em: htmlcov/index.html

# Run specific test class / Executar classe de teste específica
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py test core.tests.TestProduct

# Run with verbose output / Executar com saída verbosa
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py test core --verbosity=2
```

#### Run Tests (Local - Without Docker)

```bash
# Run all tests / Executar todos os testes
python manage.py test core

# Run with coverage / Executar com cobertura
coverage run manage.py test core
coverage report
coverage html  # Generate HTML report / Gerar relatório HTML

# Run specific test file / Executar arquivo de teste específico
python manage.py test core.tests

# Run with pytest (if installed) / Executar com pytest (se instalado)
pytest src/
```

#### Linting and Formatting (Docker)

```bash
# Check code with Ruff / Verificar código com Ruff
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff check .

# Auto-fix issues / Auto-corrigir problemas
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff check --fix .

# Format code / Formatar código
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff format .

# Run all pre-commit hooks / Executar todos os hooks pre-commit
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web pre-commit run --all-files
```

#### Linting and Formatting (Local - Without Docker)

```bash
# Check code with Ruff / Verificar código com Ruff
ruff check .

# Auto-fix issues / Auto-corrigir problemas
ruff check --fix .

# Format code / Formatar código
ruff format .

# Run all pre-commit hooks / Executar todos os hooks pre-commit
pre-commit run --all-files
```

---

### 📊 Monitoring & Observability

#### Prometheus

Access Prometheus at `http://localhost:9090` to:

- Query metrics
- Set up alerts
- Monitor application performance

Key metrics available:

- Django: `django_http_requests_total`, `django_http_responses_total`,
  `django_http_requests_latency_seconds`, `django_db_query_count`
- PostgreSQL: Connection pools, query performance, table statistics
- Redis: Memory usage, hit rate, connected clients
- Nginx: Request rates, connection stats, response codes

#### Grafana

Access Grafana at `http://localhost:3000` (default: `admin`/`admin`)

Grafana dashboards are **automatically provisioned** on startup with
pre-configured datasources.

**First-Time Setup:**

1. After logging in, change the default password when prompted
2. Navigate to **Configuration** (⚙️) → **Data Sources**
3. Click **Add data source** → Select **Prometheus**
4. Configure Prometheus:
   - **Name:** `Prometheus`
   - **URL:** `http://prometheus:9090`
   - Click **Save & Test** (you should see "Data source is working")

**Recommended Dashboards:**

Pre-configured community dashboards you can import:

1. **Django Metrics** (ID: 9528)
   - Monitors Django application metrics, request rates, response times
   - Perfect for tracking API performance

2. **PostgreSQL Database** (ID: 9628)
   - Database connection pool, query performance, table statistics
   - Essential for database health monitoring

3. **Nginx** (ID: 12708) - _Requires nginx-prometheus-exporter_
   - Nginx request rates, connection stats, response codes

4. **Redis Dashboard** (ID: 11835)
   - Redis memory usage, hit rate, connected clients
   - Useful for cache and session monitoring

**How to Import a Dashboard:**

1. In Grafana, click **"+" (Create)** → **Import**
2. Enter the dashboard ID (e.g., `9528` for Django Dashboard)
3. Click **Load**
4. Select your **Prometheus** data source from the dropdown
5. Customize folder and UID if needed
6. Click **Import**

**Custom Django Dashboard Tips:**

- After importing dashboard 9528, verify the metrics are appearing
- If no data is shown, check that `/metrics/metrics` endpoint is accessible
- You can create custom panels by clicking **Add panel** on any dashboard
- Export your customized dashboards as JSON for backup

---

### 🤖 Claude Code Integration

This project includes comprehensive
[Claude Code](https://docs.claude.com/claude-code) configuration for AI-assisted
development.

#### Features

- **Custom Agents**: 4 specialized agents (Django Expert, Code Reviewer, Backend
  Architect, Python Pro)
- **Memory MCP Server**: Persistent context across sessions
- **Token Optimization**: Configured for maximum efficiency
- **Bilingual Support**: All agents understand PT-BR/EN project standards

#### Quick Start

```bash
# Claude Code is pre-configured in .claude/
# View configuration:
cat .claude/README.md
cat .claude/context.md

# Available agents in .claude/agents/:
# - django-expert.md - Django/DRF specialist
# - code-reviewer.md - Code quality and security
# - backend-architect.md - System architecture
# - python-pro.md - Python optimization
```

#### Usage Examples

```bash
# In Claude Code conversation:
"Use django-expert to create a new API endpoint"
"Use code-reviewer to check my changes"
"Use backend-architect to design the caching strategy"
```

**Documentation**: See [`.claude/README.md`](.claude/README.md) for complete
guide.

---

### 🔒 Security Best Practices

#### Environment Variables

**Never commit `.env` files!** Always use `.env.example` as template.

**Production Checklist:**

- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY` (50+ characters)

  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set `SECURE_SSL_REDIRECT=True`
- [ ] Configure `SESSION_COOKIE_SECURE=True`
- [ ] Configure `CSRF_COOKIE_SECURE=True`
- [ ] Set up Sentry or error monitoring
- [ ] Use strong database passwords
- [ ] Configure proper CORS origins
- [ ] Enable rate limiting in Nginx
- [ ] Set up SSL certificates (Let's Encrypt recommended)

#### Security Headers

The Nginx configuration includes:

- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Strict-Transport-Security` (in production with SSL)

#### Rate Limiting

Built-in rate limiting:

- API routes: 10 requests/second (burst 20)
- General routes: 100 requests/second (burst 50)

**Django-Level Rate Limiting**

In addition to Nginx-level limiting, the project includes a `@rate_limit`
decorator for more granular control within your views. This decorator is
production-ready and uses Redis to track requests, making it suitable for
multi-process and multi-server environments.

**Usage:**

```python
from src.core.decorators import rate_limit

@rate_limit(max_requests=5, period=60) # 5 requests per minute
def my_sensitive_api_view(request):
    ...
```

This is ideal for protecting specific endpoints, applying different limits per
user, or other custom logic.

---

### 🐛 Troubleshooting

#### Common Issues

**Port Already in Use:**

```bash
# Check what's using port 5432
lsof -i :5432  # macOS/Linux
netstat -ano | findstr :5432  # Windows

# Change port in docker-compose.yml if needed
ports:
  - "5433:5432"  # Use different host port
```

**Database Connection Issues:**

```bash
# Wait for database to be ready
docker-compose exec db pg_isready -U ${POSTGRES_USER}

# Check database logs
docker-compose logs db
```

**Migrations Not Applied:**

```bash
# Ensure database is healthy, then run
docker-compose exec web python manage.py migrate --noinput
```

**Static Files Not Served:**

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --no-input

# Check Nginx logs
docker-compose logs nginx
```

**Redis Connection Issues:**

```bash
# Check Redis is running
docker-compose exec redis redis-cli ping

# Check Redis logs
docker-compose logs redis
```

---

### 📚 Project Structure

```
django_base/
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD pipeline
├── docs/                           # Project documentation
│   ├── JWT_AUTHENTICATION.md       # JWT authentication guide
│   └── SSL_HTTPS_SETUP.md          # SSL/HTTPS configuration guide (NEW v1.2.0)
├── grafana/                        # Grafana configuration (NEW v1.2.0)
│   ├── dashboards/                 # Pre-configured dashboards
│   └── provisioning/               # Auto-provisioning config
├── k8s/                            # Kubernetes manifests (NEW v1.2.0)
│   ├── base/                       # Base K8s manifests (12 files)
│   ├── dev/                        # Development overlay
│   ├── prod/                       # Production overlay
│   └── README.md                   # Complete K8s deployment guide
├── nginx/
│   ├── Dockerfile                  # Nginx image build
│   └── nginx.conf                  # Nginx configuration (enhanced security headers v1.2.0)
├── scripts/                        # Operational scripts (NEW v1.2.0)
│   ├── backup_database.sh          # Professional database backup script
│   ├── restore_database.sh         # Safe database restoration script
│   └── README.md                   # Complete backup/restore documentation
├── src/
│   ├── core/                       # Main Django app
│   │   ├── management/
│   │   │   └── commands/           # Custom management commands
│   │   ├── migrations/             # Database migrations
│   │   ├── templatetags/
│   │   │   └── core_tags.py        # 23 custom template tags & filters
│   │   ├── models.py               # 4 models: Product, UserProfile, Category, Tag
│   │   ├── forms.py                # 5 forms: Login, Register, UserProfile, UserUpdate, ProductForm
│   │   ├── views.py                # Views with JWT token endpoints (enhanced v1.2.0)
│   │   ├── viewsets.py             # 4 DRF ViewSets with custom actions
│   │   ├── serializers.py          # 10 DRF Serializers (detail + list)
│   │   ├── validators.py           # 8 custom validators (phone, CPF, image, etc.)
│   │   ├── decorators.py           # 15 decorators (permissions, cache, logging)
│   │   ├── mixins.py               # 13 mixins (model + view utilities)
│   │   ├── signals.py              # Django signals (UserProfile auto-creation)
│   │   ├── tasks.py                # Background tasks (Django Q)
│   │   ├── urls.py                 # URL routing
│   │   ├── admin.py                # Enhanced admin interface
│   │   └── tests.py                # Test cases (7 tests)
│   └── django_base/
│       ├── settings/               # Modular settings
│       │   ├── __init__.py         # Auto-detects environment
│       │   ├── base.py             # Shared settings
│       │   ├── dev.py              # Development settings (with validation v1.2.0)
│       │   ├── prod.py             # Production settings (with validation v1.2.0)
│       │   └── env_validator.py    # Environment validation module (NEW v1.2.0)
│       ├── urls.py                 # Main URL routing
│       ├── wsgi.py                 # WSGI entry point
│       └── asgi.py                 # ASGI entry point
├── templates/                      # Django templates
│   ├── base/
│   │   └── base.html               # Base template with navbar, messages, footer
│   ├── auth/
│   │   ├── home.html               # Homepage with features showcase
│   │   ├── login.html              # Login form with animations
│   │   ├── register.html           # Registration form
│   │   ├── profile.html            # User profile edit page
│   │   └── project_info.html       # Project information page
│   ├── core/
│   │   └── product/
│   │       ├── products.html         # Product page with product management
│   │       └── product_create.html   # Page for creating a new product
│   ├── health/
│   │   └── health_check.html       # Visual health check page
│   ├── partials/                   # Reusable partial templates
│   └── components/
│       ├── card.html               # Bootstrap card component
│       └── pagination.html         # Pagination controls
├── locale/                         # Internationalization (i18n)
│   ├── en/LC_MESSAGES/             # English translations
│   └── pt_BR/LC_MESSAGES/          # Portuguese (Brazil) translations
├── backups/                        # Database backups directory (gitignored)
│   └── database/                   # Automated backup storage
├── logs/                           # Application logs (gitignored)
├── staticfiles/                    # Collected static files (gitignored)
├── mediafiles/                     # User uploads (gitignored)
├── docker-compose.yml              # Production compose
├── docker-compose.dev.yml          # Development overrides
├── Dockerfile                      # Multi-stage Docker build
├── Makefile                        # 60+ commands for dev/prod/K8s (NEW v1.2.0)
├── pyproject.toml                  # Dependencies & tool config
├── .env.example                    # Environment variables template
├── .pre-commit-config.yaml         # Pre-commit hooks (20+ checks)
├── prometheus.yml                  # Prometheus configuration (enhanced v1.2.0)
├── README.md                       # This file
├── CHANGELOG.md                    # Project changelog (updated v1.2.0)
├── TODOLIST.md                     # Development roadmap (updated v1.2.0)
└── CONTRIBUTING.md                 # Contribution guidelines
```

---

### 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run linters and tests

   ```bash
   pre-commit run --all-files
   python manage.py test src
   ```

5. Commit your changes (`git commit -m 'Add: amazing feature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

#### Code Standards

- Use Ruff for formatting (`ruff format .`)
- Pass all linters (`ruff check .`)
- Add tests for new features
- Maintain coverage above 80%
- **Write ALL docstrings and comments in BOTH English and Portuguese**
- Follow Django best practices
- Add detailed explanations for complex logic

---

### 📄 License

This project is licensed under the MIT License - see the LICENSE file for
details.

---

### 🙏 Acknowledgments

- Django Software Foundation
- All the amazing open-source libraries used in this project
- The Python community

---

## 🇧🇷 Português

Este é um projeto base moderno e pronto para produção para desenvolvimento
Django, totalmente configurado com Docker, segurança reforçada, settings
modulares e observabilidade completa. A estrutura segue as melhores práticas
para escalabilidade, manutenibilidade e deploy profissional.

### 🛠️ Stack Tecnológica

#### Tecnologias Principais

- **Servidor Web:** [Nginx](https://nginx.org/en/docs/) (com rate limiting,
  gzip, headers de segurança)
- **Servidor de Aplicação:** [Gunicorn](https://docs.gunicorn.org/) (WSGI
  multi-worker)
- **Backend:** [Django](https://docs.djangoproject.com/) 5.2+,
  [Django REST Framework](https://www.django-rest-framework.org/)
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/docs/) 15 (com
  connection pooling)
- **Cache & Fila:** [Redis](https://redis.io/docs/) 7 (para cache, sessões,
  Django Q)
- **Gerenciador de Pacotes:** [uv](https://docs.astral.sh/uv/) (gerenciador de
  pacotes Python ultrarrápido)
- **Tarefas em Background:** [Django Q2](https://django-q2.readthedocs.io/)
  (`django-q2`)
- **Recursos API:** [CORS](https://pypi.org/project/django-cors-headers/),
  [DRF Spectacular](https://drf-spectacular.readthedocs.io/) (OpenAPI/Swagger),
  [django-filter](https://django-filter.readthedocs.io/)
- **Containerização:** [Docker](https://docs.docker.com/) &
  [Docker Compose](https://docs.docker.com/compose/) (builds multi-stage),
  [Kubernetes](https://kubernetes.io/docs/)
- **Qualidade de Código:** [Ruff](https://docs.astral.sh/ruff/)
  linter/formatter, [pre-commit](https://pre-commit.com/) hooks,
  [Bandit](https://bandit.readthedocs.io/) segurança
- **Testes:**
  [django.test](https://docs.djangoproject.com/en/stable/topics/testing/) com
  [coverage](https://coverage.readthedocs.io/),
  [Factory Boy](https://factoryboy.readthedocs.io/)
- **Rastreamento de Erros:**
  [Sentry](https://docs.sentry.io/platforms/python/integrations/django/) para
  monitoramento de erros e performance
- **Observabilidade:** [Prometheus](https://prometheus.io/docs/) &
  [Grafana](https://grafana.com/docs/) dashboards com exporters
- **Configuração:** [python-decouple](https://pypi.org/project/python-decouple/)
  com suporte abrangente a `.env`
- **Ferramentas de Desenvolvimento:**
  [django-extensions](https://django-extensions.readthedocs.io/),
  [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/),
  [watchdog](https://python-watchdog.readthedocs.io/) para hot-reloading,
  [Makefile](https://www.gnu.org/software/make/manual/make.html) (60+ comandos)
- **Assistente IA:** [Claude Code](https://docs.claude.com/claude-code)
  integração com agentes customizados e servidor MCP

### ✨ Funcionalidades Principais

#### Infraestrutura & Arquitetura

- ✅ **Settings Modulares:** `base.py`, `dev.py`, `prod.py` separados para
  configuração por ambiente
- ✅ **Validação de Ambiente:** Validação automática de configuração crítica na
  inicialização
- ✅ **Segurança Reforçada:** HSTS, redirecionamento SSL, cookies seguros,
  headers de segurança, rate limiting
- ✅ **Pronto para Produção:** Builds Docker multi-stage, usuário não-root,
  health checks, SSL/HTTPS pronto
- ✅ **Suporte Kubernetes:** Manifestos K8s completos com Kustomize overlays
  para ambientes dev/prod
- ✅ **Sistema de Backup:** Scripts profissionais de backup/restore com
  políticas de retenção
- ✅ **Integração Redis:** Cache, armazenamento de sessão, backend de fila de
  tarefas
- ✅ **Observabilidade Aprimorada:** Prometheus + Grafana com exporters para
  PostgreSQL, Redis e Nginx
- ✅ **Produtividade do Desenvolvedor:** Makefile com 60+ comandos (18 para
  Kubernetes)
- ✅ **Pre-commit Hooks:** 20+ hooks incluindo Ruff, Bandit, detect-secrets,
  django-upgrade
- ✅ **CI/CD Pronto:** Pipeline GitHub Actions com linting e testes
- ✅ **Documentação Bilíngue:** Comentários completos PT-BR/EN em todo o código
- ✅ **Otimização de Queries:** Todos os ViewSets otimizados com
  select_related/prefetch_related
- ✅ **Suporte a Dark Mode:** Toggle elegante de tema claro/escuro com
  persistência em localStorage
- ✅ **Internacionalização (i18n):** Suporte multi-idioma (EN/PT-BR) com seletor
  de idioma na navbar
- ✅ **Reorganização de Templates:** Estrutura de templates limpa e organizada
  seguindo melhores práticas Django
- ✅ **Padrão Soft Delete:** Todos os modelos usam exclusão suave com mixins
  para integridade de dados
- ✅ **Setup Multi-Plataforma:** Suporte Windows com scripts PowerShell (.ps1) e
  Batch (.bat)
- ✅ **Página Info Aprimorada:** Documentação completa da stack tecnológica com
  links
- ✅ **Rastreamento de Erros:** Integração Sentry com traces e profiling
- ✅ **Debug Toolbar:** django-debug-toolbar para profiling em desenvolvimento
- ✅ **Factories de Teste:** Factory Boy para geração de dados de teste
  realistas
- ✅ **Testes de Integração:** Testes completos de fluxos de trabalho da API
- ✅ **Integração Claude Code:** Agentes customizados (Django Expert, Code
  Reviewer, Backend Architect, Python Pro) + servidor Memory MCP

#### Recursos de Portfólio (Autenticação & Gerenciamento de Usuários)

- ✅ **Sistema de Autenticação Completo:** Login, registro, logout,
  gerenciamento de perfil
- ✅ **Perfis de Usuário:** Modelo de usuário estendido com avatar, bio,
  telefone, localização, website
- ✅ **5 Formulários Customizados:** LoginForm com remember_me, RegisterForm com
  validação, UserProfileForm, UserUpdateForm, ProductForm
- ✅ **Templates Bootstrap 5:** UI responsiva com páginas home, login, registro,
  perfil, listagem de produtos, criação de produtos
- ✅ **Criação Automática de Perfil:** Signals do Django criam automaticamente
  UserProfile quando User é criado
- ✅ **Gerenciamento de Produtos:** CRUD completo para produtos com filtragem
  por categoria/tag

#### Modelos de Dados & Relacionamentos

- ✅ **4 Models:** Product, UserProfile, Category (hierárquico), Tag
- ✅ **Relacionamentos de Modelo:** OneToOne, ForeignKey, ManyToMany,
  Self-referencing FK
- ✅ **Padrão Soft Delete:** Desativar ao invés de deletar para integridade de
  dados
- ✅ **Lógica de Negócio:** Properties, métodos customizados, class methods em
  models
- ✅ **Validadores de Modelo:** Telefone, CPF, tamanho/dimensões de imagem,
  datas, URLs

#### API REST & Documentação

- ✅ **Documentação API:** OpenAPI/Swagger auto-gerado com drf-spectacular
- ✅ **4 DRF ViewSets:** Product, Category, Tag, UserProfile com CRUD completo
- ✅ **10 Serializers:** Serializers de detalhe e lista para todos os models
- ✅ **Actions Customizadas:** /tree/ para categorias, /popular/ para tags, /me/
  para perfis
- ✅ **Filtragem & Busca:** Integração django-filter com busca, ordenação,
  paginação

#### Sistema de Templates & Componentes UI

- ✅ **23 Template Tags & Filters:** currency, percentage, time_ago, file_size,
  badges, icons, alerts
- ✅ **Componentes Reutilizáveis:** Componente card, paginação, layouts
  responsivos
- ✅ **Páginas de Produtos:** Listagem com filtros (categoria, tags, faixa de
  preço) + formulário de criação
- ✅ **Internacionalização (i18n):** Suporte completo PT-BR/EN com tags
  {% trans %} em todos os templates
- ✅ **Health Check Visual:** Página de monitoramento com auto-atualização e
  status em tempo real
- ✅ **Melhorias UI:** Efeitos hover, auto-dismiss de alertas, tema verde
  customizado (#198754)
- ✅ **Bootstrap 5.3 Tema Verde:** Cor primária verde (#198754) substituindo
  azul padrão
- ✅ **Suporte HTMX:** Interações dinâmicas sem complexidade JavaScript

#### Ferramentas de Desenvolvedor & Utilitários

- ✅ **8 Validadores Customizados:** Telefone, CPF, validação de imagem,
  validação de data, validadores regex
- ✅ **15 Decoradores:** Permissões, cache, logging, limitação de taxa pronta
  para produção baseada em Redis, AJAX, resposta JSON
- ✅ **13 Mixins:** Mixins de modelo (timestamps, soft delete, rastreamento de
  usuário) + mixins de view (permissões, paginação, AJAX)
- ✅ **Django Signals:** Auto-criação de modelos relacionados com tratamento de
  erros
- ✅ **Customização Admin:** Interface admin aprimorada com fieldsets e filtros
  customizados

### 🏁 Executando o Projeto (Docker)

#### 💻 Modo Desenvolvimento (perfil `dev`)

Este modo é para desenvolvimento ativo com hot-reloading, modo debug e logging
verboso.

1. **Configuração Automatizada (Recomendado):**

   **Linux/macOS:**

   ```bash
   # Clone o repositório e entre no diretório
   git clone <url-do-seu-repositorio> && cd django_base

   # Execute o script de configuração automatizada
   ./setup.sh
   ```

   **Windows (PowerShell - Recomendado):**

   ```powershell
   # Clone o repositório e entre no diretório
   git clone <url-do-seu-repositorio>
   cd django_base

   # Execute o script de configuração automatizada
   .\setup.ps1
   ```

   **Windows (Prompt de Comando):**

   ```cmd
   # Clone o repositório e entre no diretório
   git clone <url-do-seu-repositorio>
   cd django_base

   # Execute o script de configuração automatizada
   setup.bat
   ```

   **Isso configura automaticamente:**
   - Criação do arquivo .env
   - Build e inicialização do Docker
   - Migrações do banco de dados
   - Criação de superusuário (admin/admin)
   - Seed do banco de dados
   - Compilação de traduções (PT-BR/EN)
   - Execução de testes com coverage

   **Opções disponíveis:**
   - `--quick` ou `-Quick`: Pular testes e pre-commit (setup mais rápido)
   - `--skip-build` ou `-SkipBuild`: Pular build do Docker (use se as imagens já
     existem)
   - `--help` ou `-Help`: Mostrar todas as opções disponíveis

2. **Configuração Manual (Alternativa):**

   ```bash
   # Clone o repositório e entre no diretório
   git clone <url-do-seu-repositorio> && cd django_base

   # Crie o arquivo de ambiente
   cp .env.example .env

   # Construa e inicie todos os serviços
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d --build

   # Execute as migrações do banco de dados
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate

   # Crie um superusuário
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

   # Popule o banco de dados
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py seed_database

   # Compile traduções i18n
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py compilemessages
   ```

3. **Para Iniciar o Servidor de Desenvolvimento:** _Este comando irá anexar ao
   seu terminal e mostrar logs ao vivo. Pressione `Ctrl + C` para parar._

   ```bash
   # Iniciar em primeiro plano (com logs)
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up

   # Ou iniciar em background
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d
   ```

4. **Para Parar o Servidor de Desenvolvimento:**

   ```bash
   # Parar todos os serviços
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down
   ```

#### 🚀 Modo Produção (perfil `prod`)

Este modo executa a stack de produção com Nginx, Gunicorn, cache Redis e
segurança reforçada.

1. **Configuração Automatizada (Recomendado):**

   ```bash
   # Configure .env para produção primeiro!
   cp .env.example .env
   # Edite .env: Defina DEBUG=False, SECRET_KEY forte, ALLOWED_HOSTS, etc.

   # Execute o script de configuração de produção
   ./setup-prod.sh
   # ou
   make setup-prod

   # Isso configura automaticamente:
   # - Validação de ambiente (DEBUG, SECRET_KEY, etc.)
   # - Build e inicialização do Docker
   # - Migrações do banco de dados
   # - Coleta de arquivos estáticos
   # - Compilação de traduções
   # - Verificações de saúde
   # - Lembrete de checklist de segurança
   ```

2. **Configuração Manual (Alternativa):**

   ```bash
   # Copie e edite .env com valores de produção
   cp .env.example .env
   # IMPORTANTE: Defina DEBUG=False, configure SECRET_KEY, ALLOWED_HOSTS, etc.

   # Construa e inicie todos os serviços de produção
   docker-compose --profile prod up -d --build

   # Execute as migrações
   docker-compose --profile prod exec web python manage.py migrate

   # Colete arquivos estáticos para o Nginx
   docker-compose --profile prod exec web python manage.py collectstatic --no-input

   # Compile traduções i18n
   docker-compose --profile prod exec web python manage.py compilemessages

   # Crie um superusuário (manual)
   docker-compose --profile prod exec web python manage.py createsuperuser
   ```

3. **Para Parar a Stack de Produção:**

   ```bash
   # Parar todos os serviços
   docker-compose --profile prod down
   # ou
   make prod-down
   ```

#### 🌐 Pontos de Acesso

Após iniciar, seu ambiente estará disponível em:

**Frontend (Templates):**

- **Página Inicial:** `http://localhost:8000/`
- **Login:** `http://localhost:8000/login/`
- **Registro:** `http://localhost:8000/register/`
- **Perfil:** `http://localhost:8000/profile/` (requer autenticação)
- **Produtos:** `http://localhost:8000/products/` (catálogo com filtros)
- **Criar Produto:** `http://localhost:8000/products/create/` (requer
  autenticação)
- **Admin Django:** `http://localhost:8000/admin/`

**API (REST Framework):**

- **API Root:** `http://localhost:8000/api/v1/`
- **Produtos:** `http://localhost:8000/api/v1/products/`
- **Categorias:** `http://localhost:8000/api/v1/categories/`
  - **Árvore de Categorias:** `http://localhost:8000/api/v1/categories/tree/`
- **Tags:** `http://localhost:8000/api/v1/tags/`
  - **Tags Populares:** `http://localhost:8000/api/v1/tags/popular/`
- **Perfis de Usuário:** `http://localhost:8000/api/v1/profiles/`
  - **Meu Perfil:** `http://localhost:8000/api/v1/profiles/me/` (requer
    autenticação)
- **Info da API:** `http://localhost:8000/api/info/`

**Documentação:**

- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`
- **Schema OpenAPI:** `http://localhost:8000/api/schema/`

**Monitoramento & Saúde:**

- **Health Check (API):** `http://localhost:8000/health/`
- **Health Check (Visual):** `http://localhost:8000/health-status/`
- **Métricas Prometheus:** `http://localhost:8000/metrics/metrics`
- **Prometheus:** `http://localhost:9090`
- **Grafana:** `http://localhost:3000` (login padrão: `admin`/`admin`)

**Credenciais de Teste (Auto-Criadas em Dev):**

- **Superuser:** `admin` / `admin123`
- **Test User:** `testuser` / `test123` (tem perfil automaticamente criado)

---

### 💻 Desenvolvimento Local (Sem Docker)

#### Pré-requisitos

- Python 3.11+
- Servidor PostgreSQL rodando localmente
- Servidor Redis rodando localmente (opcional, para cache/fila)
- `uv` instalado (recomendado) ou `pip`

#### Passos

1. **Clone o repositório e entre nele:**

   ```bash
   git clone <url-do-seu-repositorio> && cd django_base
   ```

2. **Configure o arquivo de ambiente (`.env`):** Copie `.env.example` para
   `.env`. **Importante:** Mude `POSTGRES_HOST=db` para
   `POSTGRES_HOST=localhost` e `REDIS_HOST=redis` para `REDIS_HOST=localhost`.

   ```bash
   cp .env.example .env
   # Agora edite .env e atualize os hosts do banco/redis
   ```

3. **Instale as dependências com `uv` (Recomendado):**

   ```bash
   # Crie um ambiente virtual
   uv venv

   # Ative-o (macOS/Linux)
   source .venv/bin/activate

   # Ative-o (Windows PowerShell)
   .venv\Scripts\Activate.ps1

   # ou Windows (Prompt de Comando)
   .venv\Scripts\activate.bat

   # Instale todas as dependências (produção + dev)
   uv sync --dev
   ```

4. **Execute Migrações e Crie Superusuário:**

   ```bash
   # Defina o módulo de settings do Django para desenvolvimento
   export DJANGO_SETTINGS_MODULE=django_base.settings.dev  # Linux/macOS
   # ou
   set DJANGO_SETTINGS_MODULE=django_base.settings.dev     # Windows CMD
   # ou
   $env:DJANGO_SETTINGS_MODULE="django_base.settings.dev"  # Windows PowerShell

   # Execute as migrações
   python manage.py migrate

   # Crie um superusuário
   python manage.py createsuperuser
   ```

5. **Execute o Servidor de Desenvolvimento:**

   ```bash
   # Com django-extensions (debugger aprimorado)
   python manage.py runserver_plus

   # Ou runserver padrão
   python manage.py runserver
   ```

---

### 📖 Fluxo de Trabalho de Desenvolvimento

#### Configurações de Ambiente

Este projeto usa settings modulares para diferentes ambientes:

- **`settings/base.py`**: Configuração compartilhada entre todos os ambientes
- **`settings/dev.py`**: Configurações específicas de desenvolvimento
  (DEBUG=True, email no console, cache dummy)
- **`settings/prod.py`**: Configurações de produção (segurança reforçada, cache
  Redis, logging)

Para alternar entre ambientes, defina a variável `DJANGO_SETTINGS_MODULE`:

```bash
# Desenvolvimento (padrão)
export DJANGO_SETTINGS_MODULE=django_base.settings.dev

# Produção
export DJANGO_SETTINGS_MODULE=django_base.settings.prod
```

#### Como Adicionar uma Nova Biblioteca

O arquivo `pyproject.toml` é a fonte da verdade para as dependências.

**Com Docker:**

1. **Execute o comando de instalação dentro do container `web`:**

   ```bash
   # Para uma dependência de produção
   docker-compose exec web uv add "algum-pacote"

   # Para uma dependência de desenvolvimento (como ferramenta de teste)
   docker-compose exec web uv add "algum-pacote-dev" --dev
   ```

2. **Para tornar a mudança permanente na imagem**, reconstrua-a:

   ```bash
   docker-compose build
   ```

**Localmente (sem Docker):**

```bash
# Para uma dependência de produção
uv add "algum-pacote"

# Para uma dependência de desenvolvimento
uv add "algum-pacote-dev" --dev
```

#### Como Criar um Novo App

1. Certifique-se de que seu ambiente de **desenvolvimento** está rodando.
2. Execute o comando `startapp`:

   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py startapp meu_novo_app
   ```

3. Mova a pasta `meu_novo_app` para o diretório `src/`.
4. Adicione `'meu_novo_app'` ao `INSTALLED_APPS` em
   `src/django_base/settings/base.py`.
5. Crie e configure o `urls.py` do app.

#### Pre-commit Hooks

Este projeto usa pre-commit hooks abrangentes para qualidade de código:

```bash
# Instale os hooks pre-commit (apenas uma vez)
pre-commit install

# Execute os hooks manualmente em todos os arquivos
pre-commit run --all-files

# Atualize os hooks para as versões mais recentes
pre-commit autoupdate
```

Os hooks incluem:

- **Ruff** (linting + formatação)
- **Bandit** (linting de segurança)
- **detect-secrets** (prevenir commits de secrets)
- **django-upgrade** (melhores práticas Django)
- **markdownlint** (formatação Markdown)
- E mais de 15 outras verificações de qualidade

---

### 🚀 Comandos do Dia-a-Dia (Docker)

#### Comandos de Desenvolvimento

```bash
# Iniciar ambiente dev com logs ao vivo
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up

# Iniciar em background
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d

# Ver logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f web

# Acessar shell do container
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web bash

# Executar migrações
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate

# Compilar traduções
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py compilemessages

# Criar superusuário
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Executar testes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py test core

# Executar testes com cobertura
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage run manage.py test core
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage report

# Executar linting
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff check .

# Formatar código
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff format .

# Parar todos os serviços
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down
```

#### Comandos de Produção

```bash
# Iniciar stack de produção
docker-compose --profile prod up -d

# Ver logs
docker-compose --profile prod logs -f

# Executar migrações
docker-compose --profile prod exec web python manage.py migrate

# Compilar traduções
docker-compose --profile prod exec web python manage.py compilemessages

# Coletar arquivos estáticos
docker-compose --profile prod exec web python manage.py collectstatic --no-input

# Acessar shell do container
docker-compose --profile prod exec web bash

# Reiniciar serviços
docker-compose --profile prod restart

# Parar todos os serviços
docker-compose --profile prod down
```

#### Comandos de Banco de Dados

```bash
# Criar backup do banco de dados
docker-compose exec db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup.sql

# Restaurar backup do banco de dados
docker-compose exec -T db psql -U ${POSTGRES_USER} ${POSTGRES_DB} < backup.sql

# Acessar shell PostgreSQL
docker-compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# Verificar se banco está pronto
docker-compose exec db pg_isready -U ${POSTGRES_USER}
```

#### Comandos Redis

```bash
# Acessar CLI do Redis
docker-compose exec redis redis-cli

# Testar conexão Redis
docker-compose exec redis redis-cli ping

# Verificar informações do Redis
docker-compose exec redis redis-cli INFO

# Limpar todos os dados do Redis (CUIDADO!)
docker-compose exec redis redis-cli FLUSHALL
```

---

### ☸️ Deploy Kubernetes

Este projeto inclui manifestos Kubernetes completos para deploy em qualquer
cluster Kubernetes.

#### Início Rápido

**Configuração Automatizada (Recomendado):**

```bash
# Configuração de desenvolvimento (build da imagem + deploy)
./setup-k8s.sh
# ou
make setup-k8s

# Configuração de produção (build da imagem + deploy)
./setup-k8s.sh --prod
# ou
make setup-k8s-prod
```

**Deploy Manual:**

```bash
# Deploy em desenvolvimento
make k8s-dev-deploy

# Deploy em produção (requer confirmação)
make k8s-prod-deploy

# Verificar status do deployment
make k8s-status

# Ver logs
make k8s-logs

# Acessar aplicação via port forward
kubectl port-forward -n django-base svc/dev-nginx-service 8000:80
```

#### Recursos

- **Manifestos Completos:** 12 manifestos base (namespace, configmaps, secrets,
  PVCs, deployments, services, ingress)
- **Kustomize Overlays:** Configurações separadas para ambientes dev e prod
- **Pronto para Auto-Scaling:** Configuração HPA incluída
- **Health Checks:** Probes de liveness e readiness para todos os serviços
- **Limites de Recursos:** Limites de CPU e memória definidos
- **RBAC:** Service account do Prometheus com cluster role
- **Armazenamento Persistente:** PVCs para PostgreSQL, Redis, arquivos
  static/media, Prometheus, Grafana

#### Serviços Deployados

- Aplicação web Django (com init containers para migrations/collectstatic)
- Banco de dados PostgreSQL
- Cache Redis
- Nginx reverse proxy
- Monitoramento Prometheus
- Dashboards Grafana

Para documentação completa do Kubernetes, veja [`k8s/README.md`](k8s/README.md).

---

### 🧪 Testes

#### Executar Testes (Docker)

```bash
# Executar todos os testes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py test core

# Executar com cobertura
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage run manage.py test core
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage report

# Gerar relatório HTML de cobertura
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage html
# Relatório disponível em: htmlcov/index.html

# Executar classe de teste específica
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py test core.tests.TestProduct

# Executar com saída verbosa
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py test core --verbosity=2
```

#### Executar Testes (Local - Sem Docker)

```bash
# Executar todos os testes
python manage.py test core

# Executar com cobertura
coverage run manage.py test core
coverage report
coverage html  # Gerar relatório HTML

# Executar arquivo de teste específico
python manage.py test core.tests

# Executar com pytest (se instalado)
pytest src/
```

#### Linting e Formatação (Docker)

```bash
# Verificar código com Ruff
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff check .

# Auto-corrigir problemas
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff check --fix .

# Formatar código
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web ruff format .

# Executar todos os hooks pre-commit
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web pre-commit run --all-files
```

#### Linting e Formatação (Local - Sem Docker)

```bash
# Verificar código com Ruff
ruff check .

# Auto-corrigir problemas
ruff check --fix .

# Formatar código
ruff format .

# Executar todos os hooks pre-commit
pre-commit run --all-files
```

---

### 📊 Monitoramento & Observabilidade

#### Prometheus

Acesse o Prometheus em `http://localhost:9090` para:

- Consultar métricas
- Configurar alertas
- Monitorar performance da aplicação

Métricas principais disponíveis:

- Django: `django_http_requests_total`, `django_http_responses_total`,
  `django_http_requests_latency_seconds`, `django_db_query_count`
- PostgreSQL: Pools de conexão, performance de queries, estatísticas de tabelas
- Redis: Uso de memória, taxa de acerto, clientes conectados
- Nginx: Taxas de requisição, estatísticas de conexão, códigos de resposta

#### Grafana

Acesse o Grafana em `http://localhost:3000` (padrão: `admin`/`admin`)

Os dashboards Grafana são **automaticamente provisionados** na inicialização com
datasources pré-configurados.

**Configuração Inicial:**

1. Após fazer login, altere a senha padrão quando solicitado
2. Navegue para **Configuration** (⚙️) → **Data Sources**
3. Clique em **Add data source** → Selecione **Prometheus**
4. Configure o Prometheus:
   - **Name:** `Prometheus`
   - **URL:** `http://prometheus:9090`
   - Clique em **Save & Test** (você deve ver "Data source is working")

**Dashboards Recomendados:**

Dashboards da comunidade pré-configurados que você pode importar:

1. **Django Metrics** (ID: 9528)
   - Monitora métricas da aplicação Django, taxas de requisição, tempos de
     resposta
   - Perfeito para rastrear performance da API

2. **PostgreSQL Database** (ID: 9628)
   - Pool de conexões do banco, performance de queries, estatísticas de tabelas
   - Essencial para monitoramento da saúde do banco de dados

3. **Nginx** (ID: 12708) - _Requer nginx-prometheus-exporter_
   - Taxas de requisição Nginx, estatísticas de conexão, códigos de resposta

4. **Redis Dashboard** (ID: 11835)
   - Uso de memória Redis, taxa de acerto, clientes conectados
   - Útil para monitoramento de cache e sessões

**Como Importar um Dashboard:**

1. No Grafana, clique em **"+" (Create)** → **Import**
2. Digite o ID do dashboard (ex: `9528` para Django Dashboard)
3. Clique em **Load**
4. Selecione sua fonte de dados **Prometheus** no dropdown
5. Personalize pasta e UID se necessário
6. Clique em **Import**

**Dicas para Dashboard Django Personalizado:**

- Após importar o dashboard 9528, verifique se as métricas estão aparecendo
- Se nenhum dado for exibido, verifique se o endpoint `/metrics/metrics` está
  acessível
- Você pode criar painéis personalizados clicando em **Add panel** em qualquer
  dashboard
- Exporte seus dashboards personalizados como JSON para backup

---

### 🔒 Melhores Práticas de Segurança

#### Variáveis de Ambiente

**Nunca faça commit de arquivos `.env`!** Sempre use `.env.example` como
template.

**Checklist de Produção:**

- [ ] Defina `DEBUG=False`
- [ ] Gere uma `SECRET_KEY` forte (50+ caracteres)

  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

- [ ] Configure `ALLOWED_HOSTS` com seu domínio
- [ ] Defina `SECURE_SSL_REDIRECT=True`
- [ ] Configure `SESSION_COOKIE_SECURE=True`
- [ ] Configure `CSRF_COOKIE_SECURE=True`
- [ ] Configure Sentry ou monitoramento de erros
- [ ] Use senhas fortes para o banco de dados
- [ ] Configure origens CORS adequadas
- [ ] Habilite rate limiting no Nginx
- [ ] Configure certificados SSL (Let's Encrypt recomendado)

#### Headers de Segurança

A configuração do Nginx inclui:

- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Strict-Transport-Security` (em produção com SSL)

#### Rate Limiting

Rate limiting integrado:

- Rotas de API: 10 requisições/segundo (burst 20)
- Rotas gerais: 100 requisições/segundo (burst 50)

**Limitação de Taxa a Nível de Django**

Além da limitação a nível de Nginx, o projeto inclui um decorador `@rate_limit`
para um controle mais granular dentro de suas views. Este decorador é pronto
para produção e usa Redis para rastrear requisições, tornando-o adequado para
ambientes com múltiplos processos e servidores.

**Uso:**

```python
from src.core.decorators import rate_limit

@rate_limit(max_requests=5, period=60) # 5 requisições por minuto
def my_sensitive_api_view(request):
    ...
```

Isso é ideal para proteger endpoints específicos, aplicar limites diferentes por
usuário, ou outra lógica customizada.

---

### 🐛 Solução de Problemas

#### Problemas Comuns

**Porta Já em Uso:**

```bash
# Verificar o que está usando a porta 5432
lsof -i :5432  # macOS/Linux
netstat -ano | findstr :5432  # Windows

# Altere a porta no docker-compose.yml se necessário
ports:
  - "5433:5432"  # Use porta host diferente
```

**Problemas de Conexão com Banco de Dados:**

```bash
# Aguarde o banco de dados estar pronto
docker-compose exec db pg_isready -U ${POSTGRES_USER}

# Verifique os logs do banco de dados
docker-compose logs db
```

**Migrações Não Aplicadas:**

```bash
# Certifique-se de que o banco está saudável, então execute
docker-compose exec web python manage.py migrate --noinput
```

**Arquivos Estáticos Não Servidos:**

```bash
# Colete arquivos estáticos
docker-compose exec web python manage.py collectstatic --no-input

# Verifique logs do Nginx
docker-compose logs nginx
```

**Problemas de Conexão com Redis:**

```bash
# Verifique se o Redis está rodando
docker-compose exec redis redis-cli ping

# Verifique logs do Redis
docker-compose logs redis
```

---

### 📚 Estrutura do Projeto

```
django_base/
├── .github/
│   └── workflows/
│       └── ci.yml                  # Pipeline CI/CD GitHub Actions
├── grafana/                        # Configuração Grafana (NOVO v1.2.0)
│   ├── dashboards/                 # Dashboards pré-configurados
│   └── provisioning/               # Config de auto-provisionamento
├── k8s/                            # Manifestos Kubernetes (NOVO v1.2.0)
│   ├── base/                       # Manifestos K8s base (12 arquivos)
│   ├── dev/                        # Overlay de desenvolvimento
│   ├── prod/                       # Overlay de produção
│   └── README.md                   # Guia completo de deploy K8s
├── nginx/
│   ├── Dockerfile                  # Build da imagem Nginx
│   └── nginx.conf                  # Configuração Nginx (rate limiting, segurança, gzip)
├── src/
│   ├── core/                       # App Django principal
│   │   ├── management/
│   │   │   └── commands/           # Management commands customizados
│   │   ├── migrations/             # Migrações de banco de dados
│   │   ├── templatetags/
│   │   │   └── core_tags.py        # 23 template tags & filters customizadas
│   │   ├── models.py               # 4 models: Product, UserProfile, Category, Tag
│   │   ├── forms.py                # 4 forms: Login, Register, UserProfile, UserUpdate
│   │   ├── views.py                # 7 views: home, login, register, logout, profile, products, health_check_page
│   │   ├── viewsets.py             # 4 DRF ViewSets com custom actions
│   │   ├── serializers.py          # 10 DRF Serializers (detail + list)
│   │   ├── validators.py           # 8 custom validators (phone, CPF, image, etc.)
│   │   ├── decorators.py           # 15 decorators (permissions, cache, logging)
│   │   ├── mixins.py               # 13 mixins (model + view utilities)
│   │   ├── signals.py              # Django signals (criação de UserProfile)
│   │   ├── tasks.py                # Background tasks (Django Q)
│   │   ├── urls.py                 # URL routing
│   │   ├── admin.py                # Interface do Admin
│   │   └── tests.py                # Test cases (7 tests)
│   └── django_base/
│       ├── settings/               # Settings modulares
│       │   ├── __init__.py         # Auto-detecta ambiente
│       │   ├── base.py             # Settings compartilhados
│       │   ├── dev.py              # Settings de desenvolvimento
│       │   └── prod.py             # Settings de produção (segurança reforçada)
│       ├── urls.py                 # Roteamento principal de URLs
│       ├── wsgi.py                 # Ponto de entrada WSGI
│       └── asgi.py                 # Ponto de entrada ASGI
├── templates/                      # Templates globais
│   ├── base/
│   │   └── base.html               # Template base com navbar, messages, footer
│   ├── auth/
│   │   ├── home.html               # Homepage com showcase das features
│   │   ├── login.html              # Formulário de login
│   │   ├── register.html           # Formulário de cadastro
│   │   ├── profile.html            # Página de Edição de Perfil do Usuário
│   ├── core/
│   │   └── product/
│   │       ├── products.html           # Listagem de Produtos com Filtros
│   │       └── product_create.html   # Página para criar um novo produto
│   ├── health/
│   │   └── health_check.html       # Página de Health Check
│   ├── partials/                   # Partial templates reutilizáveis
│   └── components/
│       ├── card.html               # Componente de card com Bootstrap
│       └── pagination.html         # Controle de paginação
├── logs/                           # Logs (gitignored)
├── staticfiles/                    # Arquivos estáticos coletados (gitignored)
├── mediafiles/                     # Uploads de usuários (gitignored)
├── docker-compose.yml              # Production compose
├── docker-compose.dev.yml          # Sobrescrita de desenvolvimento
├── Dockerfile                      # Build Docker multi-stage
├── Makefile                        # 60+ comandos para dev/prod/K8s (NOVO v1.2.0)
├── pyproject.toml                  # Dependências & configuração de ferramentas
├── .env.example                    # Template de variáveis de ambiente
├── .pre-commit-config.yaml         # Pre-commit hooks (20+ checks)
├── prometheus.yml                  # Configuração Prometheus (melhorado v1.2.0)
├── README.md                       # Este arquivo
├── CHANGELOG.md                    # Changelog do projeto (atualizado v1.2.0)
├── TODOLIST.md                     # Roadmap de desenvolvimento (atualizado v1.2.0)
└── CONTRIBUTING.md                 # Diretrizes de contribuição
```

---

### 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch de feature (`git checkout -b feature/RecursoIncrivel`)
3. Faça suas alterações
4. Execute linters e testes

   ```bash
   pre-commit run --all-files
   python manage.py test src
   ```

5. Commit suas alterações (`git commit -m 'Add: recurso incrível'`)
6. Faça push para a branch (`git push origin feature/RecursoIncrivel`)
7. Abra um Pull Request

#### Padrões de Código

- Use Ruff para formatação (`ruff format .`)
- Passe em todos os linters (`ruff check .`)
- Adicione testes para novos recursos
- Mantenha cobertura acima de 80%
- Escreva docstrings em inglês e português
- Siga as melhores práticas do Django

---

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para
detalhes.

---

### 🙏 Agradecimentos

- Django Software Foundation
- Todas as incríveis bibliotecas open-source usadas neste projeto
- A comunidade Python

---

**Happy Coding! 🎉 / Bom Código! 🎉**
