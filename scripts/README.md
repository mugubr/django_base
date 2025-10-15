# Database Management Scripts / Scripts de Gerenciamento de Banco de Dados

🇬🇧 / 🇺🇸 **English** | 🇧🇷 **Português**

---

## English

### Overview

This directory contains scripts for database backup and restore operations.
These scripts support both Docker-based and local PostgreSQL installations.

### Available Scripts

#### 1. `backup_database.sh` - Database Backup

Creates compressed PostgreSQL backups with automatic retention management.

**Features:**

- ✅ Compressed backups (gzip) to save disk space
- ✅ Timestamped filenames for easy identification
- ✅ Automatic cleanup of old backups (configurable retention period)
- ✅ Backup integrity verification
- ✅ Supports Docker and local PostgreSQL
- ✅ Detailed logging with colored output

**Usage:**

```bash
# Basic usage / Uso básico
./scripts/backup_database.sh

# With custom retention period (days) / Com período de retenção customizado (dias)
RETENTION_DAYS=7 ./scripts/backup_database.sh

# Via Docker Compose / Via Docker Compose
docker-compose exec web bash -c "./scripts/backup_database.sh"
```

**Configuration:**

The script automatically loads configuration from `.env` file. Key variables:

- `POSTGRES_DB` - Database name (default: django_db)
- `POSTGRES_USER` - Database user (default: postgres)
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_HOST` - Database host (default: localhost)
- `POSTGRES_PORT` - Database port (default: 5432)
- `DB_CONTAINER` - Docker container name (default: django_base-db-1)
- `RETENTION_DAYS` - Days to keep backups (default: 30)

**Backup Location:**

Backups are stored in: `backups/database/backup_<db_name>_<timestamp>.sql.gz`

**Scheduling Backups (Cron):**

Add to crontab for automated backups:

```bash
# Daily backup at 2 AM / Backup diário às 2h
0 2 * * * cd /path/to/django_base && ./scripts/backup_database.sh >> /var/log/db_backup.log 2>&1

# Weekly backup every Sunday at 3 AM / Backup semanal todo domingo às 3h
0 3 * * 0 cd /path/to/django_base && ./scripts/backup_database.sh >> /var/log/db_backup.log 2>&1
```

---

#### 2. `restore_database.sh` - Database Restore

Restores a PostgreSQL database from a backup file with safety checks.

**Features:**

- ✅ Interactive backup selection
- ✅ Multiple confirmation prompts to prevent accidents
- ✅ Automatic pre-restore backup creation
- ✅ Backup integrity verification before restore
- ✅ Supports Docker and local PostgreSQL
- ✅ Detailed progress logging

**Usage:**

```bash
# Interactive mode - select from available backups
./scripts/restore_database.sh

# Restore specific backup file
./scripts/restore_database.sh backup_django_db_20250112_143022.sql.gz

# Restore with full path
./scripts/restore_database.sh /path/to/backup.sql.gz

# Via Docker Compose
docker-compose exec web bash -c "./scripts/restore_database.sh"
```

**Safety Features:**

1. **Double Confirmation:** Requires typing "yes" and then "RESTORE" to proceed
2. **Pre-Restore Backup:** Automatically creates a backup before restore
3. **Integrity Check:** Verifies backup file is not corrupted
4. **Clear Warnings:** Shows what will be replaced

**⚠️ Warning:**

Database restore will **REPLACE ALL DATA** in the target database. Always ensure
you have a recent backup before proceeding.

---

### Best Practices

#### Backup Strategy

**3-2-1 Backup Rule:**

- Keep at least **3** copies of your data
- Store backups on **2** different media types
- Keep **1** copy offsite (cloud storage)

**Recommended Backup Schedule:**

- **Hourly:** For critical production databases
- **Daily:** For production databases
- **Weekly:** For development/staging environments

#### Backup Storage

**Local Storage:**

- Default: `backups/database/` (gitignored)
- Ensure sufficient disk space (monitor with `df -h`)

**Remote/Cloud Storage:**

Upload backups to cloud storage for disaster recovery:

```bash
# AWS S3
aws s3 cp backups/database/backup_*.sql.gz s3://your-bucket/backups/

# Google Cloud Storage
gsutil cp backups/database/backup_*.sql.gz gs://your-bucket/backups/

