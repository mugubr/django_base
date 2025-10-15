# Contributing to Django Base / Contribuindo para Django Base

First off, thank you for considering contributing to Django Base! 🎉
Primeiramente, obrigado por considerar contribuir para o Django Base! 🎉

Following these guidelines helps to communicate that you respect the time of the
developers managing and developing this open source project. Seguir estas
diretrizes ajuda a comunicar que você respeita o tempo dos desenvolvedores
gerenciando e desenvolvendo este projeto de código aberto.

---

## Table of Contents / Índice

- [Code of Conduct / Código de Conduta](#code-of-conduct--código-de-conduta)
- [How Can I Contribute? / Como Posso Contribuir?](#how-can-i-contribute--como-posso-contribuir)
- [Development Setup / Configuração de Desenvolvimento](#development-setup--configuração-de-desenvolvimento)
- [Coding Standards / Padrões de Código](#coding-standards--padrões-de-código)
- [Commit Messages / Mensagens de Commit](#commit-messages--mensagens-de-commit)
- [Pull Request Process / Processo de Pull Request](#pull-request-process--processo-de-pull-request)
- [Testing / Testes](#testing--testes)

---

## Code of Conduct / Código de Conduta

This project and everyone participating in it is governed by respect, empathy,
and professionalism. By participating, you are expected to uphold this code.
Este projeto e todos que participam dele são governados por respeito, empatia e
profissionalismo. Ao participar, espera-se que você mantenha este código.

**Be respectful / Seja respeitoso:**

- Use welcoming and inclusive language / Use linguagem acolhedora e inclusiva
- Be respectful of differing viewpoints / Seja respeitoso com pontos de vista
  diferentes
- Accept constructive criticism gracefully / Aceite críticas construtivas com
  elegância
- Focus on what is best for the community / Foque no que é melhor para a
  comunidade

---

## How Can I Contribute? / Como Posso Contribuir?

### Reporting Bugs / Reportando Bugs

Before creating bug reports, please check existing issues to avoid duplicates.
Antes de criar relatórios de bugs, verifique issues existentes para evitar
duplicatas.

**When creating a bug report, include:** **Ao criar um relatório de bug,
inclua:**

- Use a clear and descriptive title / Use um título claro e descritivo
- Describe the exact steps to reproduce the problem / Descreva os passos exatos
  para reproduzir o problema
- Provide specific examples / Forneça exemplos específicos
- Describe the behavior you observed and what you expected / Descreva o
  comportamento observado e o esperado
- Include screenshots if relevant / Inclua screenshots se relevante
- Include your environment details (OS, Python version, Django version) / Inclua
  detalhes do ambiente

### Suggesting Enhancements / Sugerindo Melhorias

Enhancement suggestions are tracked as GitHub issues. When creating an
enhancement suggestion: Sugestões de melhorias são rastreadas como issues do
GitHub. Ao criar uma sugestão:

- Use a clear and descriptive title / Use um título claro e descritivo
- Provide a step-by-step description of the suggested enhancement / Forneça
  descrição passo a passo da melhoria sugerida
- Provide specific examples / Forneça exemplos específicos
- Explain why this enhancement would be useful / Explique por que esta melhoria
  seria útil
- List any alternatives you've considered / Liste alternativas que você
  considerou

### Your First Code Contribution / Sua Primeira Contribuição de Código

Unsure where to begin? Look for issues labeled: Não sabe por onde começar?
Procure por issues com labels:

- `good first issue` - Good for newcomers / Bom para iniciantes
- `help wanted` - Extra attention needed / Atenção extra necessária
- `bug` - Something isn't working / Algo não está funcionando
- `enhancement` - New feature or request / Nova funcionalidade ou requisição

---

## Development Setup / Configuração de Desenvolvimento

### 1. Fork and Clone / Fork e Clone

```bash
# Fork the repository on GitHub first
# Faça fork do repositório no GitHub primeiro

git clone https://github.com/YOUR-USERNAME/django-base.git
cd django-base
```

### 2. Run Setup Script / Execute Script de Setup

```bash
# On Linux/Mac
bash setup.sh

# On Windows (use Git Bash or WSL)
bash setup.sh
```

This script will: Este script irá:

- Check Docker installation / Verificar instalação do Docker
- Create `.env` file from template / Criar arquivo `.env` do template
- Build Docker containers / Construir containers Docker
- Run migrations / Executar migrações
- Create superuser / Criar superusuário
- Seed database with test data / Popular banco com dados de teste

### 3. Create a Branch / Crie uma Branch

```bash
git checkout -b feature/your-feature-name
# or / ou
git checkout -b fix/your-bug-fix-name
```

---

## Coding Standards / Padrões de Código

### 1. Bilingual Documentation / Documentação Bilíngue

**All code must have bilingual documentation (English/Portuguese).** **Todo
código deve ter documentação bilíngue (Inglês/Português).**

```python
def example_function(param1: str) -> str:
    """
    Short description in English.
    Descrição curta em português.

    Args / Argumentos:
        param1 (str): Description in English / Descrição em português

    Returns / Retorna:
        str: Return description in English / Descrição do retorno em português
    """
    pass
```

### 2. Code Formatting / Formatação de Código

We use **Ruff** for linting and formatting: Usamos **Ruff** para linting e
formatação:

```bash
# Format code / Formatar código
docker-compose exec web ruff format .

# Check linting / Verificar linting
docker-compose exec web ruff check --fix .
```

**Key rules / Regras principais:**

- Line length: 88 characters / Comprimento de linha: 88 caracteres
- Use type hints / Use type hints
- Follow Django naming conventions / Siga convenções de nomenclatura Django
- No unused imports / Sem imports não utilizados

### 3. Pre-commit Hooks / Hooks de Pre-commit

Pre-commit hooks run automatically before each commit: Hooks de pre-commit
executam automaticamente antes de cada commit:

```bash
# Install pre-commit hooks / Instalar hooks de pre-commit
pre-commit install

# Run manually / Executar manualmente
pre-commit run --all-files
```

### 4. Import Order / Ordem de Imports

```python
# Standard library / Biblioteca padrão
import os
from datetime import datetime

# Third-party packages / Pacotes de terceiros
from django.contrib import admin
from rest_framework import serializers

# Local imports / Imports locais
from .models import Product
from .utils import helper_function
```

---

## Commit Messages / Mensagens de Commit

### Format / Formato

```
type(scope): Short description in English

Descrição curta em português

- Additional details if needed
- Detalhes adicionais se necessário
```

### Types / Tipos

- `feat`: New feature / Nova funcionalidade
- `fix`: Bug fix / Correção de bug
- `docs`: Documentation changes / Mudanças na documentação
- `style`: Code style changes (formatting) / Mudanças de estilo de código
- `refactor`: Code refactoring / Refatoração de código
- `test`: Adding or updating tests / Adicionando ou atualizando testes
- `chore`: Maintenance tasks / Tarefas de manutenção
- `perf`: Performance improvements / Melhorias de performance

### Examples / Exemplos

```
feat(api): Add JWT authentication endpoint

Adiciona endpoint de autenticação JWT

- Implements token generation
- Adds token refresh mechanism
- Implementa geração de token
- Adiciona mecanismo de refresh de token
```

```
fix(auth): Resolve login redirect issue

Resolve problema de redirecionamento no login

Fixes #123
```

---

## Pull Request Process / Processo de Pull Request

### Before Submitting / Antes de Submeter

1. **Update documentation / Atualize documentação**
   - Update docstrings / Atualize docstrings
   - Update README if needed / Atualize README se necessário
   - Update CHANGELOG.md / Atualize CHANGELOG.md

2. **Run tests / Execute testes**

   ```bash
   docker-compose exec web python manage.py test src
   ```

3. **Check coverage / Verifique cobertura**

   ```bash
   docker-compose exec web coverage run manage.py test src
   docker-compose exec web coverage report
   ```

4. **Run linting / Execute linting**

   ```bash
   docker-compose exec web ruff check --fix .
   docker-compose exec web ruff format .
   ```

5. **Security check / Verificação de segurança**
   ```bash
   docker-compose exec web bandit -r src/
   ```

### Pull Request Template / Template de Pull Request

Your pull request should include: Seu pull request deve incluir:

- **Description / Descrição**: What changes did you make and why?
- **Type / Tipo**: Feature, Bug Fix, Documentation, etc.
- **Related Issues / Issues Relacionadas**: Link to related issues
- **Testing / Testes**: How did you test your changes?
- **Screenshots / Capturas de Tela**: If UI changes
- **Checklist / Lista de Verificação**:
  - [ ] Tests pass / Testes passam
  - [ ] Documentation updated / Documentação atualizada
  - [ ] Code formatted with Ruff / Código formatado com Ruff
  - [ ] Bilingual docstrings / Docstrings bilíngues
  - [ ] CHANGELOG.md updated / CHANGELOG.md atualizado

### Review Process / Processo de Revisão

1. At least one maintainer approval required / Pelo menos uma aprovação de
   mantenedor necessária
2. All CI checks must pass / Todas verificações de CI devem passar
3. Resolve all review comments / Resolva todos comentários de revisão
4. Keep commits clean and organized / Mantenha commits limpos e organizados
5. Rebase if requested / Faça rebase se solicitado

---

## Testing / Testes

### Running Tests / Executando Testes

```bash
# All tests / Todos os testes
docker-compose exec web python manage.py test src

# Specific app / App específica
docker-compose exec web python manage.py test src.core

# With coverage / Com cobertura
docker-compose exec web coverage run manage.py test src
docker-compose exec web coverage report
docker-compose exec web coverage html  # Generate HTML report
```

### Writing Tests / Escrevendo Testes

```python
from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    """
    Test suite for Product model.
    Suite de testes para model Product.
    """

    def setUp(self):
        """
        Set up test data.
        Configura dados de teste.
        """
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00
        )

    def test_product_creation(self):
        """
        Test product is created correctly.
        Testa se produto é criado corretamente.
        """
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 100.00)
```

**Test coverage requirements / Requisitos de cobertura de testes:**

- Aim for 80%+ coverage / Almeje 80%+ de cobertura
- All new features must have tests / Todas novas funcionalidades devem ter
  testes
- Bug fixes should include regression tests / Correções de bugs devem incluir
  testes de regressão

---

## Questions? / Dúvidas?

If you have questions, please: Se você tiver dúvidas, por favor:

- Check existing documentation / Verifique documentação existente
- Search existing issues / Busque em issues existentes
- Create a new issue with the `question` label / Crie uma nova issue com label
  `question`
- Contact the maintainers / Contate os mantenedores

---

## Recognition / Reconhecimento

Contributors will be recognized in: Contribuidores serão reconhecidos em:

- Project README / README do projeto
- humans.txt file / arquivo humans.txt
- Release notes / Notas de lançamento

---

## License / Licença

By contributing, you agree that your contributions will be licensed under the
MIT License. Ao contribuir, você concorda que suas contribuições serão
licenciadas sob a Licença MIT.

---

**Thank you for contributing to Django Base! 🚀** **Obrigado por contribuir para
o Django Base! 🚀**
