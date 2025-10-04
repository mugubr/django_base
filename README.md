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
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Ruff-D7B092?style=for-the-badge&logo=ruff&logoColor=black" alt="Ruff">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
</div>

-   **Web Server:** Nginx
-   **Application Server:** Gunicorn
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
-   **Development Tools:** `django-extensions` with `watchdog` for hot-reloading.

### 🏁 Running the Project (Docker)

#### 💻 Development Mode (`dev` profile)

This mode is for active development. It uses Django's development server with hot-reloading and provides detailed logs.

1.  **First-Time Setup:**
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

2.  **To Start the Development Server:**
    *This command will attach to your terminal and show live logs. Press `Ctrl + C` to stop.*
    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up
    ```

#### 🚀 Production Mode (`prod` profile)

This mode runs the production-like stack with Nginx and Gunicorn.

1.  **To Start the Production Stack:**
    ```bash
    docker-compose --profile prod up -d --build
    ```

2.  **Required Commands (after starting):**
    ```bash
    # Run migrations
    docker-compose --profile prod exec web python manage.py migrate
    # Collect static files for Nginx
    docker-compose --profile prod exec web python manage.py collectstatic --no-input
    ```

The application will be available at `http://localhost:8000` with hot-reload enabled.

After these steps, your environment will be running
-   **Application:** `http://localhost:8000`
-   **Example API Endpoint:** `http://localhost:8000/api/v1/hello/`
-   **Django Admin:** `http://localhost:8000/admin`
-   **Prometheus:** `http://localhost:9090`
-   **Grafana:** `http://localhost:3000` (login: `admin`/`admin`)

---

### 💻 Local Development (Without Docker)

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
        # or Windows (Command Prompt)
        .venv\Scripts\activate.bat
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
        # or Windows (Command Prompt)
        .venv\Scripts\activate.bat
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
    # For a production dependency
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

1.  Ensure your **development** environment is running.
2.  Execute the `startapp` command:
    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py startapp my_new_app
    ```
3.  Move the new `my_new_app` folder from the project root into the `src/` directory.
4.  Add `'my_new_app'` to `INSTALLED_APPS` in `src/django_base/settings.py`.
5.  Create and configure the app's `urls.py`.

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
    docker-compose exec web python -m coverage run manage.py test src
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
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Ruff-D7B092?style=for-the-badge&logo=ruff&logoColor=black" alt="Ruff">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
</div>

-   **Servidor Web:** Nginx
-   **Servidor de Aplicação:** Gunicorn
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
-   **Ferramentas de Desenvolvimento:** `django-extensions` com `watchdog` para hot-reloading.

### 🏁 Executando o Projeto (Docker)

#### 💻 Modo de Desenvolvimento (perfil `dev`)

Este modo é para o desenvolvimento ativo. Ele usa o servidor de desenvolvimento do Django com hot-reloading e logs detalhados.

1.  **Setup da Primeira Vez:**
    ```bash
    # Clone o repositório e entre na pasta
    git clone <url-do-seu-repositorio> && cd django_base
    
    # Crie o arquivo de ambiente
    cp .env.example .env
    
    # Construa as imagens
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev build
    
    # Rode as migrações (usando 'run' para um container temporário)
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py migrate
    
    # Crie um superusuário
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py createsuperuser
    ```

2.  **Para Iniciar o Servidor de Desenvolvimento:**
    *Este comando vai "prender" seu terminal e mostrar os logs ao vivo. Pressione `Ctrl + C` para parar.*
    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up
    ```

#### 🚀 Modo de Produção (perfil `prod`)

Este modo executa a stack de produção com Nginx e Gunicorn.

1.  **Para Iniciar a Stack de Produção:**
    ```bash
    docker-compose --profile prod up -d --build
    ```

2.  **Comandos Necessários (após iniciar):**
    ```bash
    # Rodar migrações
    docker-compose --profile prod exec web python manage.py migrate
    # Coletar arquivos estáticos para o Nginx
    docker-compose --profile prod exec web python manage.py collectstatic --no-input
    ```

Após esses passos, seu ambiente estará no ar!
-   **Aplicação:** `http://localhost:8000`
-   **Endpoint de API de Exemplo:** `http://localhost:8000/api/v1/hello/`
-   **Admin do Django:** `http://localhost:8000/admin`
-   **Prometheus:** `http://localhost:9090`
-   **Grafana:** `http://localhost:3000` (login: `admin`/`admin`)
---

### 💻 Desenvolvimento Local (Sem Docker)

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
        # ou no Windows (Command Prompt)
        .venv\Scripts\activate.bat
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
        # ou no Windows (Command Prompt)
        .venv\Scripts\activate.bat
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

    # Para uma dependência de desenvolvimento
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

1.  **Garanta que seu ambiente de desenvolvimento esteja rodando.**
2.  Execute o comando `startapp`:
    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py startapp meu_novo_app
    ```
3.  Mova a nova pasta `meu_novo_app` da raiz do projeto para dentro do diretório `src/`.
4.  Adicione `'meu_novo_app'` à lista `INSTALLED_APPS` no arquivo `src/django_base/settings.py`.
5.  Crie e configure o arquivo `urls.py` da sua nova app, e inclua-o no `urls.py` principal.
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
    docker-compose exec web python -m coverage run manage.py test src
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