# Azure Blob Storage
az storage blob upload-batch -d your-container -s backups/database/
```

#### Testing Restores

Regularly test your backup restoration process:

```bash
# 1. Create a test database
docker exec -i django_base-db-1 createdb -U postgres test_restore_db

# 2. Restore to test database (modify script DB_NAME temporarily)
DB_NAME=test_restore_db ./scripts/restore_database.sh backup_file.sql.gz

# 3. Verify data integrity
docker exec -i django_base-db-1 psql -U postgres -d test_restore_db -c "SELECT COUNT(*) FROM your_table;"

# 4. Drop test database
docker exec -i django_base-db-1 dropdb -U postgres test_restore_db
```

---

### Troubleshooting

#### Error: "pg_dump: command not found"

**Solution:** Ensure PostgreSQL client tools are installed or use Docker mode.

```bash
# Ubuntu/Debian
sudo apt-get install postgresql-client

# macOS
brew install postgresql

# Or use Docker mode (automatic if container is running)
```

#### Error: "Permission denied"

**Solution:** Make scripts executable:

```bash
chmod +x scripts/backup_database.sh scripts/restore_database.sh
```

#### Error: "Docker container not found"

**Solution:** Check container name and ensure it's running:

```bash
# List running containers
docker ps

# Update DB_CONTAINER variable if needed
DB_CONTAINER=your_actual_container_name ./scripts/backup_database.sh
```

#### Backup file is too large

**Solution:** Backups are already compressed. For very large databases:

1. Increase retention cleanup frequency
2. Consider incremental backups (requires WAL archiving)
3. Use cloud storage with lifecycle policies

---

## Português (Brasil)

### Visão Geral

Este diretório contém scripts para operações de backup e restauração de banco de
dados. Estes scripts suportam instalações PostgreSQL baseadas em Docker e
locais.

### Scripts Disponíveis

#### 1. `backup_database.sh` - Backup do Banco de Dados

Cria backups comprimidos do PostgreSQL com gerenciamento automático de retenção.

**Recursos:**

- ✅ Backups comprimidos (gzip) para economizar espaço em disco
- ✅ Nomes de arquivo com timestamp para fácil identificação
- ✅ Limpeza automática de backups antigos (período de retenção configurável)
- ✅ Verificação de integridade do backup
- ✅ Suporta Docker e PostgreSQL local
- ✅ Log detalhado com saída colorida

**Uso:**

```bash
# Uso básico
./scripts/backup_database.sh

# Com período de retenção customizado (dias)
RETENTION_DAYS=7 ./scripts/backup_database.sh

# Via Docker Compose
docker-compose exec web bash -c "./scripts/backup_database.sh"
```

**Configuração:**

O script carrega automaticamente a configuração do arquivo `.env`. Variáveis
principais:

- `POSTGRES_DB` - Nome do banco de dados (padrão: django_db)
- `POSTGRES_USER` - Usuário do banco (padrão: postgres)
- `POSTGRES_PASSWORD` - Senha do banco
- `POSTGRES_HOST` - Host do banco (padrão: localhost)
- `POSTGRES_PORT` - Porta do banco (padrão: 5432)
- `DB_CONTAINER` - Nome do container Docker (padrão: django_base-db-1)
- `RETENTION_DAYS` - Dias para manter backups (padrão: 30)

**Localização dos Backups:**

Backups são armazenados em:
`backups/database/backup_<nome_db>_<timestamp>.sql.gz`

**Agendamento de Backups (Cron):**

Adicione ao crontab para backups automatizados:

```bash
# Backup diário às 2h da manhã
0 2 * * * cd /caminho/para/django_base && ./scripts/backup_database.sh >> /var/log/db_backup.log 2>&1

# Backup semanal todo domingo às 3h
0 3 * * 0 cd /caminho/para/django_base && ./scripts/backup_database.sh >> /var/log/db_backup.log 2>&1
```

---

#### 2. `restore_database.sh` - Restauração do Banco de Dados

Restaura um banco de dados PostgreSQL de um arquivo de backup com verificações
de segurança.

**Recursos:**

- ✅ Seleção interativa de backup
- ✅ Múltiplos prompts de confirmação para prevenir acidentes
- ✅ Criação automática de backup pré-restauração
- ✅ Verificação de integridade do backup antes de restaurar
- ✅ Suporta Docker e PostgreSQL local
- ✅ Log detalhado de progresso

**Uso:**

```bash
# Modo interativo - selecione dos backups disponíveis
./scripts/restore_database.sh

