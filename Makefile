# Makefile for Django Base Project
# Makefile para Projeto Django Base

# Docker Compose files / Arquivos do Docker Compose
COMPOSE_DEV = docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev
COMPOSE_PROD = docker-compose --profile prod

# Colors for output / Cores para output
BLUE = \033[0;34m
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help
help: ## Show this help message / Mostra esta mensagem de ajuda
	@echo "$(BLUE)Django Base Project - Available Commands$(NC)"
	@echo "$(BLUE)Projeto Django Base - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-25s$(NC) %s\n", $$1, $$2}'

# =============================================================================
# DEVELOPMENT COMMANDS / COMANDOS DE DESENVOLVIMENTO
# =============================================================================

.PHONY: setup
setup: ## Initial project setup (dev) / Configuração inicial do projeto (dev)
	@echo "$(BLUE)Setting up Django Base project (development)...$(NC)"
	@bash setup.sh

.PHONY: setup-prod
setup-prod: ## Initial production setup / Configuração inicial de produção
	@echo "$(BLUE)Setting up Django Base project (PRODUCTION)...$(NC)"
	@bash setup-prod.sh

.PHONY: dev
dev: ## Start development environment / Inicia ambiente de desenvolvimento
	@echo "$(BLUE)Starting development environment...$(NC)"
	$(COMPOSE_DEV) up

.PHONY: dev-build
dev-build: ## Build and start dev environment / Constrói e inicia ambiente dev
	@echo "$(BLUE)Building and starting development environment...$(NC)"
	$(COMPOSE_DEV) up --build

.PHONY: dev-down
dev-down: ## Stop development environment / Para ambiente de desenvolvimento
	@echo "$(YELLOW)Stopping development environment...$(NC)"
	$(COMPOSE_DEV) down

.PHONY: dev-logs
dev-logs: ## Show dev logs / Mostra logs do dev
	$(COMPOSE_DEV) logs -f

# =============================================================================
# PRODUCTION COMMANDS / COMANDOS DE PRODUÇÃO
# =============================================================================

.PHONY: prod
prod: ## Start production environment / Inicia ambiente de produção
	@echo "$(BLUE)Starting production environment...$(NC)"
	$(COMPOSE_PROD) up -d

.PHONY: prod-build
prod-build: ## Build and start prod environment / Constrói e inicia ambiente prod
	@echo "$(BLUE)Building and starting production environment...$(NC)"
	$(COMPOSE_PROD) up --build -d

.PHONY: prod-down
prod-down: ## Stop production environment / Para ambiente de produção
	@echo "$(YELLOW)Stopping production environment...$(NC)"
	$(COMPOSE_PROD) down

.PHONY: prod-logs
prod-logs: ## Show prod logs / Mostra logs do prod
	$(COMPOSE_PROD) logs -f

# =============================================================================
# DJANGO COMMANDS / COMANDOS DO DJANGO
# =============================================================================

.PHONY: shell
shell: ## Open Django shell / Abre shell do Django
	docker-compose exec web python manage.py shell

.PHONY: bash
bash: ## Open bash shell in web container / Abre bash no container web
	docker-compose exec web bash

.PHONY: migrate
migrate: ## Run database migrations / Executa migrações do banco
	@echo "$(BLUE)Running migrations...$(NC)"
	docker-compose exec web python manage.py migrate

.PHONY: makemigrations
makemigrations: ## Create new migrations / Cria novas migrações
	@echo "$(BLUE)Creating migrations...$(NC)"
	docker-compose exec web python manage.py makemigrations

.PHONY: superuser
superuser: ## Create superuser / Cria superusuário
	docker-compose exec web python manage.py createsuperuser

.PHONY: seed
seed: ## Seed database with test data / Popula banco com dados de teste
	@echo "$(BLUE)Seeding database...$(NC)"
	docker-compose exec web python manage.py seed_database

.PHONY: collectstatic
collectstatic: ## Collect static files / Coleta arquivos estáticos
	@echo "$(BLUE)Collecting static files...$(NC)"
	docker-compose exec web python manage.py collectstatic --noinput

# =============================================================================
# TESTING COMMANDS / COMANDOS DE TESTE
# =============================================================================

