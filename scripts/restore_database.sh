#!/bin/bash
# Database Restore Script for Django Base Project
# Script de Restauração do Banco de Dados para Projeto Django Base

# This script restores a PostgreSQL database from a compressed backup file.
# It includes safety checks and confirmation prompts to prevent accidental data loss.
#
# Este script restaura um banco de dados PostgreSQL de um arquivo de backup comprimido.
# Inclui verificações de segurança e prompts de confirmação para prevenir perda acidental de dados.

set -e  # Exit immediately if a command exits with a non-zero status / Sai imediatamente se um comando falhar

# Colors for output / Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration / Configuração
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="${PROJECT_ROOT}/backups/database"

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

# Function to print messages / Função para imprimir mensagens
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Function to list available backups / Função para listar backups disponíveis
list_backups() {
    echo ""
    info "=========================================="
    info "Available backups / Backups disponíveis:"
    info "=========================================="

    if ls "${BACKUP_DIR}"/backup_*.sql.gz 1> /dev/null 2>&1; then
        local i=1
        for backup in $(ls -t "${BACKUP_DIR}"/backup_*.sql.gz); do
            local size=$(du -h "$backup" | cut -f1)
            local date=$(stat -c %y "$backup" 2>/dev/null || stat -f "%Sm" "$backup" 2>/dev/null || echo "Unknown")
            echo "${i}. $(basename "$backup") - ${size} - ${date}"
            ((i++))
        done
    else
        error "No backups found in ${BACKUP_DIR}"
        error "Nenhum backup encontrado em ${BACKUP_DIR}"
        exit 1
    fi
    echo ""
}

# Function to select backup file / Função para selecionar arquivo de backup
select_backup() {
    local backup_file="$1"

    # If backup file provided as argument / Se arquivo de backup fornecido como argumento
    if [ -n "$backup_file" ]; then
        if [ -f "$backup_file" ]; then
            echo "$backup_file"
            return 0
        elif [ -f "${BACKUP_DIR}/$backup_file" ]; then
            echo "${BACKUP_DIR}/$backup_file"
            return 0
        else
            error "Backup file not found / Arquivo de backup não encontrado: $backup_file"
            exit 1
        fi
    fi

    # Interactive selection / Seleção interativa
    list_backups

    local backups=($(ls -t "${BACKUP_DIR}"/backup_*.sql.gz))
    local backup_count=${#backups[@]}

    read -p "Select backup number (1-${backup_count}) or 'q' to quit: " selection

    if [ "$selection" = "q" ]; then
        log "Restore cancelled / Restauração cancelada"
        exit 0
    fi

    if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le "$backup_count" ]; then
        echo "${backups[$((selection-1))]}"
    else
        error "Invalid selection / Seleção inválida"
        exit 1
    fi
}

# Function to verify backup file / Função para verificar arquivo de backup
verify_backup() {
    local backup_file="$1"

    log "Verifying backup file / Verificando arquivo de backup..."

    if [ ! -f "$backup_file" ]; then
        error "Backup file does not exist / Arquivo de backup não existe: $backup_file"
        return 1
    fi

    if ! gzip -t "$backup_file" 2>/dev/null; then
        error "Backup file is corrupted / Arquivo de backup está corrompido"
        return 1
    fi

    log "✓ Backup file is valid / Arquivo de backup é válido"
    return 0
}

# Function to confirm restore / Função para confirmar restauração
confirm_restore() {
    local backup_file="$1"

    warning "=========================================="
    warning "⚠️  WARNING / AVISO"
    warning "=========================================="
    warning "This will REPLACE ALL DATA in the database!"
    warning "Isto irá SUBSTITUIR TODOS OS DADOS no banco de dados!"
    warning ""
    warning "Database / Banco: ${DB_NAME}"
    warning "Backup file / Arquivo de backup: $(basename "$backup_file")"
    warning "=========================================="
    echo ""

    read -p "Are you sure you want to continue? Type 'yes' to confirm: " confirmation

    if [ "$confirmation" != "yes" ]; then
        log "Restore cancelled / Restauração cancelada"
        exit 0
    fi

    echo ""
    read -p "Last chance! Type 'RESTORE' in capital letters to proceed: " final_confirmation

    if [ "$final_confirmation" != "RESTORE" ]; then
        log "Restore cancelled / Restauração cancelada"
        exit 0
    fi
}

