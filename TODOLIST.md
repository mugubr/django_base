# 📋 TODO List - Django Base Project / Lista de Tarefas

## 🚀 Features / Funcionalidades

### API & Backend

- [ ] **Social Login (OAuth2)** - Implement social login with Google, GitHub,
      etc. / Implementar login social com Google, GitHub, etc.
- [ ] **GraphQL Support** - Add a GraphQL endpoint using Graphene or Strawberry.
      / Adicionar um endpoint GraphQL usando Graphene ou Strawberry.
- [x] **API Rate Limiting** - 🔥 Critical - Enhance rate limiting for API
      endpoints. (Completed) / 🔥 Crítico - Melhorar a limitação de taxa para
      endpoints da API. (Concluído)
- [ ] **Bulk Endpoints** - Add endpoints for bulk create/update/delete
      operations. / Adicionar endpoints para operações em massa de
      criar/atualizar/deletar.

### Frontend / Interface

- [x] **HTMX Integration** - ✅ Quick Win - Add more dynamic content with HTMX.
      (Completed) / ✅ Vitória Rápida - Adicionar mais conteúdo dinâmico com
      HTMX. (Concluído)
- [ ] **Dark Mode** - Implement a dark mode toggle for the UI. / Implementar um
      seletor de modo escuro para a UI.
- [ ] **PWA Support** - Add Progressive Web App (PWA) support. / Adicionar
      suporte para Progressive Web App (PWA).
- [ ] **Toast Notifications** - Implement toast notifications for user feedback.
      / Implementar notificações "toast" para feedback do usuário.
- [ ] **Tailwind CSS** - Migrate from Bootstrap to Tailwind CSS. / Migrar de
      Bootstrap para Tailwind CSS.

## ✅ Testing & Code Quality / Testes & Qualidade de Código

- [x] **Integration Tests** - 🔥 Critical - Add integration tests for API
      workflows. (Completed) / 🔥 Crítico - Adicionar testes de integração para
      fluxos de trabalho da API. (Concluído)
- [ ] **Unit Tests** - Increase test coverage for serializers and forms. /
      Aumentar a cobertura de testes para serializers e formulários.
- [x] **Factory Boy** - Implement Factory Boy for test data generation.
      (Completed) / Implementar Factory Boy para geração de dados de teste.
      (Concluído)
- [x] **Type Hints** - ✅ COMPLETED - Add comprehensive type hints to all Python
      files (models, views, serializers, forms, etc.). / ✅ CONCLUÍDO -
      Adicionar type hints abrangentes a todos os arquivos Python.
- [x] **Mypy Integration** - ✅ COMPLETED - Added mypy for static type checking
      with configuration and pre-commit hooks. / ✅ CONCLUÍDO - Adicionado mypy
      para checagem estática de tipos com configuração e hooks pre-commit.
- [ ] **Docstring Coverage** - 📚 Low - Ensure 100% bilingual docstring
      coverage. / 📚 Baixo - Garantir 100% de cobertura de docstrings bilíngues.
- [ ] **Code Complexity** - Add complexity checks (radon, mccabe). / Adicionar
      checagens de complexidade (radon, mccabe).
- [ ] **Load Testing** - Add load testing with Locust or similar. / Adicionar
      testes de carga com Locust ou similar.

## 📊 Monitoring & Observability / Monitoramento & Observabilidade

- [ ] **Logging** - Implement structured logging (e.g., python-json-logger). /
      Implementar logging estruturado (ex: python-json-logger).
- [ ] **Log Aggregation** - Add ELK Stack or Loki for log aggregation. /
      Adicionar ELK Stack ou Loki para agregação de logs.
- [x] **Error Tracking** - 🔥 Critical - Complete Sentry integration with custom
      context. (Completed) / 🔥 Crítico - Completar a integração com Sentry com
      contexto customizado. (Concluído)
- [ ] **Performance Monitoring** - Add APM (Sentry/New Relic). / Adicionar APM
      (Sentry/New Relic).
- [ ] **Custom Metrics** - Add custom business metrics for Prometheus. /
      Adicionar métricas de negócio customizadas para o Prometheus.
- [x] **Grafana Dashboards** - Create pre-configured Grafana dashboards. / Criar
      dashboards pré-configurados no Grafana.
- [ ] **Prometheus Alerts** - Configure Prometheus alerts for key metrics. /
      Configurar alertas do Prometheus para métricas chave.

## ⚡ Performance / Desempenho

- [x] **Query Optimization** - 🔥 Critical - Add `django-debug-toolbar` and
      optimize queries. (Completed) / 🔥 Crítico - Adicionar
      `django-debug-toolbar` e otimizar queries. (Concluído)
- [ ] **Database Indexes** - Review and optimize database indexes. / Revisar e
      otimizar índices do banco de dados.
- [ ] **Caching** - Implement per-view, template fragment, and query result
      caching. / Implementar cache por view, de fragmento de template e de
      resultado de query.
- [ ] **CDN Integration** - Add CDN for static files (e.g., CloudFront). /
      Adicionar integração com CDN para arquivos estáticos (ex: CloudFront).

## 🔧 Maintenance & Deployment / Manutenção & Deploy

- [ ] **CI** - Run tests, linting, and coverage on each PR. / Executar testes,
      linting e cobertura em cada PR.
- [ ] **Dependencies** - Audit and upgrade dependencies. / Auditar e atualizar
      dependências.
- [x] **Kubernetes/Helm** - Add Kubernetes manifests or Helm charts. / Adicionar
      manifestos Kubernetes ou Helm charts.
- [ ] **Blue-Green Deployment** - Implement a blue-green deployment strategy. /
      Implementar uma estratégia de deploy blue-green.
- [ ] **Service Layer** - Refactor business logic into a service layer. /
      Refatorar lógica de negócio para uma camada de serviço.

---

**Priority Legend / Legenda de Prioridade:**

- 🔥 **Critical** - Security, production stability / Segurança, estabilidade em
  produção.
- 📊 **Medium** - Nice to have, improvements / Bom ter, melhorias.
- 📚 **Low** - Documentation, polish / Documentação, polimento.

**Estimated Effort / Esforço Estimado:**

- ✅ **Quick Win:** 1-2 hours / Vitória Rápida: 1-2 horas
- 🚀 **Feature:** 4-16 hours / Funcionalidade: 4-16 horas
- 🏗️ **Epic:** 16+ hours / Épico: 16+ horas
