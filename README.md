# Django Base (django_base) 🚀

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

- **Web Server:** Nginx (with rate limiting, gzip, security headers)
- **Application Server:** Gunicorn (multi-worker WSGI)
- **Backend:** Django 5.2+, Django REST Framework
- **Database:** PostgreSQL 15 (with connection pooling)
- **Cache & Queue:** Redis 7 (for caching, sessions, Django Q)
- **Package Manager:** `uv` (blazing fast Python package manager)
- **Background Tasks:** Django Q2 (`django-q2`)
- **API Features:** CORS, DRF Spectacular (OpenAPI/Swagger), django-filter
- **Containerization:** Docker & Docker Compose (multi-stage builds)
- **Code Quality:** `Ruff` linter/formatter, `pre-commit` hooks, Bandit security
- **Testing:** `django.test` with `coverage`
- **Observability:** Prometheus & Grafana dashboards
- **Configuration:** `python-decouple` with comprehensive `.env` support
- **Development Tools:** `django-extensions`, `watchdog` for hot-reloading

### ✨ Key Features

- ✅ **Modular Settings:** Separate `base.py`, `dev.py`, `prod.py` for
  environment-specific config
- ✅ **Security Hardening:** HSTS, SSL redirect, secure cookies, security
  headers, rate limiting
- ✅ **Production-Ready:** Multi-stage Docker builds, non-root user, health
  checks
- ✅ **Redis Integration:** Caching, session storage, task queue backend
- ✅ **API Documentation:** Auto-generated OpenAPI/Swagger with drf-spectacular
- ✅ **Observability:** Prometheus metrics + Grafana dashboards
- ✅ **Pre-commit Hooks:** 20+ hooks including Ruff, Bandit, detect-secrets,
  django-upgrade
- ✅ **CI/CD Ready:** GitHub Actions pipeline with linting and tests
- ✅ **Bilingual Documentation:** Full PT-BR/EN comments throughout codebase

### 🏁 Running the Project (Docker)

#### 💻 Development Mode (`dev` profile)

This mode is for active development with hot-reloading, debug mode, and verbose
logging.

1. **First-Time Setup:**

   ```bash
   # Clone the repo and enter the directory
   git clone <your-repository-url> && cd django_base

   # Create the environment file
   cp .env.example .env

   # Build the images
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev build

   # Run database migrations (using 'run' for a temporary container)
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py migrate

   # Create a superuser
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py createsuperuser
   ```

2. **To Start the Development Server:** _This command will attach to your
   terminal and show live logs. Press `Ctrl + C` to stop._

   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up
   ```

#### 🚀 Production Mode (`prod` profile)

This mode runs the production stack with Nginx, Gunicorn, Redis caching, and
security hardening.

1. **Configure Production Environment:**

   ```bash
   # Copy and edit .env with production values
   cp .env.example .env
   # IMPORTANT: Set DEBUG=False, configure SECRET_KEY, ALLOWED_HOSTS, etc.
   ```

2. **To Start the Production Stack:**

   ```bash
   docker-compose --profile prod up -d --build
   ```

3. **Required Commands (after starting):**

   ```bash
   # Run migrations
   docker-compose --profile prod exec web python manage.py migrate

   # Collect static files for Nginx
   docker-compose --profile prod exec web python manage.py collectstatic --no-input

   # Create superuser (optional)
   docker-compose --profile prod exec web python manage.py createsuperuser
   ```

#### 🌐 Access Points

After starting, your environment will be available at:

- **Application:** `http://localhost:8000`
- **API Root:** `http://localhost:8000/api/v1/`
- **API Documentation (Swagger):**
  `http://localhost:8000/api/schema/swagger-ui/`
- **API Documentation (ReDoc):** `http://localhost:8000/api/schema/redoc/`
- **Django Admin:** `http://localhost:8000/admin/`
- **Health Check:** `http://localhost:8000/health/`
- **Prometheus Metrics:** `http://localhost:8000/django-metrics/`
- **Prometheus:** `http://localhost:9090`
- **Grafana:** `http://localhost:3000` (default login: `admin`/`admin`)

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
- **hadolint** (Dockerfile linting)
- **shellcheck** (Shell script linting)
- And 15+ more quality checks

