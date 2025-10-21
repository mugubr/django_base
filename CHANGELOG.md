## [Unreleased] - 2025-01-20

### Added - Development & Testing / Desenvolvimento & Testes

- **Django Debug Toolbar:** Added django-debug-toolbar for development profiling
  - **Django Debug Toolbar:** Adicionado django-debug-toolbar para profiling em
    desenvolvimento
  - Configured in `settings/dev.py` with middleware
  - URL patterns for `__debug__/` in development
  - Helps identify N+1 queries and slow database operations

- **Query Optimization:** Optimized all DRF ViewSets with
  select_related/prefetch_related
  - **Otimização de Queries:** Otimizados todos ViewSets DRF com
    select_related/prefetch_related
  - ProductViewSet: `select_related('category', 'created_by', 'updated_by')` +
    `prefetch_related('tags')`
  - CategoryViewSet: `select_related('parent', 'created_by', 'updated_by')` +
    `prefetch_related('children')`
  - TagViewSet: `select_related('created_by')`
  - UserProfileViewSet: `select_related('user')`
  - Eliminates N+1 query problems

- **Factory Boy Integration:** Test data factories for all models
  - **Integração Factory Boy:** Fábricas de dados de teste para todos os modelos
  - New file: `src/core/factories.py`
  - Factories: UserFactory, UserProfileFactory, CategoryFactory, TagFactory,
    ProductFactory
  - Uses Faker with PT-BR and EN-US locales for realistic data
  - Automatic relationship creation

- **Integration Tests:** Complete API workflow testing
  - **Testes de Integração:** Testes completos de fluxos de trabalho da API
  - New directory: `src/core/tests/`
  - ProductAPIIntegrationTest: Full CRUD + filtering workflows
  - AuthenticationIntegrationTest: Registration → profile → update flows
  - CategoryHierarchyIntegrationTest: Tree structure operations
  - Uses Factory Boy for test data generation

### Added - Monitoring & Error Tracking / Monitoramento & Rastreamento de Erros

- **Sentry Integration:** Complete Sentry setup for error tracking and
  performance monitoring
  - **Integração Sentry:** Configuração completa Sentry para rastreamento de
    erros e monitoramento de performance
  - Added `sentry-sdk[django]>=2.19.2` dependency
  - Configured in `settings/prod.py` with traces and profiles sampling
  - Environment variables: `SENTRY_DSN`, `SENTRY_TRACES_SAMPLE_RATE`,
    `SENTRY_PROFILES_SAMPLE_RATE`, `SENTRY_RELEASE`
  - Only active in production when DSN is configured
  - Supports release tracking and custom environments

### Added - Claude Code Integration / Integração Claude Code

- **Custom AI Agents:** 4 specialized agents for different development tasks
  - **Agentes IA Customizados:** 4 agentes especializados para diferentes
    tarefas de desenvolvimento
  - Django Expert (`agents/django-expert.md`) - Django/DRF specialist
  - Code Reviewer (`agents/code-reviewer.md`) - Quality and security review
  - Backend Architect (`agents/backend-architect.md`) - System architecture
  - Python Pro (`agents/python-pro.md`) - Python optimization
  - Complete documentation in `.claude/README.md`

- **Memory MCP Server:** Persistent context across sessions
  - **Servidor Memory MCP:** Contexto persistente entre sessões
  - Configuration in `.mcp.json`
  - Reduces context repetition and improves continuity

- **Token Optimization:** Optimized configuration for Claude Code
  - **Otimização de Tokens:** Configuração otimizada para Claude Code
  - Project context in `.claude/context.md`
  - Simplified permissions in `.claude/settings.local.json`
  - Status line with token monitoring

### Changed - Documentation / Documentação

- **Enhanced README:** Added direct links to all library and tool documentation
  - **README Aprimorado:** Adicionados links diretos para documentação de todas
    bibliotecas e ferramentas
  - Links to Django, DRF, PostgreSQL, Redis, Docker, Kubernetes docs
  - New Claude Code integration section
  - Updated feature list with recent additions
  - Cross-platform setup instructions (Linux/macOS/Windows)

