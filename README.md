# Meu Projeto Django

Um projeto Django dockerizado com uv, PostgreSQL, Django Q, Ruff, pre-commit e testes automatizados

## Pré-requisitos

-   Docker
-   Docker Compose

## Como Iniciar o Ambiente de Desenvolvimento

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd meu_projeto_django
    ```

2.  **Crie seu arquivo de ambiente:**
    Copie o arquivo de exemplo e, se necessário, ajuste as variáveis.
    ```bash
    cp .env.example .env
    ```

3.  **Construa e inicie os contêineres:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Execute as migrações do banco de dados:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Crie um superusuário:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

O ambiente estará disponível em `http://localhost:8000`.

## Comandos Úteis

-   **Parar os contêineres:**
    ```bash
    docker-compose down
    ```

-   **Acessar o shell do contêiner web:**
    ```bash
    docker-compose exec web bash
    ```

-   **Ver os logs dos contêineres:**
    ```bash
    docker-compose logs -f
    ```

### Testes

Para rodar a suíte de testes e ver o relatório de cobertura, execute os seguintes comandos:

1.  **Rodar os testes com coverage:**
    ```bash
    docker-compose exec web coverage run manage.py test
    ```

2.  **Ver o relatório no terminal:**
    ```bash
    docker-compose exec web coverage report -m
    ```

### Qualidade de Código

Este projeto usa `ruff` para linting e formatação e `pre-commit` para garantir a qualidade do código antes de cada commit. Os hooks são instalados automaticamente, basta ter o `pre-commit` instalado localmente se desejar.