.PHONY: test
test: ## Run all tests / Executa todos os testes
	@echo "$(BLUE)Running tests...$(NC)"
	docker-compose exec web python manage.py test src

.PHONY: test-app
test-app: ## Run tests for specific app (usage: make test-app APP=core) / Executa testes de app específica
	@echo "$(BLUE)Running tests for $(APP)...$(NC)"
	docker-compose exec web python manage.py test src.$(APP)

.PHONY: coverage
coverage: ## Run tests with coverage / Executa testes com cobertura
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	docker-compose exec web coverage run manage.py test src
	docker-compose exec web coverage report

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report / Gera relatório HTML de cobertura
	@echo "$(BLUE)Generating HTML coverage report...$(NC)"
	docker-compose exec web coverage run manage.py test src
	docker-compose exec web coverage html
	@echo "$(GREEN)Coverage report generated at htmlcov/index.html$(NC)"

# =============================================================================
# CODE QUALITY COMMANDS / COMANDOS DE QUALIDADE DE CÓDIGO
# =============================================================================

.PHONY: lint
lint: ## Run Ruff linter / Executa linter Ruff
	@echo "$(BLUE)Running Ruff linter...$(NC)"
	docker-compose exec web ruff check .

.PHONY: lint-fix
lint-fix: ## Run Ruff linter with auto-fix / Executa linter Ruff com auto-correção
	@echo "$(BLUE)Running Ruff linter with auto-fix...$(NC)"
	docker-compose exec web ruff check --fix .

.PHONY: format
format: ## Format code with Ruff / Formata código com Ruff
	@echo "$(BLUE)Formatting code with Ruff...$(NC)"
	docker-compose exec web ruff format .

.PHONY: format-check
format-check: ## Check code formatting / Verifica formatação do código
	@echo "$(BLUE)Checking code formatting...$(NC)"
	docker-compose exec web ruff format --check .

.PHONY: security
security: ## Run security checks with Bandit / Executa verificações de segurança com Bandit
	@echo "$(BLUE)Running security checks...$(NC)"
	docker-compose exec web bandit -r src/ -ll

.PHONY: check
check: lint format-check security ## Run all code quality checks / Executa todas verificações de qualidade
	@echo "$(GREEN)All checks completed!$(NC)"

# =============================================================================
# DATABASE COMMANDS / COMANDOS DE BANCO DE DADOS
# =============================================================================

.PHONY: db-shell
db-shell: ## Open PostgreSQL shell / Abre shell do PostgreSQL
	docker-compose exec db psql -U django_user -d django_db

.PHONY: db-backup
db-backup: ## Backup database / Faz backup do banco
	@echo "$(BLUE)Creating database backup...$(NC)"
	@mkdir -p backups
	docker-compose exec -T db pg_dump -U django_user django_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Backup created in backups/ directory$(NC)"

.PHONY: db-restore
db-restore: ## Restore database from backup (usage: make db-restore FILE=backup.sql) / Restaura banco de backup
	@echo "$(YELLOW)Restoring database from $(FILE)...$(NC)"
	docker-compose exec -T db psql -U django_user -d django_db < $(FILE)
	@echo "$(GREEN)Database restored!$(NC)"

.PHONY: db-reset
db-reset: ## Reset database (WARNING: deletes all data) / Reseta banco (ATENÇÃO: deleta todos dados)
	@echo "$(RED)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(YELLOW)Resetting database...$(NC)"; \
		docker-compose exec web python manage.py flush --noinput; \
		echo "$(GREEN)Database reset complete!$(NC)"; \
	fi

# =============================================================================
# DOCKER COMMANDS / COMANDOS DO DOCKER
# =============================================================================

.PHONY: build
build: ## Build Docker images / Constrói imagens Docker
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build

.PHONY: up
up: ## Start all containers / Inicia todos containers
	docker-compose up -d

.PHONY: down
down: ## Stop all containers / Para todos containers
	docker-compose down

.PHONY: restart
restart: down up ## Restart all containers / Reinicia todos containers

.PHONY: ps
ps: ## Show container status / Mostra status dos containers
	docker-compose ps

.PHONY: logs
logs: ## Show logs from all containers / Mostra logs de todos containers
	docker-compose logs -f

