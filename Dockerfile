FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Define o PATH para o ambiente virtual
ENV PATH="/app/.venv/bin:$PATH"

# Instala o uv
RUN pip install uv

# Copia apenas o necessário para instalar as dependências
COPY ./pyproject.toml ./uv.lock* .

# Agora, copia o resto do seu código-fonte para o contêiner
COPY . .

# Cria o ambiente virtual e instala todas as dependências (normais e de dev)
RUN uv venv && uv sync --dev

# Expõe a porta para o Django
EXPOSE 8000

# Define um comando padrão (será sobrescrito pelo docker-compose.yml)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]