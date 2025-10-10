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
