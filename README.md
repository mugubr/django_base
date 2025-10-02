# Django Base (django_base) 🚀

🇬🇧 / 🇺🇸
## English

This is a modern base project for Django development, fully configured to run in a robust and professional Docker environment. The structure is designed to be efficient, scalable, and easy to maintain, utilizing the best practices and tools in the ecosystem.

### 🛠️ Tech Stack

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django-rest-framework&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Ruff-D7B092?style=for-the-badge&logo=ruff&logoColor=black" alt="Ruff">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
</div>

-   **Backend:** Django, Django REST Framework
-   **Database:** PostgreSQL
-   **Package Manager:** `uv`
-   **Background Tasks:** Django Q2 (`django-q2`)
-   **API Communication:** CORS (`django-cors-headers`)
-   **Containerization:** Docker & Docker Compose
-   **Code Quality:** `Ruff` & `pre-commit`
-   **Testing:** `django.test` with `coverage`
-   **Observability:** `Prometheus` & `Grafana`
-   **Environment Variables:** `python-decouple`
-   **Development Server:** `django-extensions` with `watchdog` for hot-reloading.

### 🏁 Getting Started (Docker)

#### Prerequisites

-   Docker
-   Docker Compose

#### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd django_base
    ```

2.  **Create the Environment File:**
    Copy the example file. The default values are suitable for development.
    ```bash
    cp .env.example .env
    ```

3.  **Build Images and Start Containers:**
    ```bash
    docker-compose build
    docker-compose up -d
    ```

4.  **Run Database Migrations:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a Superuser:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

After these steps, your environment will be up and running!
-   **Example API Endpoint:** `http://localhost:8000/api/v1/hello/`
-   **Django Admin:** `http://localhost:8000/admin`
-   **Prometheus:** `http://localhost:9090`
-   **Grafana:** `http://localhost:3000` (default login: `admin`/`admin`)

---

### 💻 Local Development (Without Docker)

For running the project directly on your machine.

#### Prerequisites

-   Python 3.11+
-   A local PostgreSQL server running.
-   `uv`, `pip`, or `poetry` installed.

#### Steps

1.  **Clone the repository and `cd` into it.**

2.  **Set up the environment file (`.env`):**
    Copy `.env.example` to `.env`. **Crucially, you must change `HOST=db` to `HOST=localhost`** so Django connects to your local PostgreSQL instance, not a Docker container.
    ```bash
    cp .env.example .env
    # Now edit .env and change HOST=db to HOST=localhost
    ```

3.  **Install dependencies (choose one method):**

    * **Using `uv` (Recommended):**
        ```bash
        # Create a virtual environment
        uv venv
        # Activate it (macOS/Linux)
        source .venv/bin/activate
        # Activate it (Windows PowerShell)
        .venv\Scripts\Activate.ps1
        # Install all dependencies
        uv sync --dev
        ```

    * **Using `pip`:**
        ```bash
        # Create a virtual environment
        python -m venv .venv
        # Activate it (macOS/Linux)
        source .venv/bin/activate
        # Activate it (Windows PowerShell)
        .venv\Scripts\Activate.ps1
        # Install all dependencies from requirements.txt
        pip install -r requirements.txt
        ```

    * **Using `Poetry`:**
        ```bash
        # Install all dependencies (Poetry manages the venv automatically)
        poetry install
        # To activate the shell
        poetry shell
        ```

4.  **Run Migrations and the Server:**
    *(Ensure your virtual environment is activated if using `uv` or `pip`)*
    ```bash
    # Run migrations
    python manage.py migrate
    # Run the development server
    python manage.py runserver_plus
    ```

---

### 📖 Development Workflow

#### How to Add a New Library

The `pyproject.toml` file is the source of truth for dependencies. Use the CLI commands of your package manager to add new libraries, as this will update the file automatically.

**With Docker:**