---

### 🚀 Day-to-Day Commands (Docker)

#### Development Commands

```bash
# Start dev environment with live logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up

# Start in background
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d

# View logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f web

# Access container shell
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web bash

# Run migrations
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Run tests with coverage
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage run manage.py test src
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage report

# Stop all services
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down
```

#### Production Commands

```bash
# Start production stack
docker-compose --profile prod up -d

# View logs
docker-compose --profile prod logs -f

# Run migrations
docker-compose --profile prod exec web python manage.py migrate

# Collect static files
docker-compose --profile prod exec web python manage.py collectstatic --no-input

# Access container shell
docker-compose --profile prod exec web bash

# Restart services
docker-compose --profile prod restart

# Stop all services
docker-compose --profile prod down
```

#### Database Commands

```bash
# Create database backup
docker-compose exec db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup.sql

# Restore database backup
docker-compose exec -T db psql -U ${POSTGRES_USER} ${POSTGRES_DB} < backup.sql

# Access PostgreSQL shell
docker-compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
```

#### Redis Commands

```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# Check Redis info
docker-compose exec redis redis-cli INFO

# Flush all Redis data (CAREFUL!)
docker-compose exec redis redis-cli FLUSHALL
```

---

### 🧪 Testing

#### Run Tests

```bash
# Run all tests
python manage.py test src

# Run with coverage
coverage run manage.py test src
coverage report
coverage html  # Generate HTML report

# Run specific test file
python manage.py test src.core.tests

# Run with pytest (if installed)
pytest src/
```

#### Linting and Formatting

```bash
# Check code with Ruff
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Run all pre-commit hooks
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

- `django_http_requests_total_by_view_transport_method`
- `django_http_responses_total_by_status`
- `django_http_requests_latency_seconds`
- `django_db_query_count`

#### Grafana

Access Grafana at `http://localhost:3000` (default: `admin`/`admin`)

**Recommended Dashboards:**

1. Django Dashboard (ID: 9528)
2. PostgreSQL Database (ID: 9628)
3. Nginx (ID: 12708)
4. Redis (ID: 11835)

**To Import:**

1. Click "+" → "Import"
2. Enter dashboard ID
3. Select Prometheus data source
4. Click "Import"

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
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── nginx/
│   ├── Dockerfile              # Nginx image build
│   └── nginx.conf              # Nginx configuration (rate limiting, security, gzip)
├── src/
│   ├── core/                   # Main Django app
│   │   ├── migrations/
│   │   ├── models.py           # Data models with validation
│   │   ├── views.py            # View functions + error handlers
│   │   ├── viewsets.py         # DRF ViewSets with filters
│   │   ├── serializers.py      # DRF Serializers with validation
│   │   ├── signals.py          # Django signals with error handling
│   │   ├── tasks.py            # Background tasks (Django Q)
│   │   ├── urls.py             # URL routing
│   │   └── tests.py            # Test cases
│   └── django_base/
│       ├── settings/           # Modular settings
│       │   ├── __init__.py     # Auto-detects environment
│       │   ├── base.py         # Shared settings
│       │   ├── dev.py          # Development settings
│       │   └── prod.py         # Production settings (security hardened)
│       ├── urls.py             # Main URL routing
│       ├── wsgi.py             # WSGI entry point
│       └── asgi.py             # ASGI entry point
├── templates/                  # Global templates
├── logs/                       # Application logs (gitignored)
├── staticfiles/                # Collected static files (gitignored)
├── mediafiles/                 # User uploads (gitignored)
├── docker-compose.yml          # Production compose
├── docker-compose.dev.yml      # Development overrides
├── Dockerfile                  # Multi-stage Docker build
├── pyproject.toml              # Dependencies & tool config
├── .env.example                # Environment variables template
├── .pre-commit-config.yaml     # Pre-commit hooks (20+ checks)
├── prometheus.yml              # Prometheus configuration
└── README.md                   # This file
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
- Write docstrings in English and Portuguese
- Follow Django best practices

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

