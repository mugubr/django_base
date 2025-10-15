#!/bin/bash
# Database Backup Script for Django Base Project
# Script de Backup do Banco de Dados para Projeto Django Base

# This script creates compressed PostgreSQL backups with timestamps
# and supports retention policies to manage disk space.
#
# Este script cria backups comprimidos do PostgreSQL com timestamps
# e suporta políticas de retenção para gerenciar espaço em disco.

set -e  # Exit immediately if a command exits with a non-zero status / Sai imediatamente se um comando falhar

# Colors for output / Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration / Configuração
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="${PROJECT_ROOT}/backups/database"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS=${RETENTION_DAYS:-30}  # Keep backups for 30 days by default / Manter backups por 30 dias por padrão

# Load environment variables / Carrega variáveis de ambiente
if [ -f "${PROJECT_ROOT}/.env" ]; then
    export $(grep -v '^#' "${PROJECT_ROOT}/.env" | xargs)
fi

# Database configuration / Configuração do banco de dados
DB_NAME=${POSTGRES_DB:-django_db}
DB_USER=${POSTGRES_USER:-postgres}
DB_HOST=${POSTGRES_HOST:-localhost}
DB_PORT=${POSTGRES_PORT:-5432}
DB_CONTAINER=${DB_CONTAINER:-django_base-db-1}  # Docker container name / Nome do container Docker

# Backup filename / Nome do arquivo de backup
BACKUP_FILE="${BACKUP_DIR}/backup_${DB_NAME}_${TIMESTAMP}.sql.gz"
BACKUP_LOG="${BACKUP_DIR}/backup.log"

# Function to print messages / Função para imprimir mensagens
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "${BACKUP_LOG}"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[ERROR] $1" >> "${BACKUP_LOG}"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[WARNING] $1" >> "${BACKUP_LOG}"
}

# Create backup directory if it doesn't exist / Cria diretório de backup se não existir
mkdir -p "${BACKUP_DIR}"

# Main backup function / Função principal de backup
backup_database() {
    log "=========================================="
    log "Starting database backup / Iniciando backup do banco"
    log "Database / Banco: ${DB_NAME}"
    log "Backup file / Arquivo de backup: ${BACKUP_FILE}"
    log "=========================================="

    # Check if running in Docker or local / Verifica se está rodando em Docker ou local
    if docker ps | grep -q "${DB_CONTAINER}"; then
        log "Docker container detected / Container Docker detectado: ${DB_CONTAINER}"
        log "Creating backup from Docker container..."

        # Backup from Docker container / Backup do container Docker
        if docker exec -t "${DB_CONTAINER}" pg_dump -U "${DB_USER}" -d "${DB_NAME}" --no-owner --clean | gzip > "${BACKUP_FILE}"; then
            log "✓ Backup created successfully from Docker / Backup criado com sucesso do Docker"
        else
            error "Failed to create backup from Docker / Falha ao criar backup do Docker"
            return 1
        fi

    elif command -v pg_dump &> /dev/null; then
        log "Local PostgreSQL installation detected / Instalação local do PostgreSQL detectada"
        log "Creating backup from local database..."

        # Backup from local PostgreSQL / Backup do PostgreSQL local
        if PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" --no-owner --clean | gzip > "${BACKUP_FILE}"; then
            log "✓ Backup created successfully from local database / Backup criado com sucesso do banco local"
        else
            error "Failed to create backup from local database / Falha ao criar backup do banco local"
            return 1
        fi

    else
        error "Neither Docker container nor local pg_dump found / Container Docker nem pg_dump local encontrado"
        error "Please ensure PostgreSQL is running or use Docker / Por favor, certifique-se de que o PostgreSQL está rodando ou use Docker"
        return 1
    fi

    # Check backup file size / Verifica tamanho do arquivo de backup
    if [ -f "${BACKUP_FILE}" ]; then
        BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
        log "✓ Backup size / Tamanho do backup: ${BACKUP_SIZE}"
        log "✓ Backup location / Localização do backup: ${BACKUP_FILE}"
    else
        error "Backup file was not created / Arquivo de backup não foi criado"
        return 1
    fi
}

# Function to clean old backups / Função para limpar backups antigos
cleanup_old_backups() {
    log "Cleaning up old backups / Limpando backups antigos (older than ${RETENTION_DAYS} days)..."

    # Find and delete old backups / Encontra e deleta backups antigos
    DELETED_COUNT=0
    while IFS= read -r old_backup; do
        if [ -f "$old_backup" ]; then
            log "Deleting old backup / Deletando backup antigo: $(basename "$old_backup")"
            rm -f "$old_backup"
            ((DELETED_COUNT++))
        fi
    done < <(find "${BACKUP_DIR}" -name "backup_*.sql.gz" -type f -mtime +"${RETENTION_DAYS}")

    if [ $DELETED_COUNT -gt 0 ]; then
        log "✓ Deleted ${DELETED_COUNT} old backup(s) / Deletados ${DELETED_COUNT} backup(s) antigo(s)"
    else
        log "No old backups to delete / Nenhum backup antigo para deletar"
    fi
}

# Function to list recent backups / Função para listar backups recentes
list_backups() {
    log "Recent backups / Backups recentes:"
    if ls "${BACKUP_DIR}"/backup_*.sql.gz 1> /dev/null 2>&1; then
        ls -lh "${BACKUP_DIR}"/backup_*.sql.gz | tail -n 5 | awk '{print "  - " $9 " (" $5 ")"}'
    else
        warning "No backups found / Nenhum backup encontrado"
    fi
}

# Function to verify backup integrity / Função para verificar integridade do backup
verify_backup() {
    log "Verifying backup integrity / Verificando integridade do backup..."

    if gzip -t "${BACKUP_FILE}" 2>/dev/null; then
        log "✓ Backup integrity verified / Integridade do backup verificada"
        return 0
    else
        error "Backup file is corrupted / Arquivo de backup está corrompido"
        return 1
    fi
}

# Main execution / Execução principal
main() {
    # Create backup / Criar backup
    if backup_database; then
        # Verify backup / Verificar backup
        if verify_backup; then
            # Cleanup old backups / Limpar backups antigos
            cleanup_old_backups

            # List recent backups / Listar backups recentes
            list_backups

            log "=========================================="
            log "✓ Backup completed successfully / Backup concluído com sucesso"
            log "=========================================="
            return 0
        else
            error "Backup verification failed / Verificação do backup falhou"
            return 1
        fi
    else
        error "Backup failed / Backup falhou"
        return 1
    fi
}

# Run main function / Executa função principal
main

# Exit with appropriate status code / Sai com código de status apropriado
exit $?