1.  **Run the install command inside the `web` container:**
    ```bash
    # For a PRODUCTION dependency
    docker-compose exec web uv add "some-package"

    # For a development dependency (like a testing tool)
    docker-compose exec web uv add "some-dev-package" --dev
    ```
2.  **To make the change permanent in the image**, rebuild it after updating `pyproject.toml`:
    ```bash
    docker-compose build
    ```

**Locally (without Docker):**

*(Ensure your virtual environment is activated)*

* **Using `uv`:**
    ```bash
    # For a production dependency
    uv add "some-package"

    # For a development dependency
    uv add "some-dev-package" --dev
    ```
* **Using `Poetry`:**
    ```bash
    # For a production dependency
    poetry add "some-package"

    # For a development dependency
    poetry add "some-dev-package" --group dev
    ```
* **After Adding:** If your team uses `requirements.txt`, remember to regenerate it:
    ```bash
    uv pip freeze > requirements.txt
    ```

#### How to Create a New App

1.  **Run the `startapp` command:**
    * **Docker:** `docker-compose exec web python manage.py startapp my_new_app`
    * **Local:** `python manage.py startapp my_new_app`
2.  Add `'my_new_app'` to the `INSTALLED_APPS` list in `django_base/settings.py`.
3.  Create a `my_new_app/urls.py` and include its routes in the main `django_base/urls.py`.

---

### 🚀 Day-to-Day Commands (Docker)

-   **Start the environment with live logs (Recommended for development):**
    *Shows colored, hot-reloading logs in your terminal. To stop, press `Ctrl + C`.*
    ```bash
    docker-compose up
    ```

-   **Start the environment in the background:**
    ```bash
    docker-compose up -d
    ```

-   **Stop all services:**
    ```bash
    docker-compose down
    ```

-   **View logs (if running in the background):**
    ```bash
    docker-compose logs -f web
    ```

-   **Access the web container's shell:**
    ```bash
    docker-compose exec web bash
    ```

### ✅ Running Tests

-   **Run tests and generate coverage data:**
    ```bash
    docker-compose exec web python -m coverage run manage.py test
    ```

-   **View the coverage report in the terminal:**
    ```bash
    docker-compose exec web python -m coverage report -m
    ```

-   **Generate an interactive HTML report (saved in the `htmlcov/` folder):**
    ```bash
    docker-compose exec web python -m coverage html
    ```

### ✨ Code Quality

#### Ruff & Pre-commit

`pre-commit` is configured to run `ruff` (formatter and linter) automatically before each commit, ensuring code consistency.

-   **Activation (optional, but recommended):**
    To enable this, install `pre-commit` on your local machine and run:
    ```bash
    pre-commit install
    ```

#### VSCode

The settings in `.vscode/settings.json` integrate `ruff` with the editor, automatically formatting your code on save.

### ⁉️ Troubleshooting

If the environment behaves unexpectedly, a corrupted Docker cache is the most likely cause. Follow these "deep clean" steps:

1.  **Stop and remove containers and networks:**
    ```bash
    docker-compose down
    ```
2.  **Prune the build cache:**
    ```bash
    docker builder prune
    ```
3.  **Rebuild the images from scratch:**
    ```bash
    docker-compose build --no-cache
    ```
4.  **Start the services again:**
    ```bash
    docker-compose up -d
    ```

---

🇧🇷
## Português (Brasil)

Este é um projeto base moderno para desenvolvimento com Django, totalmente configurado para rodar em um ambiente Docker robusto e profissional. A estrutura foi projetada para ser eficiente, escalável e fácil de manter, utilizando as melhores práticas e ferramentas do ecossistema.

### 🛠️ Tecnologias Utilizadas

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django-rest-framework&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Ruff-D7B092?style=for-the-badge&logo=ruff&logoColor=black" alt="Ruff">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
</div>