# Function to create pre-restore backup / Função para criar backup pré-restauração
create_pre_restore_backup() {
    log "Creating pre-restore backup / Criando backup pré-restauração..."

    local pre_restore_backup="${BACKUP_DIR}/pre_restore_backup_${DB_NAME}_$(date +"%Y%m%d_%H%M%S").sql.gz"

    if docker ps | grep -q "${DB_CONTAINER}"; then
        if docker exec -t "${DB_CONTAINER}" pg_dump -U "${DB_USER}" -d "${DB_NAME}" --no-owner --clean | gzip > "${pre_restore_backup}"; then
            log "✓ Pre-restore backup created / Backup pré-restauração criado: $(basename "$pre_restore_backup")"
        else
            warning "Failed to create pre-restore backup / Falha ao criar backup pré-restauração"
            read -p "Continue without pre-restore backup? (yes/no): " continue_without_backup
            if [ "$continue_without_backup" != "yes" ]; then
                exit 1
            fi
        fi
    elif command -v pg_dump &> /dev/null; then
        if PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" --no-owner --clean | gzip > "${pre_restore_backup}"; then
            log "✓ Pre-restore backup created / Backup pré-restauração criado: $(basename "$pre_restore_backup")"
        else
            warning "Failed to create pre-restore backup / Falha ao criar backup pré-restauração"
        fi
    fi
}

# Function to restore database / Função para restaurar banco de dados
restore_database() {
    local backup_file="$1"

    log "=========================================="
    log "Starting database restore / Iniciando restauração do banco"
    log "Database / Banco: ${DB_NAME}"
    log "Backup file / Arquivo de backup: $(basename "$backup_file")"
    log "=========================================="

    # Check if running in Docker or local / Verifica se está rodando em Docker ou local
    if docker ps | grep -q "${DB_CONTAINER}"; then
        log "Docker container detected / Container Docker detectado: ${DB_CONTAINER}"
        log "Restoring from Docker container..."

        # Restore to Docker container / Restaurar para container Docker
        if gunzip < "${backup_file}" | docker exec -i "${DB_CONTAINER}" psql -U "${DB_USER}" -d "${DB_NAME}"; then
            log "✓ Database restored successfully from Docker / Banco restaurado com sucesso do Docker"
        else
            error "Failed to restore database from Docker / Falha ao restaurar banco do Docker"
            return 1
        fi

    elif command -v psql &> /dev/null; then
        log "Local PostgreSQL installation detected / Instalação local do PostgreSQL detectada"
        log "Restoring to local database..."

        # Restore to local PostgreSQL / Restaurar para PostgreSQL local
        if gunzip < "${backup_file}" | PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}"; then
            log "✓ Database restored successfully to local database / Banco restaurado com sucesso para banco local"
        else
            error "Failed to restore database to local database / Falha ao restaurar banco para banco local"
            return 1
        fi

    else
        error "Neither Docker container nor local psql found / Container Docker nem psql local encontrado"
        error "Please ensure PostgreSQL is running or use Docker / Por favor, certifique-se de que o PostgreSQL está rodando ou use Docker"
        return 1
    fi
}

# Usage information / Informações de uso
usage() {
    echo ""
    echo "Usage / Uso:"
    echo "  $0 [backup_file]"
    echo ""
    echo "Examples / Exemplos:"
    echo "  $0                                    # Interactive mode / Modo interativo"
    echo "  $0 backup_django_db_20250112.sql.gz  # Restore specific backup / Restaurar backup específico"
    echo ""
}

# Main execution / Execução principal
main() {
    local backup_file

    # Check for help flag / Verifica flag de ajuda
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        usage
        exit 0
    fi

    # Select backup file / Selecionar arquivo de backup
    backup_file=$(select_backup "$1")

    # Verify backup file / Verificar arquivo de backup
    if ! verify_backup "$backup_file"; then
        error "Backup verification failed / Verificação do backup falhou"
        exit 1
    fi

    # Confirm restore / Confirmar restauração
    confirm_restore "$backup_file"

    # Create pre-restore backup / Criar backup pré-restauração
    create_pre_restore_backup

    # Restore database / Restaurar banco de dados
    if restore_database "$backup_file"; then
        log "=========================================="
        log "✓ Restore completed successfully / Restauração concluída com sucesso"
        log "=========================================="
        return 0
    else
        error "Restore failed / Restauração falhou"
        return 1
    fi
}

# Run main function / Executa função principal
main "$@"

# Exit with appropriate status code / Sai com código de status apropriado
exit $?