- **Cross-Platform Setup Scripts:** Complete Windows support for all setup
  scripts
  - **Scripts de Configuração Multi-Plataforma:** Suporte completo Windows para
    todos scripts de configuração
  - New files: `setup.ps1`, `setup.bat` (development)
  - New files: `setup-prod.ps1`, `setup-prod.bat` (production)
  - New files: `setup-k8s.ps1`, `setup-k8s.bat` (Kubernetes)
  - PowerShell versions with colored output and better error handling
  - Batch versions for Command Prompt compatibility
  - All scripts support same flags as bash versions
  - Updated README with platform-specific instructions

### Fixed - Pre-commit & Code Quality / Correções Pre-commit & Qualidade de Código

- **Pre-commit Claude Code Exclusions:** Fixed pre-commit formatting `.claude/`
  configuration files
  - **Exclusões Claude Code no Pre-commit:** Corrigido pre-commit formatando
    arquivos de configuração `.claude/`
  - Added `exclude: ^\.claude/` to all formatting hooks (Ruff, Prettier,
    trailing-whitespace, etc.)
  - Created `.prettierignore` file to explicitly exclude `.claude/` from
    Prettier
  - Updated `.gitignore` to ignore `.claude/settings.local.json` and
    `.claude/todos/`
  - Prevents accidental formatting of AI assistant configuration files

- **Windows Batch Scripts Fixes:** Fixed syntax and encoding issues in batch
  scripts
  - **Correções Scripts Batch Windows:** Corrigidos problemas de sintaxe e
    encoding em scripts batch
  - Fixed `docker compose` command handling with proper quoting
  - Removed accents to prevent encoding issues in Command Prompt
  - Added `test-setup.bat` for system diagnostics
  - Created `setup-quiet.bat` for minimal output (logs to setup.log)
  - New file: `WINDOWS-SETUP.md` with complete Windows troubleshooting guide
  - All batch scripts now work correctly on Windows 10/11
  - **Added `makemigrations` step** to all setup scripts (was missing)
  - All Windows scripts now match bash versions exactly

- **Tests Directory Structure Fix:** Resolved test discovery conflicts
  - **Correção da Estrutura do Diretório Tests:** Resolvido conflitos de
    descoberta de testes
  - Moved `tests.py` to `tests/test_models.py`
  - Now using proper package structure: `src/core/tests/`
  - Prevents ImportError during test discovery

### Changed - Complete Model Refactoring / Refatoração Completa de Modelos

- **All Models Refactored to Use Mixins:** Complete refactoring of all models
  for consistency
  - **Todos os Modelos Refatorados para Usar Mixins:** Refatoração completa de
    todos modelos para consistência

- **Product Model:**
  - Now uses `TimeStampedModelMixin`, `SoftDeleteModelMixin`,
    `UserTrackingMixin`
  - Removed duplicate fields (created_at, updated_at, created_by)
  - Added `stock` field (IntegerField, default=0)
  - Added `updated_by` field (from UserTrackingMixin)
  - Changed from `is_active` to `is_deleted` pattern (proper soft delete)
  - Removed deprecated `deactivate()` and `activate()` methods
  - Use `soft_delete()` and `restore()` instead
  - Updated indexes: `is_active` → `is_deleted`
  - Added `stock_idx` index for stock queries
  - Updated permission: `can_deactivate_product` → `can_delete_product`

- **Category Model:**
  - Now uses `TimeStampedModelMixin`, `SoftDeleteModelMixin`,
    `UserTrackingMixin`
  - Removed duplicate fields (created_at, updated_at, is_active)
  - Added `created_by`, `updated_by`, `deleted_at` fields
  - Changed from `is_active` to `is_deleted` pattern
  - Updated `product_count` property to filter by `is_deleted=False`
  - Updated indexes to use `is_deleted`