-   **Backend:** Django, Django REST Framework
-   **Banco de Dados:** PostgreSQL
-   **Gerenciador de Pacotes:** `uv`
-   **Tarefas em Background:** Django Q2 (`django-q2`)
-   **Comunicação de API:** CORS (`django-cors-headers`)
-   **Containerização:** Docker & Docker Compose
-   **Qualidade de Código:** `Ruff` e `pre-commit`
-   **Testes:** `django.test` com `coverage`
-   **Observabilidade:** `Prometheus` e `Grafana`
-   **Variáveis de Ambiente:** `python-decouple`
-   **Servidor de Desenvolvimento:** `django-extensions` com `watchdog` para hot-reloading.

### 🏁 Configuração Inicial (Docker)

#### Pré-requisitos

-   Docker
-   Docker Compose

#### Passos

1.  **Clone o Repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd django_base
    ```

2.  **Crie o Arquivo de Ambiente:**
    Copie o arquivo de exemplo. Os valores padrão já funcionam para desenvolvimento.
    ```bash
    cp .env.example .env
    ```

3.  **Construa as Imagens e Inicie os Contêineres:**
    ```bash
    docker-compose build
    docker-compose up -d
    ```

4.  **Execute as Migrações do Banco de Dados:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Crie um Superusuário:**
    Necessário para acessar o painel de administração do Django.
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

Após esses passos, seu ambiente estará no ar!
-   **Endpoint de API de Exemplo:** `http://localhost:8000/api/v1/hello/`
-   **Admin do Django:** `http://localhost:8000/admin`
-   **Prometheus:** `http://localhost:9090`
-   **Grafana:** `http://localhost:3000` (login: `admin`/`admin`)

---

### 💻 Desenvolvimento Local (Sem Docker)

Para rodar o projeto diretamente na sua máquina.

#### Pré-requisitos

-   Python 3.11+
-   Um servidor PostgreSQL rodando localmente.
-   `uv`, `pip`, ou `poetry` instalados.

#### Passos

1.  **Clone o repositório e entre na pasta.**

2.  **Configure o arquivo de ambiente (`.env`):**
    Copie o `.env.example` para `.env`. **É crucial que você altere `HOST=db` para `HOST=localhost`**, para que o Django se conecte à sua instância local do PostgreSQL, e não a um contêiner.
    ```bash
    cp .env.example .env
    # Agora, edite o arquivo .env e mude HOST=db para HOST=localhost
    ```

3.  **Instale as dependências (escolha um método):**

    * **Usando `uv` (Recomendado):**
        ```bash
        # Crie o ambiente virtual
        uv venv
        # Ative o ambiente (macOS/Linux)
        source .venv/bin/activate
        # Ative o ambiente (Windows PowerShell)
        .venv\Scripts\Activate.ps1
        # Instale todas as dependências
        uv sync --dev
        ```

    * **Usando `pip`:**
        ```bash
        # Crie o ambiente virtual
        python -m venv .venv
        # Ative o ambiente (macOS/Linux)
        source .venv/bin/activate
        # Ative o ambiente (Windows PowerShell)
        .venv\Scripts\Activate.ps1
        # Instale as dependências a partir do requirements.txt
        pip install -r requirements.txt
        ```

    * **Usando `Poetry`:**
        ```bash
        # Instala as dependências (o Poetry gerencia o ambiente virtual)
        poetry install
        # Para ativar o shell do ambiente
        poetry shell
        ```

4.  **Execute as Migrações e o Servidor:**
    *(Garanta que seu ambiente virtual esteja ativado se usar `uv` ou `pip`)*
    ```bash
    # Rode as migrações
    python manage.py migrate
    # Rode o servidor de desenvolvimento
    python manage.py runserver_plus
    ```

---

### 📖 Workflow de Desenvolvimento

#### Como Adicionar uma Nova Biblioteca

O arquivo `pyproject.toml` é a fonte da verdade para as dependências. Use os comandos CLI do seu gerenciador de pacotes para adicionar novas bibliotecas, pois isso atualizará o arquivo automaticamente.

**Com Docker:**