.PHONY: clean
clean: ## Remove containers, volumes, and orphans / Remove containers, volumes e órfãos
	@echo "$(YELLOW)Cleaning up Docker resources...$(NC)"
	docker-compose down -v --remove-orphans
	@echo "$(GREEN)Cleanup complete!$(NC)"

.PHONY: prune
prune: ## Prune all unused Docker resources / Remove recursos Docker não usados
	@echo "$(RED)WARNING: This will remove all unused Docker resources!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker system prune -af --volumes; \
		echo "$(GREEN)Prune complete!$(NC)"; \
	fi

# =============================================================================
# TRANSLATION COMMANDS / COMANDOS DE TRADUÇÃO
# =============================================================================

.PHONY: messages
messages: ## Create/update translation files / Cria/atualiza arquivos de tradução
	@echo "$(BLUE)Creating/updating translation files...$(NC)"
	docker-compose exec web python manage.py makemessages -l pt_BR -l en

.PHONY: compile-messages
compile-messages: ## Compile translation files / Compila arquivos de tradução
	@echo "$(BLUE)Compiling translation files...$(NC)"
	docker-compose exec web python manage.py compilemessages

# =============================================================================
# MONITORING COMMANDS / COMANDOS DE MONITORAMENTO
# =============================================================================

.PHONY: health
health: ## Check application health / Verifica saúde da aplicação
	@echo "$(BLUE)Checking application health...$(NC)"
	@curl -f http://localhost:8000/health/ || echo "$(RED)Health check failed!$(NC)"

.PHONY: prometheus
prometheus: ## Open Prometheus (http://localhost:9090) / Abre Prometheus
	@echo "$(BLUE)Opening Prometheus...$(NC)"
	@python -m webbrowser http://localhost:9090 || echo "Open http://localhost:9090 in your browser"

.PHONY: grafana
grafana: ## Open Grafana (http://localhost:3000) / Abre Grafana
	@echo "$(BLUE)Opening Grafana...$(NC)"
	@python -m webbrowser http://localhost:3000 || echo "Open http://localhost:3000 in your browser"

# =============================================================================
# UTILITY COMMANDS / COMANDOS UTILITÁRIOS
# =============================================================================

.PHONY: requirements
requirements: ## Show installed Python packages / Mostra pacotes Python instalados
	docker-compose exec web uv pip list

.PHONY: outdated
outdated: ## Show outdated packages / Mostra pacotes desatualizados
	docker-compose exec web uv pip list --outdated

.PHONY: install
install: ## Install a package (usage: make install PKG=package-name) / Instala um pacote
	@echo "$(BLUE)Installing $(PKG)...$(NC)"
	docker-compose exec web uv pip install $(PKG)
	@echo "$(YELLOW)Don't forget to update pyproject.toml!$(NC)"

.PHONY: docs
docs: ## Open API documentation / Abre documentação da API
	@echo "$(BLUE)Opening API documentation...$(NC)"
	@python -m webbrowser http://localhost:8000/api/docs/ || echo "Open http://localhost:8000/api/docs/ in your browser"

.PHONY: admin
admin: ## Open Django admin / Abre admin do Django
	@echo "$(BLUE)Opening Django admin...$(NC)"
	@python -m webbrowser http://localhost:8000/admin/ || echo "Open http://localhost:8000/admin/ in your browser"

# =============================================================================
# KUBERNETES COMMANDS / COMANDOS DO KUBERNETES
# =============================================================================

.PHONY: setup-k8s
setup-k8s: ## Automated Kubernetes setup (dev) / Setup automatizado do Kubernetes (dev)
	@echo "$(BLUE)Setting up Kubernetes (development)...$(NC)"
	@bash setup-k8s.sh

.PHONY: setup-k8s-prod
setup-k8s-prod: ## Automated Kubernetes setup (prod) / Setup automatizado do Kubernetes (prod)
	@echo "$(BLUE)Setting up Kubernetes (PRODUCTION)...$(NC)"
	@bash setup-k8s.sh --prod

.PHONY: k8s-dev-deploy
k8s-dev-deploy: ## Deploy to Kubernetes (dev) / Deploy no Kubernetes (dev)
	@echo "$(BLUE)Deploying to Kubernetes (dev)...$(NC)"
	kubectl apply -k k8s/dev/
	@echo "$(GREEN)Deploy complete! Check status with: make k8s-status$(NC)"

