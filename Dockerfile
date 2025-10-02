FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
# Set the working directory inside the container
WORKDIR /app

# Define a variável de ambiente PATH para incluir o diretório de binários do venv.
# Isso garante que os comandos instalados no venv (como 'ruff', 'django-admin')
# sejam encontrados pelo terminal
# Set the PATH environment variable to include the venv's binary directory.
# This ensures that commands installed in the venv (like 'ruff', 'django-admin')
# are found by the shell
ENV PATH="/app/.venv/bin:$PATH"

# Instala o 'uv'
# Install 'uv'
RUN pip install uv

# Copia os arquivos que definem as dependências primeiro.
# Isso aproveita o cache do Docker: se esses arquivos não mudarem,
# o Docker não reinstalará as dependências em builds futuros.
# Copy the dependency definition files first
# This leverages Docker's cache: if these files don't change,
# Docker won't reinstall dependencies on future builds
COPY ./pyproject.toml ./uv.lock* .

# Copia todo o código-fonte do projeto para o diretório de trabalho
# Copy all the project's source code into the working directory
COPY . .

# Cria o ambiente virtual e instala TODAS as dependências (produção e dev)
# Create the virtual environment and install ALL dependencies (production and dev)
RUN uv venv && uv sync --dev

# Expõe a porta 8000 do contêiner para que possamos nos conectar a ela
# a partir da nossa máquina ou de outros contêineres
# Expose port 8000 of the container so we can connect to it
# from our host machine or other containers
EXPOSE 8000

# Define um comando padrão para executar quando o contêiner iniciar.
# Este comando será sobrescrito pelo `command` no docker-compose.yml.
# Defines a default command to run when the container starts.
# This command will be overridden by the `command` in docker-compose.yml.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]