- **Servidor Web:** Nginx (com rate limiting, gzip, headers de segurança)
- **Servidor de Aplicação:** Gunicorn (WSGI multi-worker)
- **Backend:** Django 5.2+, Django REST Framework
- **Banco de Dados:** PostgreSQL 15 (com connection pooling)
- **Cache & Fila:** Redis 7 (para cache, sessões, Django Q)
- **Gerenciador de Pacotes:** `uv` (gerenciador de pacotes Python ultrarrápido)
- **Tarefas em Background:** Django Q2 (`django-q2`)
- **Recursos API:** CORS, DRF Spectacular (OpenAPI/Swagger), django-filter
- **Containerização:** Docker & Docker Compose (builds multi-stage)
- **Qualidade de Código:** `Ruff` linter/formatter, `pre-commit` hooks,
  segurança Bandit
- **Testes:** `django.test` com `coverage`
- **Observabilidade:** Dashboards Prometheus & Grafana
- **Configuração:** `python-decouple` com suporte abrangente a `.env`
- **Ferramentas de Desenvolvimento:** `django-extensions`, `watchdog` para
  hot-reloading

### ✨ Funcionalidades Principais

- ✅ **Settings Modulares:** `base.py`, `dev.py`, `prod.py` separados para
  configuração por ambiente
- ✅ **Segurança Reforçada:** HSTS, redirecionamento SSL, cookies seguros,
  headers de segurança, rate limiting
- ✅ **Pronto para Produção:** Builds Docker multi-stage, usuário não-root,
  health checks
- ✅ **Integração Redis:** Cache, armazenamento de sessão, backend de fila de
  tarefas
- ✅ **Documentação API:** OpenAPI/Swagger auto-gerado com drf-spectacular
- ✅ **Observabilidade:** Métricas Prometheus + dashboards Grafana
- ✅ **Pre-commit Hooks:** 20+ hooks incluindo Ruff, Bandit, detect-secrets,
  django-upgrade
- ✅ **CI/CD Pronto:** Pipeline GitHub Actions com linting e testes
- ✅ **Documentação Bilíngue:** Comentários completos PT-BR/EN em todo o código

### 🏁 Executando o Projeto (Docker)

#### 💻 Modo Desenvolvimento (perfil `dev`)

Este modo é para desenvolvimento ativo com hot-reloading, modo debug e logging
verboso.

1. **Configuração Inicial:**

   ```bash
   # Clone o repositório e entre no diretório
   git clone <url-do-seu-repositorio> && cd django_base

   # Crie o arquivo de ambiente
   cp .env.example .env

   # Construa as imagens
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev build

   # Execute as migrações do banco de dados (usando 'run' para container temporário)
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py migrate

   # Crie um superusuário
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py createsuperuser
   ```

2. **Para Iniciar o Servidor de Desenvolvimento:** _Este comando irá anexar ao
   seu terminal e mostrar logs ao vivo. Pressione `Ctrl + C` para parar._

   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up
   ```

#### 🚀 Modo Produção (perfil `prod`)

Este modo executa a stack de produção com Nginx, Gunicorn, cache Redis e
segurança reforçada.

1. **Configure o Ambiente de Produção:**

   ```bash
   # Copie e edite .env com valores de produção
   cp .env.example .env
   # IMPORTANTE: Defina DEBUG=False, configure SECRET_KEY, ALLOWED_HOSTS, etc.
   ```

2. **Para Iniciar a Stack de Produção:**

   ```bash
   docker-compose --profile prod up -d --build
   ```

3. **Comandos Necessários (após iniciar):**

   ```bash
   # Execute as migrações
   docker-compose --profile prod exec web python manage.py migrate

   # Colete arquivos estáticos para o Nginx
   docker-compose --profile prod exec web python manage.py collectstatic --no-input

   # Crie um superusuário (opcional)
   docker-compose --profile prod exec web python manage.py createsuperuser
   ```

#### 🌐 Pontos de Acesso

Após iniciar, seu ambiente estará disponível em:

- **Aplicação:** `http://localhost:8000`
- **API Root:** `http://localhost:8000/api/v1/`
- **Documentação API (Swagger):** `http://localhost:8000/api/schema/swagger-ui/`
- **Documentação API (ReDoc):** `http://localhost:8000/api/schema/redoc/`
- **Admin Django:** `http://localhost:8000/admin/`
- **Health Check:** `http://localhost:8000/health/`
- **Métricas Prometheus:** `http://localhost:8000/django-metrics/`
- **Prometheus:** `http://localhost:9090`
- **Grafana:** `http://localhost:3000` (login padrão: `admin`/`admin`)

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
- **hadolint** (linting de Dockerfile)
- **shellcheck** (linting de scripts shell)
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

