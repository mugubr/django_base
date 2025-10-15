# Pull Request

## Description / Descrição

<!-- Provide a brief description of the changes in this PR -->
<!-- Forneça uma breve descrição das mudanças neste PR -->

## Type of Change / Tipo de Mudança

<!-- Mark the relevant option with an "x" -->
<!-- Marque a opção relevante com um "x" -->

- [ ] 🐛 Bug fix / Correção de bug (non-breaking change which fixes an issue /
      mudança que não quebra compatibilidade e corrige um problema)
- [ ] ✨ New feature / Nova funcionalidade (non-breaking change which adds
      functionality / mudança que não quebra compatibilidade e adiciona
      funcionalidade)
- [ ] 💥 Breaking change / Mudança que quebra compatibilidade (fix or feature
      that would cause existing functionality to not work as expected / correção
      ou funcionalidade que causaria funcionalidade existente a não funcionar
      como esperado)
- [ ] 📚 Documentation update / Atualização de documentação (changes to
      documentation only / mudanças apenas na documentação)
- [ ] 🎨 Code refactoring / Refatoração de código (code improvements without
      changing functionality / melhorias de código sem mudar funcionalidade)
- [ ] ⚡ Performance improvement / Melhoria de performance
- [ ] 🧪 Test update / Atualização de testes
- [ ] 🔧 Chore / Tarefa (maintenance, configuration, etc. / manutenção,
      configuração, etc.)

## Related Issues / Issues Relacionadas

<!-- Link to related issues -->
<!-- Link para issues relacionadas -->

Closes # Related to #

## Changes Made / Mudanças Realizadas

<!-- List the main changes made in this PR -->
<!-- Liste as principais mudanças feitas neste PR -->

-
-
-

## Testing / Testes

<!-- Describe the tests you ran to verify your changes -->
<!-- Descreva os testes que você executou para verificar suas mudanças -->

### Test Configuration / Configuração de Teste

- Python version / Versão do Python:
- Django version / Versão do Django:
- Database / Banco de dados:
- OS / SO:

### Tests Performed / Testes Realizados

- [ ] Unit tests pass / Testes unitários passam
- [ ] Integration tests pass / Testes de integração passam
- [ ] Manual testing completed / Testes manuais completados

**Test Details / Detalhes dos Testes:**

<!-- Describe how you tested your changes -->
<!-- Descreva como você testou suas mudanças -->

```bash
# Commands used for testing / Comandos usados para testes

```

## Screenshots / Capturas de Tela

<!-- If applicable, add screenshots to demonstrate the changes -->
<!-- Se aplicável, adicione screenshots para demonstrar as mudanças -->

| Before / Antes | After / Depois |
| -------------- | -------------- |
|                |                |

## Checklist / Lista de Verificação

<!-- Mark completed items with an "x" -->
<!-- Marque itens completados com um "x" -->

### Code Quality / Qualidade de Código

- [ ] My code follows the project's style guidelines / Meu código segue as
      diretrizes de estilo do projeto
- [ ] I have performed a self-review of my own code / Realizei uma auto-revisão
      do meu código
- [ ] I have commented my code, particularly in hard-to-understand areas /
      Comentei meu código, particularmente em áreas difíceis de entender
- [ ] **My code has bilingual docstrings (EN/PT)** / **Meu código tem docstrings
      bilíngues (EN/PT)**
- [ ] I have run Ruff linter and formatter / Executei o linter e formatador Ruff
- [ ] Pre-commit hooks pass / Hooks de pre-commit passam

```bash
# Run these commands before submitting / Execute estes comandos antes de submeter
docker-compose exec web ruff check --fix .
docker-compose exec web ruff format .
```

### Testing / Testes

- [ ] I have added tests that prove my fix is effective or that my feature works
      / Adicionei testes que provam que minha correção é efetiva ou que minha
      funcionalidade funciona
- [ ] New and existing unit tests pass locally with my changes / Testes
      unitários novos e existentes passam localmente com minhas mudanças
- [ ] Test coverage is maintained or improved / Cobertura de testes é mantida ou
      melhorada

```bash
# Test commands / Comandos de teste
docker-compose exec web python manage.py test src
docker-compose exec web coverage run manage.py test src
docker-compose exec web coverage report
```

### Documentation / Documentação

- [ ] I have made corresponding changes to the documentation / Fiz mudanças
      correspondentes na documentação
- [ ] I have updated the CHANGELOG.md / Atualizei o CHANGELOG.md
- [ ] I have added/updated docstrings (bilingual EN/PT) / Adicionei/atualizei
      docstrings (bilíngue EN/PT)
- [ ] I have updated the README if necessary / Atualizei o README se necessário

### Database / Banco de Dados

- [ ] I have created and tested database migrations (if applicable) / Criei e
      testei migrações de banco de dados (se aplicável)
- [ ] Migration files are included / Arquivos de migração estão incluídos
- [ ] Migrations are reversible / Migrações são reversíveis

### Security / Segurança

- [ ] My changes don't introduce security vulnerabilities / Minhas mudanças não
      introduzem vulnerabilidades de segurança
- [ ] I have run security checks (Bandit) / Executei verificações de segurança
      (Bandit)
- [ ] No sensitive data is exposed / Nenhum dado sensível é exposto

```bash
# Security check / Verificação de segurança
docker-compose exec web bandit -r src/
```

### Dependencies / Dependências

- [ ] I have updated `pyproject.toml` if I added new dependencies / Atualizei
      `pyproject.toml` se adicionei novas dependências
- [ ] I have documented why new dependencies are needed / Documentei por que
      novas dependências são necessárias

## Breaking Changes / Mudanças que Quebram Compatibilidade

<!-- If this PR introduces breaking changes, describe them here -->
<!-- Se este PR introduz mudanças que quebram compatibilidade, descreva-as aqui -->

- [ ] This PR contains breaking changes / Este PR contém mudanças que quebram
      compatibilidade

**Breaking Changes Details / Detalhes das Mudanças:**

## Migration Guide / Guia de Migração

<!-- If applicable, provide a migration guide for users -->
<!-- Se aplicável, forneça um guia de migração para usuários -->

## Additional Notes / Notas Adicionais

<!-- Any additional information that reviewers should know -->
<!-- Qualquer informação adicional que revisores devem saber -->

## Reviewer Notes / Notas para Revisores

<!-- Specific areas you'd like reviewers to focus on -->
<!-- Áreas específicas que você gostaria que revisores focassem -->

---

## For Maintainers / Para Mantenedores

<!-- To be filled by maintainers -->
<!-- A ser preenchido por mantenedores -->

- [ ] Code review completed / Revisão de código completada
- [ ] All CI checks pass / Todas verificações de CI passam
- [ ] Documentation is adequate / Documentação é adequada
- [ ] Tests are comprehensive / Testes são abrangentes
- [ ] Ready to merge / Pronto para merge

**Merge Strategy / Estratégia de Merge:**

- [ ] Squash and merge / Squash e merge
- [ ] Rebase and merge / Rebase e merge
- [ ] Create a merge commit / Criar um commit de merge