- **Tag Model:**
  - Now uses `TimeStampedModelMixin`, `UserTrackingMixin`
  - Removed duplicate `created_at` field
  - Added `created_by`, `updated_by`, `updated_at` fields

- **UserProfile Model:**
  - Now uses `TimeStampedModelMixin`
  - Removed duplicate `created_at`, `updated_at` fields
  - Model structure unchanged (already had timestamps)

- **Enhanced Product Validation:** Added comprehensive validation rules
  - **Validação Aprimorada de Produto:** Adicionadas regras de validação
    abrangentes
  - Stock validation: cannot be negative, max 1,000,000 units
  - Price validation: must be positive, max 9,999,999.99
  - Name validation: minimum 3 characters, no empty/whitespace only

- **Admin-Only Product Management:** Product create/edit restricted to staff
  members
  - **Gerenciamento de Produto Admin-Only:** Criação/edição de produto restrita
    a staff
  - `product_create_view` requires `@staff_member_required`
  - New `product_edit_view` for editing (admin only)
  - URL pattern: `/products/<pk>/edit/`
  - Template: `product_edit.html` with product history info

- **ProductForm Updates:** Updated form to reflect model changes
  - **Atualizações ProductForm:** Formulário atualizado para refletir mudanças
    no modelo
  - Added `stock` field with validation
  - Removed `is_active` field (now handled by soft delete)
  - Fields: name, price, stock, category, tags

- **Products Template Updates:** Updated UI for new model structure
  - **Atualizações Template Products:** UI atualizada para nova estrutura do
    modelo
  - Shows stock quantity for each product
  - Changed "Inactive" badge to "Deleted" badge
  - Added "Edit" button for staff members only
  - Edit button uses `{% if user.is_staff %}` conditional

### Fixed - Code Quality / Qualidade de Código

- **Removed Duplicate Dependency:** Removed duplicate sentry-sdk entry in
  pyproject.toml
  - **Removida Dependência Duplicada:** Removida entrada duplicada sentry-sdk em
    pyproject.toml

### Migration Required / Migração Necessária

⚠️ **Important:** Run migrations after pulling these changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

⚠️ **Importante:** Execute migrations após baixar estas mudanças:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## [1.2.0] - 2025-01-13

This version focuses on infrastructure improvements, Kubernetes support,
monitoring enhancements, and type safety. Major additions include complete
Kubernetes manifests, Grafana/Prometheus monitoring stack, type hints, and
enhanced development tooling.

Esta versão foca em melhorias de infraestrutura, suporte a Kubernetes,
aprimoramentos de monitoramento e type safety. Adições principais incluem
manifestos completos Kubernetes, stack de monitoramento Grafana/Prometheus, type
hints e ferramentas de desenvolvimento aprimoradas.

### Added - Security & Production Readiness / Segurança e Prontidão para Produção

- **Environment Variables Validator:** New comprehensive validation module that
  checks critical configuration on startup, preventing misconfiguration errors
  in production.
  - **Validador de Variáveis de Ambiente:** Novo módulo abrangente de validação
    que verifica configuração crítica na inicialização, prevenindo erros de
    configuração em produção.
  - Located at `src/django_base/settings/env_validator.py` (~400 lines)
  - Custom management command: `src/core/management/commands/validate_env.py`
  - Validates SECRET_KEY strength, DEBUG mode, ALLOWED_HOSTS, database config,
    SSL settings
  - Integrated into both `prod.py` and `dev.py` settings
  - Provides detailed reports with color-coded warnings and errors
  - Fully bilingual (EN/PT-BR)

- **Enhanced Security Headers:** Nginx configuration now includes modern
  security headers:
  - **Headers de Segurança Aprimorados:** Configuração Nginx agora inclui
    headers modernos:
  - `Permissions-Policy` - Granular control of browser APIs
  - `Content-Security-Policy` (commented, ready to enable)
  - `X-Permitted-Cross-Domain-Policies` - Restricts Flash/PDF cross-domain
  - `Cross-Origin-Opener-Policy` - Isolates browsing context
  - `Cross-Origin-Resource-Policy` - Controls resource sharing
  - Updated SSL configuration with OCSP Stapling, modern ciphers, IPv6 support