.PHONY: k8s-prod-deploy
k8s-prod-deploy: ## Deploy to Kubernetes (prod) / Deploy no Kubernetes (prod)
	@echo "$(RED)Deploying to Kubernetes (PRODUCTION)...$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		kubectl apply -k k8s/prod/; \
		echo "$(GREEN)Deploy complete!$(NC)"; \
	fi

.PHONY: k8s-delete
k8s-delete: ## Delete from Kubernetes / Remove do Kubernetes
	@echo "$(YELLOW)Deleting Kubernetes resources...$(NC)"
	kubectl delete namespace django-base
	@echo "$(GREEN)Resources deleted!$(NC)"

.PHONY: k8s-status
k8s-status: ## Show Kubernetes status / Mostra status do Kubernetes
	@echo "$(BLUE)Kubernetes Status:$(NC)"
	kubectl get all -n django-base

.PHONY: k8s-pods
k8s-pods: ## Show Kubernetes pods / Mostra pods do Kubernetes
	kubectl get pods -n django-base -w

.PHONY: k8s-logs
k8s-logs: ## Show logs from Django pod / Mostra logs do pod Django
	kubectl logs -n django-base -l app=django,component=web --tail=100 -f

.PHONY: k8s-shell
k8s-shell: ## Open shell in Django pod / Abre shell no pod Django
	kubectl exec -it -n django-base deployment/django-web -- /bin/sh

.PHONY: k8s-migrate
k8s-migrate: ## Run migrations in Kubernetes / Executa migrations no Kubernetes
	@echo "$(BLUE)Running migrations in Kubernetes...$(NC)"
	kubectl exec -n django-base deployment/django-web -- /app/.venv/bin/python manage.py migrate

.PHONY: k8s-port-forward
k8s-port-forward: ## Port forward to Django service / Port forward para serviço Django
	@echo "$(BLUE)Port forwarding to Django (localhost:8000)...$(NC)"
	kubectl port-forward -n django-base svc/nginx-service 8000:80

.PHONY: k8s-grafana
k8s-grafana: ## Port forward to Grafana / Port forward para Grafana
	@echo "$(BLUE)Port forwarding to Grafana (localhost:3000)...$(NC)"
	kubectl port-forward -n django-base svc/grafana-service 3000:3000

.PHONY: k8s-prometheus
k8s-prometheus: ## Port forward to Prometheus / Port forward para Prometheus
	@echo "$(BLUE)Port forwarding to Prometheus (localhost:9090)...$(NC)"
	kubectl port-forward -n django-base svc/prometheus-service 9090:9090

.PHONY: k8s-scale
k8s-scale: ## Scale Django deployment (usage: make k8s-scale REPLICAS=3) / Escala deployment Django
	@echo "$(BLUE)Scaling Django to $(REPLICAS) replicas...$(NC)"
	kubectl scale deployment/django-web --replicas=$(REPLICAS) -n django-base

.PHONY: k8s-rollout-status
k8s-rollout-status: ## Check rollout status / Verifica status do rollout
	kubectl rollout status deployment/django-web -n django-base

.PHONY: k8s-rollback
k8s-rollback: ## Rollback Django deployment / Rollback do deployment Django
	@echo "$(YELLOW)Rolling back Django deployment...$(NC)"
	kubectl rollout undo deployment/django-web -n django-base
	@echo "$(GREEN)Rollback complete!$(NC)"

.PHONY: k8s-describe
k8s-describe: ## Describe Kubernetes resources / Descreve recursos Kubernetes
	kubectl describe all -n django-base

.PHONY: k8s-events
k8s-events: ## Show Kubernetes events / Mostra eventos do Kubernetes
	kubectl get events -n django-base --sort-by='.lastTimestamp'

# =============================================================================
# GIT COMMANDS / COMANDOS DO GIT
# =============================================================================

.PHONY: commit
commit: check ## Run checks and commit (interactive) / Executa verificações e commita
	@echo "$(GREEN)All checks passed! Ready to commit.$(NC)"
	git add .
	git commit

.PHONY: precommit
precommit: ## Run pre-commit hooks manually / Executa hooks de pre-commit manualmente
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files

# =============================================================================
# DEFAULT TARGET / ALVO PADRÃO
# =============================================================================

.DEFAULT_GOAL := help