# Criar superusuário
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Executar testes com cobertura
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage run manage.py test src
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web coverage report

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
```

#### Comandos Redis

```bash
# Acessar CLI do Redis
docker-compose exec redis redis-cli

# Verificar informações do Redis
docker-compose exec redis redis-cli INFO

# Limpar todos os dados do Redis (CUIDADO!)
docker-compose exec redis redis-cli FLUSHALL
```

---

### 🧪 Testes

#### Executar Testes

```bash
# Executar todos os testes
python manage.py test src

# Executar com cobertura
coverage run manage.py test src
coverage report
coverage html  # Gerar relatório HTML

# Executar arquivo de teste específico
python manage.py test src.core.tests

# Executar com pytest (se instalado)
pytest src/
```

#### Linting e Formatação

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

- `django_http_requests_total_by_view_transport_method`
- `django_http_responses_total_by_status`
- `django_http_requests_latency_seconds`
- `django_db_query_count`

#### Grafana

Acesse o Grafana em `http://localhost:3000` (padrão: `admin`/`admin`)

**Dashboards Recomendados:**

1. Django Dashboard (ID: 9528)
2. PostgreSQL Database (ID: 9628)
3. Nginx (ID: 12708)
4. Redis (ID: 11835)

**Para Importar:**

1. Clique em "+" → "Import"
2. Digite o ID do dashboard
3. Selecione a fonte de dados Prometheus
4. Clique em "Import"

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
│       └── ci.yml              # Pipeline CI/CD GitHub Actions
├── nginx/
│   ├── Dockerfile              # Build da imagem Nginx
│   └── nginx.conf              # Configuração Nginx (rate limiting, segurança, gzip)
├── src/
│   ├── core/                   # App Django principal
│   │   ├── migrations/
│   │   ├── models.py           # Modelos de dados com validação
│   │   ├── views.py            # Funções view + tratadores de erro
│   │   ├── viewsets.py         # ViewSets DRF com filtros
│   │   ├── serializers.py      # Serializers DRF com validação
│   │   ├── signals.py          # Signals Django com tratamento de erros
│   │   ├── tasks.py            # Tarefas em background (Django Q)
│   │   ├── urls.py             # Roteamento de URLs
│   │   └── tests.py            # Casos de teste
│   └── django_base/
│       ├── settings/           # Settings modulares
│       │   ├── __init__.py     # Auto-detecta ambiente
│       │   ├── base.py         # Settings compartilhados
│       │   ├── dev.py          # Settings de desenvolvimento
│       │   └── prod.py         # Settings de produção (segurança reforçada)
│       ├── urls.py             # Roteamento principal de URLs
│       ├── wsgi.py             # Ponto de entrada WSGI
│       └── asgi.py             # Ponto de entrada ASGI
├── templates/                  # Templates globais
├── logs/                       # Logs da aplicação (gitignored)
├── staticfiles/                # Arquivos estáticos coletados (gitignored)
├── mediafiles/                 # Uploads de usuários (gitignored)
├── docker-compose.yml          # Compose de produção
├── docker-compose.dev.yml      # Sobrescrita de desenvolvimento
├── Dockerfile                  # Build Docker multi-stage
├── pyproject.toml              # Dependências & configuração de ferramentas
├── .env.example                # Template de variáveis de ambiente
├── .pre-commit-config.yaml     # Hooks pre-commit (20+ verificações)
├── prometheus.yml              # Configuração Prometheus
└── README.md                   # Este arquivo
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
