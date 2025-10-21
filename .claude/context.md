# Claude Code - Contexto Otimizado do Projeto Django Base

## 🎯 Missão e Regras Críticas (SEMPRE SEGUIR)

**Sua Missão:** Você é meu parceiro de programação para o projeto `django_base`.
Seu objetivo é me ajudar a escrever, refatorar, testar e documentar o código,
seguindo rigorosamente os padrões e a arquitetura definidos neste documento.

### 1. MÁXIMA ECONOMIA DE TOKENS ⚡

- **Priorize `Edit` em vez de reescrever.**
- Use `Task` para buscas e revisões complexas.
- Seja direto e conciso. **Sem frases como "Claro, aqui está...", "Vou
  fazer...", ou explicações óbvias.** Respostas devem ter de 1 a 4 linhas.

### 2. DOCUMENTAÇÃO BILÍNGUE OBRIGATÓRIA (PT/EN) 🌍

- **Docstrings em todos os arquivos `.py`:** A primeira linha em inglês, a
  segunda em português. Argumentos e retornos também devem ser bilíngues.
- **Comentários inline:** `# English comment / Comentário em português`.

### 3. WORKFLOW OTIMIZADO 🚀

- **Sempre verifique o `git status` ANTES de iniciar modificações.**
- Para tarefas com 3 ou mais passos, use a ferramenta `TodoWrite`.
- **Crie testes** para novas funcionalidades ou após mudanças críticas.
- Commits devem ser descritivos e bilíngues.

---

## 🏛️ Arquitetura e Stack Tecnológica

| Categoria               | Tecnologia               | Propósito no Projeto                                                |
| ----------------------- | ------------------------ | ------------------------------------------------------------------- |
| **Backend**             | Python 3.13, Django 5.2+ | Framework principal para a lógica de negócio.                       |
| **API**                 | DRF, django-filter       | Criação de endpoints RESTful, com filtros e busca.                  |
| **Banco de Dados**      | PostgreSQL 15            | Banco de dados relacional principal.                                |
| **Cache & Tarefas**     | Redis 7, Django Q2       | Cache de alta performance e processamento de tarefas em background. |
| **Servidor**            | Nginx, Gunicorn          | Servidor web (proxy reverso) e servidor de aplicação WSGI.          |
| **Containerização**     | Docker                   | Ambiente de desenvolvimento e produção padronizado.                 |
| **Monitoramento**       | Prometheus, Grafana      | Coleta e visualização de métricas da aplicação.                     |
| **Qualidade de Código** | Ruff, Pre-commit, Bandit | Linter, formatador, hooks de git e análise de segurança.            |

---

## 🧬 Princípios de Design do Projeto

- **Bilingual by Default:** Todo o código, da documentação aos templates, é
  escrito em inglês e português para ser acessível globalmente.
- **Security First:** Configurações de produção reforçadas (HSTS, secure
  cookies), rate limiting no Nginx e análise de segurança com Bandit.
- **Developer Experience (DX) Focada:** O `setup.sh` automatiza 100% do ambiente
  de desenvolvimento. Pre-commit hooks garantem a qualidade do código antes do
  commit.
- **Performance Otimizada:** Uso de cache com Redis, consultas otimizadas com
  `select_related` e `prefetch_related`, e compressão Gzip via Nginx.
- **Soft Deletion:** Dados nunca são permanentemente deletados do banco. O
  método `deactivate()` é usado para manter a integridade referencial.

---

## 📁 Arquivos Core (Referência Rápida)

- **Models (4):** `Product`, `UserProfile`, `Category` (hierárquico), `Tag`.
- **Views (7):** `home`, `login`, `register`, `logout`, `profile`, `products`,
  `health_check_page`.
- **Forms (5):** `Login`, `Register`, `UserProfile`, `UserUpdate`,
  `ProductForm`.
- **API (4 ViewSets):** `ProductViewSet`, `CategoryViewSet`, `TagViewSet`,
  `UserProfileViewSet`.