1.  **Execute o comando de instalação dentro do container `web`:**
    ```bash
    # Para uma dependência de produção
    docker-compose exec web uv add "nome-do-pacote"

    # Para uma dependência de desenvolvimento (ex: ferramenta de teste)
    docker-compose exec web uv add "pacote-de-dev" --dev
    ```
2.  **Para tornar a mudança permanente na imagem**, reconstrua-a após atualizar o `pyproject.toml`:
    ```bash
    docker-compose build
    ```

**Localmente (sem Docker):**

*(Garanta que seu ambiente virtual esteja ativado)*

* **Usando `uv`:**
    ```bash
    # Para uma dependência de produção
    uv add "nome-do-pacote"

    # Para uma dependência de DESENVOLVIMENTO
    uv add "nome-do-pacote" --dev
    ```
* **Usando `Poetry`:**
    ```bash
    # Para uma dependência de produção
    poetry add "nome-do-pacote"

    # Para uma dependência de desenvolvimento
    poetry add "pacote-de-dev" --group dev
    ```
* **Após Adicionar:** Se seu time utiliza `requirements.txt`, lembre-se de regerá-lo:
    ```bash
    uv pip freeze > requirements.txt
    ```

#### Como Criar uma Nova App

1.  **Execute o comando `startapp`:**
    * **Docker:** `docker-compose exec web python manage.py startapp meu_novo_app`
    * **Local:** `python manage.py startapp meu_novo_app`
2.  Adicione `'meu_novo_app'` à lista `INSTALLED_APPS` no arquivo `django_base/settings.py`.
3.  Crie um arquivo `meu_novo_app/urls.py` e inclua suas rotas no `django_base/urls.py` principal.

---

### 🚀 Comandos do Dia a Dia (Docker)

-   **Iniciar o ambiente com logs ao vivo (Recomendado para desenvolver):**
    *Mostra os logs coloridos e com hot-reload no seu terminal. Para parar, pressione `Ctrl + C`.*
    ```bash
    docker-compose up
    ```

-   **Iniciar o ambiente em segundo plano:**
    ```bash
    docker-compose up -d
    ```

-   **Parar todos os serviços:**
    ```bash
    docker-compose down
    ```

-   **Ver os logs (se estiver rodando em segundo plano):**
    ```bash
    docker-compose logs -f web
    ```

-   **Acessar o terminal (shell) do container web:**
    ```bash
    docker-compose exec web bash
    ```

### ✅ Executando Testes

-   **Rodar os testes e gerar dados de cobertura:**
    ```bash
    docker-compose exec web python -m coverage run manage.py test
    ```

-   **Ver o relatório de cobertura no terminal:**
    ```bash
    docker-compose exec web python -m coverage report -m
    ```

-   **Gerar um relatório HTML interativo (salvo na pasta `htmlcov/`):**
    ```bash
    docker-compose exec web python -m coverage html
    ```

### ✨ Qualidade de Código

#### Ruff & Pre-commit

O `pre-commit` está configurado para rodar o `ruff` (formatador e linter) automaticamente antes de cada commit, garantindo a consistência do código.

-   **Ativação (opcional, mas recomendado):**
    Para habilitar, instale `pre-commit` na sua máquina local e rode:
    ```bash
    pre-commit install
    ```

#### VSCode

As configurações em `.vscode/settings.json` integram o `ruff` ao editor, formatando seu código automaticamente ao salvar.

### ⁉️ Solução de Problemas (Troubleshooting)

Se o ambiente se comportar de forma estranha, um cache corrompido do Docker é a causa mais provável. Siga os passos de "limpeza profunda":

1.  **Pare e remova contêineres e redes:**
    ```bash
    docker-compose down
    ```
2.  **Limpe o cache de build:**
    ```bash
    docker builder prune
    ```
3.  **Reconstrua as imagens do zero:**
    ```bash
    docker-compose build --no-cache
    ```
4.  **Inicie os serviços novamente:**
    ```bash
    docker-compose up -d
    ```