- **Database Backup & Restore System:** Professional-grade scripts for database
  management:
  - **Sistema de Backup e Restauração:** Scripts profissionais para
    gerenciamento do banco:
  - `scripts/backup_database.sh` - Automated compressed backups with retention
    policies
  - `scripts/restore_database.sh` - Safe restoration with double confirmation
  - Supports both Docker and local PostgreSQL installations
  - Automatic backup verification and integrity checks
  - Pre-restore backup creation for safety
  - Detailed logging with colored output
  - Comprehensive documentation in `scripts/README.md` (~500 lines)

- **SSL/HTTPS Configuration Guide:** Complete guide for production HTTPS setup:
  - **Guia de Configuração SSL/HTTPS:** Guia completo para configuração HTTPS em
    produção:
  - Located at `docs/SSL_HTTPS_SETUP.md` (~800 lines)
  - Step-by-step Certbot (Let's Encrypt) setup instructions
  - Manual certificate configuration guide
  - Automatic renewal configuration (cron/systemd/Docker)
  - SSL testing procedures and tools (SSL Labs, OpenSSL, curl)
  - Troubleshooting section with common issues
  - Security best practices and monitoring
  - Fully bilingual (EN/PT-BR)

- **JWT Authentication Documentation:** Complete guide for JWT token
  authentication:
  - **Documentação de Autenticação JWT:** Guia completo para autenticação por
    token JWT:
  - Located at `docs/JWT_AUTHENTICATION.md` (~500 lines)
  - Configuration and environment variables
  - API endpoints (obtain, refresh, verify)
  - Usage examples (curl, JavaScript, Python)
  - Security best practices
  - Troubleshooting and migration guide
  - Fully bilingual (EN/PT-BR)

### Added - Kubernetes Infrastructure / Infraestrutura Kubernetes

- **Complete Kubernetes Manifests:** Production-ready K8s configuration:
  - **Manifestos Kubernetes Completos:** Configuração K8s pronta para produção:
  - Base manifests (12 files): namespace, configmaps, secrets, PVCs,
    deployments, services, ingress
  - Dev and prod overlays using Kustomize
  - PostgreSQL, Redis, Django, Nginx, Prometheus, Grafana deployments
  - Health checks, resource limits, RBAC for Prometheus
  - Auto-scaling ready with HPA configuration
  - Comprehensive README (~300 lines) with deployment guide

- **Automated Kubernetes Setup Script:** New `setup-k8s.sh` script for automated
  deployment:
  - **Script de Setup Automatizado Kubernetes:** Novo script `setup-k8s.sh` para
    deployment automatizado:
  - Windows-compatible kubectl and docker detection
  - Automatic image building with local image support
  - Pre-flight checks (kubectl, Docker, cluster connection)
  - Automated namespace creation and resource deployment
  - Health monitoring with timeout handling
  - Comprehensive deployment instructions and next steps
  - Support for dev and prod environments
  - Fully bilingual output (EN/PT-BR)

- **Monitoring Stack Enhancements:** Full observability setup:
  - **Melhorias na Stack de Monitoramento:** Setup completo de observabilidade:
  - PostgreSQL, Redis, and Nginx exporters added to docker-compose
  - Enhanced Prometheus configuration with multiple scrape targets
  - Grafana provisioning for automatic dashboard loading
  - New simplified dashboard (django-base-overview.json)
  - Nginx `/nginx_status` endpoint for metrics

### Added - Developer Experience & Tools / Experiência do Desenvolvedor & Ferramentas

- **Makefile with Kubernetes Commands:** 18 new K8s commands added:
  - **Makefile com Comandos Kubernetes:** 18 novos comandos K8s adicionados:
  - `make k8s-dev-deploy`, `make k8s-prod-deploy` - Deploy to cluster
  - `make k8s-status`, `make k8s-logs` - Monitor deployments
  - `make k8s-shell`, `make k8s-migrate` - Access and manage pods
  - `make k8s-grafana`, `make k8s-prometheus` - Port forwarding
  - `make k8s-scale`, `make k8s-rollback` - Scaling and rollback
  - Total 60+ commands for Docker, K8s, Django operations

- **Type Hints Implementation:** Modern Python type annotations:
  - **Implementação de Type Hints:** Anotações de tipo Python modernas:
  - Complete type hints in `models.py`, `views.py`, `serializers.py`
  - Configured mypy with `pyproject.toml` settings
  - Pre-commit hook for automatic type checking
  - Better IDE autocomplete and error detection

- **Makefile:** Comprehensive Makefile with 40+ commands for common tasks:
  - **Makefile:** Makefile abrangente com 40+ comandos para tarefas comuns:
  - Development, production, testing, linting, database management
  - Docker operations, migrations, translations
  - Backup/restore shortcuts
  - Fully documented and bilingual

- **GitHub Templates:** Professional issue and PR templates:
  - **Templates GitHub:** Templates profissionais de issues e PRs:
  - Bug report template (`bug_report.yml`)
  - Feature request template (`feature_request.yml`)
  - Question template (`question.yml`)
  - Pull request template with checklist
  - Configuration file for GitHub issues

- **Contributing Guide:** Complete contribution guidelines:
  - **Guia de Contribuição:** Diretrizes completas de contribuição:
  - Located at `CONTRIBUTING.md` (~400 lines)
  - Code of conduct
  - Development setup
  - Coding standards and conventions
  - Testing guidelines
  - Pull request process
  - Fully bilingual (EN/PT-BR)

- **Project Roadmap:** Comprehensive TODO list with development priorities:
  - **Roadmap do Projeto:** Lista TODO abrangente com prioridades de
    desenvolvimento:
  - Located at `TODOLIST.md` (~400 lines)
  - High priority security & production items
  - Feature enhancements roadmap
  - Quick wins (1-2h tasks)
  - Categorized by priority and effort
  - Fully bilingual (EN/PT-BR)

- **Sitemap & SEO:** SEO optimization files:
  - **Sitemap & SEO:** Arquivos de otimização SEO:
  - `src/core/sitemaps.py` - Dynamic sitemap generation
  - `static/robots.txt` - Search engine crawler directives
  - `static/humans.txt` - Team and project information
  - Integrated into Django URLs

### Added - New Features & Enhancements / Novas Funcionalidades & Melhorias

- **Project Information Page:** New page displaying project metadata:
  - **Página de Informações do Projeto:** Nova página exibindo metadados do
    projeto:
  - Located at `templates/auth/project_info.html`
  - Shows Python version, Django version, dependencies
  - Git commit information
  - Database and cache status
  - Environment details

- **Context Processors:** New context processor for global template variables:
  - **Context Processors:** Novo context processor para variáveis globais de
    template:
  - Located at `src/core/context_processors.py`
  - Provides project metadata to all templates
  - Git information, versions, environment data

- **JWT Token Endpoints:** Enhanced JWT authentication views with bilingual
  docstrings:
  - **Endpoints de Token JWT:** Views de autenticação JWT aprimoradas com
    docstrings bilíngues:
  - `CustomTokenObtainPairView` - Obtain access/refresh tokens
  - `CustomTokenRefreshView` - Refresh access token
  - `CustomTokenVerifyView` - Verify token validity
  - Complete API documentation in views
  - Examples for curl, JavaScript, Python

### Changed - Security Improvements / Melhorias de Segurança

- **Production Settings Validation:** Both production and development settings
  now validate environment variables on startup, with stricter checks for
  production.
  - **Validação de Settings de Produção:** Settings de produção e
    desenvolvimento agora validam variáveis de ambiente na inicialização, com
    verificações mais rigorosas para produção.

- **Nginx SSL Configuration:** Enhanced SSL configuration with:
  - **Configuração SSL Nginx:** Configuração SSL aprimorada com:
  - Modern cipher suites including CHACHA20-POLY1305
  - OCSP Stapling for faster certificate validation
  - Support for Diffie-Hellman parameters
  - IPv6 support
  - Let's Encrypt ACME challenge support

- **Base Settings Enhancements:** Updated `base.py` with:
  - **Melhorias em Base Settings:** Atualizado `base.py` com:
  - Context processor for project metadata
  - Sitemaps framework integration
  - Enhanced TEMPLATES configuration

### Changed - UI/UX Improvements / Melhorias de UI/UX

- **Homepage Redesign:** Completely redesigned homepage with:
  - **Redesign da Homepage:** Homepage completamente redesenhada com:
  - Modern card-based layout
  - Feature showcase sections
  - Better navigation and user flow
  - Responsive design improvements

- **Templates Refactoring:** Major template improvements:
  - **Refatoração de Templates:** Grandes melhorias nos templates:
  - Renamed `examples.html` to `products.html` for better clarity
  - Removed deprecated `about.html` page
  - Added `project_info.html` with comprehensive project details
  - Enhanced base template with better navigation
  - Improved login page styling
  - Updated product creation form

### Changed - Configuration & Dependencies / Configuração & Dependências

- **PyProject Configuration:** Enhanced `pyproject.toml` with:
  - **Configuração PyProject:** `pyproject.toml` aprimorado com:
  - New dependencies for sitemap and documentation
  - Updated tool configurations
  - Better organized dependency groups

- **Environment Example:** Updated `.env.example` with:
  - **Exemplo de Ambiente:** Atualizado `.env.example` com:
  - New environment variables for validators
  - Better documentation
  - Security recommendations

- **Git Configuration:** Updated `.gitignore` with:
  - **Configuração Git:** Atualizado `.gitignore` com:
  - Backup directory exclusions
  - Additional temporary files
  - Better organized sections

### Changed - Security & Performance / Segurança e Performance

- **Redis-Based Rate Limiting:** The `@rate_limit` decorator in
  `src/core/decorators.py` now uses a Redis-based backend instead of the simple
  in-memory store. This ensures that rate limits are shared correctly across
  multiple server processes, making it suitable for production environments.
  - **Limitação de Taxa Baseada em Redis:** O decorador `@rate_limit` em
    `src/core/decorators.py` agora usa um backend baseado em Redis em vez do
    simples armazenamento em memória. Isso garante que os limites de taxa sejam
    compartilhados corretamente entre múltiplos processos do servidor,
    tornando-o adequado para ambientes de produção.

### Added - Code Quality / Qualidade de Código

- **Rate Limiter Test:** Added a new test case (`RateLimitDecoratorTest`) to
  `src/core/tests.py` to verify the functionality of the Redis-based rate
  limiter and ensure its correctness.
  - **Teste do Limitador de Taxa:** Adicionado um novo caso de teste
    (`RateLimitDecoratorTest`) a `src/core/tests.py` para verificar a
    funcionalidade do limitador de taxa baseado em Redis e garantir sua
    correção.

### Fixed - Translation Corrections / Correções de Tradução

- **Portuguese Translation:** Fixed typo in `locale/pt_BR/LC_MESSAGES/django.po`
  - **Tradução Portuguesa:** Corrigido erro de digitação em
    `locale/pt_BR/LC_MESSAGES/django.po`
  - Changed "diretament" to "em texto simples" for better accuracy
  - Added 100+ new translation strings
  - Improved existing translations for consistency

### Fixed - Code Quality / Qualidade de Código

- **Test Suite:** Updated tests in `src/core/tests.py`:
  - **Suite de Testes:** Testes atualizados em `src/core/tests.py`:
  - Removed deprecated test cases
  - Improved test coverage
  - Better test organization

### Fixed - Kubernetes Configuration / Configuração Kubernetes

- **Kustomize Syntax Updates:** Fixed deprecated Kustomize syntax:
  - **Atualizações de Sintaxe Kustomize:** Corrigida sintaxe depreciada do
    Kustomize:
  - Changed `bases:` to `resources:` in overlays
  - Updated `commonLabels:` to `labels:` with `pairs:` format
  - Removed `configMapGenerator` with `behavior: merge`
  - Used JSON patches instead for ConfigMap modifications

- **Storage Class Configuration:** Fixed PVC configuration for Docker Desktop:
  - **Configuração de Storage Class:** Corrigida configuração de PVC para Docker
    Desktop:
  - Changed `storageClassName: standard` to `hostpath`
  - Updated `accessModes` from `ReadWriteMany` to `ReadWriteOnce`
  - All 6 PVCs now use correct storage class

- **Service Discovery:** Fixed service hostname resolution:
  - **Service Discovery:** Corrigida resolução de nomes de serviços:
  - Updated ConfigMap patches to use prefixed service names
    (dev-postgres-service, dev-redis-service)
  - Fixed Nginx upstream to point to dev-django-service
  - Corrected all cross-service references

- **Environment Configuration:** Fixed Django settings for Kubernetes:
  - **Configuração de Ambiente:** Corrigidas settings do Django para Kubernetes:
  - Dev overlay now uses `django_base.settings.dev` instead of prod
  - Added proper SECRET_KEY generation (70+ characters)
  - Added POSTGRES_PASSWORD to django-secrets
  - Environment validation passes in development mode

- **Container Configuration:** Fixed Django container initialization:
  - **Configuração de Containers:** Corrigida inicialização dos containers
    Django:
  - Added `imagePullPolicy: Never` for local development images
  - Added `PYTHONPATH=/app/src` to all Django containers
  - Fixed command execution with `/bin/sh -c` and multi-line args
  - Init containers (migrations, collectstatic) now run successfully

- **Health Checks:** Fixed Nginx health probe configuration:
  - **Health Checks:** Corrigida configuração de health probes do Nginx:
  - Changed from `httpGet` to `tcpSocket` probes
  - Prevents CrashLoopBackOff when Django is not ready yet
  - More reliable liveness and readiness checks

### Documentation - Comprehensive Updates / Atualizações Abrangentes

- **Complete Documentation Overhaul:** Major documentation additions:
  - **Revisão Completa da Documentação:** Grandes adições de documentação:
  - Added `scripts/README.md` - Complete backup/restore documentation (~500
    lines)
  - Added `docs/SSL_HTTPS_SETUP.md` - Production HTTPS setup guide (~800 lines)
  - Added `docs/JWT_AUTHENTICATION.md` - JWT authentication guide (~500 lines)
  - Added `CONTRIBUTING.md` - Contribution guidelines (~400 lines)
  - Added `TODOLIST.md` - Project roadmap (~400 lines)
  - Updated `README.md` - Enhanced feature descriptions and structure
  - Updated `CHANGELOG.md` - This file with complete v1.2.0 details

- **Inline Documentation:** All new code includes:
  - **Documentação Inline:** Todo código novo inclui:
  - Bilingual docstrings (EN/PT-BR)
  - Comprehensive comments
  - Usage examples
  - Type hints where applicable

---

## [1.1.0] - 2025-10-10

This version focuses on modernizing the development environment, updating
dependencies, and reinforcing security and performance configurations, aligning
the project with the latest best practices. Esta versão foca na modernização do
ambiente de desenvolvimento, atualização de dependências e reforço das
configurações de segurança e performance, alinhando o projeto com as práticas
mais recentes.

### Changed - Infrastructure & Environment / Infraestrutura e Ambiente

- **Python Update:** The development and production environment has been
  upgraded to use **Python 3.14**, ensuring access to the latest language
  features and performance improvements.
- **Atualização do Python:** O ambiente de desenvolvimento e produção foi
  atualizado para usar **Python 3.14**, garantindo acesso aos recursos mais
  recentes e melhorias de performance da linguagem.
- **Dependency Upgrade:** All project dependencies (such as Django, DRF, Ruff,
  etc.) have been updated to their latest stable versions, ensuring better
  security and new features.
  - **Atualização de Dependências:** Todas as dependências do projeto (como
    Django, DRF, Ruff, etc.) foram atualizadas para as suas versões mais
    recentes e estáveis, garantindo mais segurança e novas funcionalidades.
- **`docker-compose.yml` Improvement:** Docker volumes now have explicit names
  (e.g., `django_base_postgres_data`), which simplifies management and prevents
  conflicts.
  - **Melhoria no `docker-compose.yml`:** Os volumes do Docker agora têm nomes
    explícitos (ex: `django_base_postgres_data`), facilitando a gestão e
    evitando conflitos.
- **CI Pipeline Update:** The GitHub Actions workflow (`ci.yml`) has been
  updated to use Python 3.13 and Postgres 16, ensuring that continuous
  integration runs in a modern environment.
  - **Atualização do Pipeline de CI:** O workflow do GitHub Actions (`ci.yml`)
    foi atualizado para usar Python 3.13 e Postgres 16, garantindo que a
    integração contínua rode num ambiente moderno.

### Changed - Code Quality & DX (Developer Experience) / Qualidade de Código e DX

- **Pre-commit Hooks Update:** The code verification tools (`ruff`, `bandit`,
  etc.) in `.pre-commit-config.yaml` have been updated to their latest versions,
  improving code analysis and formatting.
  - **Atualização dos Pre-commit Hooks:** As ferramentas de verificação de
    código (`ruff`, `bandit`, etc.) no `.pre-commit-config.yaml` foram
    atualizadas para as suas versões mais recentes, melhorando a análise e
    formatação do código.
- **`.gitignore` Improvement:** The `node_modules/` folder has been added to
  `.gitignore` to prevent frontend dependencies from being versioned.
  - **Melhoria no `.gitignore`:** Adicionada a pasta `node_modules/` ao
    `.gitignore` para evitar que dependências de frontend sejam versionadas.

### Changed - Security & Performance / Segurança e Performance

- **Nginx Security Hardening:** The `Permissions-Policy` header has been added
  to the `nginx.conf` configuration to restrict the use of sensitive browser
  features, increasing application security.
  - **Reforço de Segurança no Nginx:** Adicionado o cabeçalho
    `Permissions-Policy` à configuração do `nginx.conf` para restringir o uso de
    funcionalidades sensíveis do navegador, aumentando a segurança da aplicação.
- **Database Optimization:** `Meta.indexes` have been added to the
  `UserProfile`, `Category`, and `Tag` models. This speeds up database queries
  that use these fields for filtering, improving API performance.
  - **Otimização da Base de Dados:** Adicionados `Meta.indexes` aos modelos
    `UserProfile`, `Category` e `Tag`. Isto acelera as consultas à base de dados
    que usam estes campos para filtros, melhorando a performance da API.
- **Cookie Security:** The production configuration (`prod.py`) has been
  adjusted to use `SESSION_COOKIE_SAMESITE = 'Strict'`, offering more robust
  protection against CSRF attacks.
  - **Segurança de Cookies:** A configuração de produção (`prod.py`) foi
    ajustada para usar `SESSION_COOKIE_SAMESITE = 'Strict'`, oferecendo uma
    proteção mais robusta contra ataques CSRF.

### Changed - Documentation / Documentação

- **CI Status Badge:** A CI/CD pipeline status badge has been added to
  `README.md`, visually showing whether the tests are passing.
  - **Badge de Status do CI:** Adicionado um badge de status do pipeline de
    CI/CD ao `README.md`, mostrando visualmente se os testes estão a passar.