- **Serializers (10):** Serializers de lista e detalhe para cada modelo.
- **Utils:** 23 template tags, 8 validadores, 15 decoradores, 13 mixins.
- **Settings:** `base.py` (comum), `dev.py` (desenvolvimento), `prod.py`
  (produção).

---

## 🎯 Workflows Comuns (Como Fazer)

### Criar um Novo Endpoint de API (CRUD Completo)

1.  **Model:** Crie ou modifique o modelo em `src/core/models.py`. Lembre-se da
    docstring bilíngue.
2.  **Serializer:** Crie um `ModelSerializer` em `src/core/serializers.py` (um
    para lista e um para detalhes, se necessário).
3.  **ViewSet:** Crie um `ModelViewSet` em `src/core/viewsets.py`. Adicione
    filtros, busca e ordenação.
4.  **URL:** Registre o novo ViewSet no router em `src/core/urls.py`.
5.  **Testes:** Crie testes para o novo endpoint em `src/core/tests.py`,
    cobrindo todos os métodos (GET, POST, PUT, DELETE).

### Adicionar uma Nova Página com Template

1.  **View:** Crie a função de view em `src/core/views.py`. Use decoradores para
    permissões, se necessário.
2.  **URL:** Adicione o path da nova view em `src/core/urls.py`.
3.  **Template:** Crie o arquivo HTML em `templates/`, estendendo
    `base/base.html`.
4.  **Tradução (i18n):** Use `{% trans "Texto" %}` ou `{% blocktrans %}` para
    todo o texto visível ao usuário.
5.  **Atualizar Traduções:** Rode
    `docker-compose exec web python manage.py makemessages -l pt_BR -l en` e
    preencha os arquivos `.po`.
6.  **Compilar Traduções:** Rode
    `docker-compose exec web python manage.py compilemessages`.

---

## ⚡ Comandos Rápidos por Tarefa

<details>
<summary><strong>🐳 Gestão do Ambiente Docker</strong></summary>

```bash
# Iniciar ambiente DEV (com logs)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up

# Parar ambiente DEV
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev down

# Acessar o shell do container web
docker-compose exec web bash
```

</details>

<details>
<summary><strong>📦 Gestão do Banco de Dados e Django</strong></summary>

```bash
# Aplicar migrações do banco de dados
docker-compose exec web python manage.py migrate

# Criar um superusuário (apenas em dev)
docker-compose exec web python manage.py create_superuser_if_none_exists

# Popular o banco com dados de teste (apenas em dev)
docker-compose exec web python manage.py seed_database
```

</details>

<details>
<summary><strong>✅ Testes e Qualidade de Código</strong></summary>

```bash
# Rodar todos os testes
docker-compose exec web python manage.py test src

# Rodar testes com relatório de cobertura
docker-compose exec web coverage run manage.py test src && docker-compose exec web coverage report

# Formatar o código com Ruff
docker-compose exec web ruff format .

# Verificar linting com Ruff (com auto-correção)
docker-compose exec web ruff check --fix .
```

</details>

---

## 🔑 Informações Críticas

- **Credenciais de Desenvolvimento:**
  - **Superuser:** `admin` / `admin` (auto-criado pelo `setup.sh`)
  - **Grafana:** `admin` / `admin`
- **URLs Base:** `localhost:8000`
  - **API Docs:** `/api/docs/` (Swagger), `/api/redoc/` (ReDoc)
  - **Monitoramento:** `/health-status/` (Visual), `:9090` (Prometheus), `:3000`
    (Grafana)

---

## 🎨 Padrões do Projeto

- **Docstrings (SEMPRE bilíngue):**

  ```python
  """
  English first line.
  Portuguese second line.

  Args/Arguments:
      param: Description / Descrição

  Returns/Retorna:
      Type: Description / Descrição
  """
  ```

- **Formulários Bootstrap:**
  ```python
  widgets = {
      "field": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Text")})
  }
  ```
- **Templates i18n:**
  ```django
  {% load i18n %}
  {% trans "Text" %}
  {% blocktrans %}Text with {{ var }}{% endblocktrans %}
  ```

---

**Última Atualização:** 2025-10-12 | **Status:** ✅ Funcional + Otimizado +
Automatizado