# Restaurar arquivo de backup específico
./scripts/restore_database.sh backup_django_db_20250112_143022.sql.gz

# Restaurar com caminho completo
./scripts/restore_database.sh /caminho/para/backup.sql.gz

# Via Docker Compose
docker-compose exec web bash -c "./scripts/restore_database.sh"
```

**Recursos de Segurança:**

1. **Confirmação Dupla:** Requer digitar "yes" e depois "RESTORE" para
   prosseguir
2. **Backup Pré-Restauração:** Cria automaticamente um backup antes de restaurar
3. **Verificação de Integridade:** Verifica se o arquivo de backup não está
   corrompido
4. **Avisos Claros:** Mostra o que será substituído

**⚠️ Aviso:**

A restauração do banco de dados irá **SUBSTITUIR TODOS OS DADOS** no banco de
dados alvo. Sempre certifique-se de ter um backup recente antes de prosseguir.

---

### Melhores Práticas

#### Estratégia de Backup

**Regra 3-2-1 de Backup:**

- Mantenha pelo menos **3** cópias dos seus dados
- Armazene backups em **2** tipos de mídia diferentes
- Mantenha **1** cópia fora do local (armazenamento em nuvem)

**Cronograma de Backup Recomendado:**

- **A cada hora:** Para bancos de dados de produção críticos
- **Diariamente:** Para bancos de dados de produção
- **Semanalmente:** Para ambientes de desenvolvimento/staging

#### Armazenamento de Backup

**Armazenamento Local:**

- Padrão: `backups/database/` (no gitignore)
- Certifique-se de ter espaço suficiente em disco (monitore com `df -h`)

**Armazenamento Remoto/Nuvem:**

Faça upload dos backups para armazenamento em nuvem para recuperação de
desastres:

```bash
# AWS S3
aws s3 cp backups/database/backup_*.sql.gz s3://seu-bucket/backups/

# Google Cloud Storage
gsutil cp backups/database/backup_*.sql.gz gs://seu-bucket/backups/

# Azure Blob Storage
az storage blob upload-batch -d seu-container -s backups/database/
```

#### Testando Restaurações

Teste regularmente seu processo de restauração de backup:

```bash
# 1. Crie um banco de dados de teste
docker exec -i django_base-db-1 createdb -U postgres test_restore_db

# 2. Restaure para o banco de teste (modifique DB_NAME temporariamente no script)
DB_NAME=test_restore_db ./scripts/restore_database.sh arquivo_backup.sql.gz

# 3. Verifique integridade dos dados
docker exec -i django_base-db-1 psql -U postgres -d test_restore_db -c "SELECT COUNT(*) FROM sua_tabela;"

# 4. Remova o banco de teste
docker exec -i django_base-db-1 dropdb -U postgres test_restore_db
```

---

### Solução de Problemas

#### Erro: "pg_dump: command not found"

**Solução:** Certifique-se de que as ferramentas cliente do PostgreSQL estão
instaladas ou use o modo Docker.

```bash
# Ubuntu/Debian
sudo apt-get install postgresql-client

# macOS
brew install postgresql

# Ou use modo Docker (automático se o container estiver rodando)
```

#### Erro: "Permission denied"

**Solução:** Torne os scripts executáveis:

```bash
chmod +x scripts/backup_database.sh scripts/restore_database.sh
```

#### Erro: "Docker container not found"

**Solução:** Verifique o nome do container e certifique-se de que está rodando:

```bash
# Listar containers em execução
docker ps

# Atualize a variável DB_CONTAINER se necessário
DB_CONTAINER=nome_real_do_container ./scripts/backup_database.sh
```

#### Arquivo de backup está muito grande

**Solução:** Os backups já estão comprimidos. Para bancos de dados muito
grandes:

1. Aumente a frequência de limpeza de retenção
2. Considere backups incrementais (requer arquivamento WAL)
3. Use armazenamento em nuvem com políticas de ciclo de vida

---

## Additional Resources / Recursos Adicionais

- [PostgreSQL Backup Documentation](https://www.postgresql.org/docs/current/backup.html)
- [Docker PostgreSQL Backup Best Practices](https://docs.docker.com/samples/postgres/)
- [AWS RDS Backup Strategies](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html)

---

**License / Licença:** MIT **Maintainer / Mantenedor:** Django Base Project Team
