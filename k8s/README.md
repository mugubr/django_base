# Kubernetes Deployment - Django Base Project

Este diretório contém todos os manifestos Kubernetes para deploy da aplicação
Django Base em ambientes de desenvolvimento e produção.

## ⚡ Comandos Rápidos

```bash
# Setup completo (desenvolvimento)
./setup-k8s.sh              # ou: make setup-k8s

# Setup completo (produção)
./setup-k8s.sh --prod       # ou: make setup-k8s-prod

# Acessar aplicação
kubectl port-forward -n django-base svc/dev-nginx-service 8000:80

# Ver status
kubectl get all -n django-base

# Ver logs
kubectl logs -n django-base -l app=django,component=web --tail=50 -f

# Criar superuser
kubectl exec -it -n django-base deployment/dev-django-web -- /app/.venv/bin/python manage.py createsuperuser

# Limpar tudo
kubectl delete namespace django-base
```

## 📁 Estrutura de Diretórios

```
k8s/
├── base/                    # Manifestos base (comum para dev e prod)
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── pvc.yaml
│   ├── postgres-deployment.yaml
│   ├── redis-deployment.yaml
│   ├── django-deployment.yaml
│   ├── nginx-deployment.yaml
│   ├── prometheus-deployment.yaml
│   ├── grafana-deployment.yaml
│   ├── ingress.yaml
│   └── kustomization.yaml
├── dev/                     # Overlays para desenvolvimento
│   └── kustomization.yaml
├── prod/                    # Overlays para produção
│   └── kustomization.yaml
└── README.md
```

## 🚀 Quick Start

### Pré-requisitos

1. **Kubernetes Cluster** (v1.25+)
   - **Docker Desktop** (recomendado para Windows/Mac) - Habilitar Kubernetes
     nas configurações
   - **Minikube** (desenvolvimento local Linux/Mac/Windows)
   - **GKE, EKS, AKS** (produção)
   - **K3s, MicroK8s** (edge/IoT)

2. **kubectl** instalado e configurado
   - Windows: `choco install kubernetes-cli` ou
     `winget install Kubernetes.kubectl`
   - Linux: `sudo apt-get install kubectl`
   - Mac: `brew install kubectl`

3. **Docker** instalado e rodando

4. **Ingress Controller** (opcional, mas recomendado)

### Configurar Kubernetes Local

**Docker Desktop (Recomendado para Windows):**

1. Abra Docker Desktop
2. Settings → Kubernetes → Enable Kubernetes
3. Apply & Restart
4. Aguarde o cluster iniciar (ícone verde)

**Minikube:**

```bash
# Instalar Minikube
choco install minikube  # Windows
# ou
brew install minikube   # Mac
# ou
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64  # Linux

# Iniciar cluster
minikube start

# Habilitar Ingress (opcional)
minikube addons enable ingress
```

## 📦 Deploy - Desenvolvimento

### Método 1: Setup Automatizado (Recomendado)

```bash
# Opção 1: Usando o script diretamente
./setup-k8s.sh

# Opção 2: Usando Make
make setup-k8s

# O script automaticamente:
# ✓ Verifica se kubectl está instalado
# ✓ Verifica conexão com o cluster
# ✓ Constrói a imagem Docker localmente (django-base:dev-latest)
# ✓ Cria o namespace django-base
# ✓ Aplica todos os manifestos do Kubernetes
# ✓ Aguarda os deployments ficarem prontos
# ✓ Mostra instruções de como acessar
```

### Método 2: Passo a Passo Manual

### 1. Build da Imagem Docker Localmente

```bash
# Build da imagem local (não precisa de registry!)
docker build -t django-base:dev-latest .

# Verificar se a imagem foi criada
docker images | grep django-base
```

**IMPORTANTE:** Para desenvolvimento local, usamos a imagem
`django-base:dev-latest` construída localmente. Não é necessário fazer push para
um registry!

### 2. (Opcional) Atualizar Secrets

Valores padrão de desenvolvimento já estão configurados em
`k8s/base/secrets.yaml`.

Para produção, atualize com valores seguros:

```bash
# Gerar SECRET_KEY segura
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Deploy no Cluster

```bash
# Criar namespace
kubectl create namespace django-base

# Aplicar manifests
kubectl apply -k k8s/dev/

# Verificar status
kubectl get all -n django-base
```

### 4. Verificar Deploy

```bash
# Ver todos os recursos
kubectl get all -n django-base

# Ver status dos pods (aguarde todos ficarem Running)
kubectl get pods -n django-base -w

# Ver logs do Django
kubectl logs -n django-base -l app=django,component=web --tail=100 -f
```

### 5. Acessar a Aplicação

**Docker Desktop Kubernetes:**

```bash
# Port forward para acessar localmente
kubectl port-forward -n django-base svc/dev-nginx-service 8000:80

# Acessar: http://localhost:8000
```

**Minikube:**

```bash
# Opção 1: Usar serviço do Minikube (abre automaticamente)
minikube service dev-nginx-service -n django-base

# Opção 2: Port forward
kubectl port-forward -n django-base svc/dev-nginx-service 8000:80

# Acessar: http://localhost:8000
```

### 6. Criar Superuser

```bash
# Entrar no pod Django
kubectl exec -it -n django-base deployment/dev-django-web -- /bin/sh

# Dentro do pod, criar superuser
/app/.venv/bin/python manage.py createsuperuser

# Sair
exit
```

## 🏭 Deploy - Produção

### Método 1: Setup Automatizado

```bash
# Usando o script
./setup-k8s.sh --prod

# Ou usando Make
make setup-k8s-prod

# O script automaticamente:
# ✓ Constrói a imagem com tag de produção (v1.2.0)
# ✓ Cria/atualiza namespace
# ✓ Aplica manifests de produção
# ✓ Aguarda deployments (com mais réplicas)
```

### Método 2: Preparação Manual

**CRÍTICO:** Antes de fazer deploy em produção:

1. ✅ Substitua todas as senhas em `k8s/base/secrets.yaml`
2. ✅ Configure o domínio em `k8s/base/ingress.yaml`
3. ✅ Atualize `ALLOWED_HOSTS` em `k8s/prod/kustomization.yaml`
4. ✅ Configure SSL/TLS (cert-manager recomendado)
5. ✅ Revise limites de recursos em todos os deployments
6. ✅ Configure backups automáticos dos PVCs

### 1. Build e Tag da Imagem

**Para produção local (sem registry):**

```bash
# Build com tag de versão
docker build -t django-base:v1.2.0 .
docker tag django-base:v1.2.0 django-base:latest
```

**Para produção com registry:**

```bash
# Build com tag de versão
docker build -t your-registry/django-base:v1.2.0 .
docker tag your-registry/django-base:v1.2.0 your-registry/django-base:latest

# Push para registry
docker push your-registry/django-base:v1.2.0
docker push your-registry/django-base:latest
```

### 2. Deploy

```bash
# Deploy em produção
kubectl apply -k k8s/prod/

# Verificar rollout
kubectl rollout status deployment/prod-django-web -n django-base
```

## 🔧 Operações Comuns

### Scaling

```bash
# Escalar Django web
kubectl scale deployment/django-web --replicas=5 -n django-base

# Escalar Nginx
kubectl scale deployment/nginx --replicas=3 -n django-base
```

### Atualizações (Rolling Update)

```bash
# Atualizar imagem
kubectl set image deployment/django-web django=your-registry/django-base:v1.3.0 -n django-base

# Verificar rollout
kubectl rollout status deployment/django-web -n django-base

# Rollback se necessário
kubectl rollout undo deployment/django-web -n django-base
```

### Migrations

```bash
# Executar migrations manualmente
kubectl exec -it -n django-base deployment/django-web -- /app/.venv/bin/python manage.py migrate

# Criar superuser
kubectl exec -it -n django-base deployment/django-web -- /app/.venv/bin/python manage.py createsuperuser
```

### Logs e Debug

```bash
# Ver logs do Django
kubectl logs -n django-base -l app=django,component=web --tail=100 -f

# Ver logs de um pod específico
kubectl logs -n django-base <pod-name> -f

# Entrar em um pod
kubectl exec -it -n django-base <pod-name> -- /bin/sh

# Ver eventos
kubectl get events -n django-base --sort-by='.lastTimestamp'
```

## 📊 Monitoramento

### Acessar Grafana

```bash
# Port forward
kubectl port-forward -n django-base svc/grafana-service 3000:3000

# Acessar: http://localhost:3000
# User: admin
# Password: (definido em secrets.yaml)
```

### Acessar Prometheus

```bash
kubectl port-forward -n django-base svc/prometheus-service 9090:9090

# Acessar: http://localhost:9090
```

## 🔒 Segurança

### Secrets Management

**Produção:**

- Use **Sealed Secrets** ou **External Secrets Operator**
- Integre com **AWS Secrets Manager**, **Azure Key Vault**, ou **Google Secret
  Manager**
- Nunca commite secrets em Git!

## 🧹 Limpeza

```bash
# Deletar tudo do ambiente dev
kubectl delete -k k8s/dev/

# Deletar namespace (remove tudo)
kubectl delete namespace django-base

# Deletar PVCs (dados persistentes)
kubectl delete pvc --all -n django-base
```

## 🎯 Best Practices

1. **Use Kustomize overlays** para diferentes ambientes
2. **Implemente Resource Requests/Limits** em todos os containers
3. **Configure Health Checks** (liveness/readiness probes)
4. **Use ImagePullPolicy: IfNotPresent** em prod
5. **Configure monitoring e alerting** desde o início
6. **Teste rollbacks** antes de ir para produção
7. **Automatize com CI/CD** (GitHub Actions, GitLab CI, ArgoCD)

## 🔍 Troubleshooting

### Problema: "kubectl: command not found"

```bash
# Instalar kubectl
# Windows (Chocolatey)
choco install kubernetes-cli

# Windows (winget)
winget install Kubernetes.kubectl

# Mac
brew install kubectl

# Linux
sudo apt-get install kubectl
```

### Problema: "The connection to the server localhost:8080 was refused"

**Causa:** Kubernetes cluster não está rodando ou kubectl não está configurado.

**Solução:**

```bash
# Docker Desktop: Habilite Kubernetes em Settings → Kubernetes → Enable Kubernetes

# Minikube: Inicie o cluster
minikube start

# Verifique a conexão
kubectl cluster-info
```

### Problema: Pods ficam em "ImagePullBackOff"

**Causa:** Kubernetes não consegue baixar a imagem.

**Solução para imagens locais:**

```bash
# Para Docker Desktop: A imagem já está disponível localmente
docker images | grep django-base

# Se não estiver, build novamente
docker build -t django-base:dev-latest .

# Para Minikube: Precisa usar o daemon do Minikube
eval $(minikube docker-env)
docker build -t django-base:dev-latest .

# Ou carregar imagem no Minikube
minikube image load django-base:dev-latest
```

### Problema: Pods em "CrashLoopBackOff"

**Causa:** Container está iniciando e falhando repetidamente.

**Solução:**

```bash
# Ver logs do pod
kubectl logs -n django-base <pod-name>

# Ver eventos
kubectl get events -n django-base --sort-by='.lastTimestamp'

# Descrever pod para ver detalhes
kubectl describe pod -n django-base <pod-name>

# Verificar se migrations rodaram
kubectl logs -n django-base <pod-name> -c migrations
```

### Problema: "Error from server (NotFound): namespaces "django-base" not found"

**Solução:**

```bash
# Criar namespace
kubectl create namespace django-base

# Ou aplicar o manifest do namespace
kubectl apply -f k8s/base/namespace.yaml
```

### Problema: PostgreSQL não inicia (Pending)

**Causa:** PersistentVolume não está disponível.

**Solução:**

```bash
# Verificar PVCs
kubectl get pvc -n django-base

# Para desenvolvimento local, usar storageClass padrão
# Docker Desktop: Já tem storageClass configurado
# Minikube: Habilitar storage
minikube addons enable storage-provisioner
minikube addons enable default-storageclass
```

### Problema: Não consigo acessar a aplicação

**Solução:**

```bash
# Verificar se os pods estão Running
kubectl get pods -n django-base

# Verificar serviços
kubectl get svc -n django-base

# Tentar port-forward direto para o Django
kubectl port-forward -n django-base deployment/dev-django-web 8000:8000

# Verificar health check
curl http://localhost:8000/health/
```

### Comandos úteis de debug

```bash
# Entrar no pod para debug
kubectl exec -it -n django-base deployment/dev-django-web -- /bin/sh

# Verificar variáveis de ambiente
kubectl exec -n django-base deployment/dev-django-web -- env

# Testar conexão com PostgreSQL dentro do pod
kubectl exec -n django-base deployment/dev-postgres -- pg_isready -U django_user

# Testar conexão com Redis
kubectl exec -n django-base deployment/dev-redis -- redis-cli ping

# Ver configuração aplicada
kubectl get deployment dev-django-web -n django-base -o yaml
```

---

**Versão:** 1.2.0 **Última atualização:** 2025-01-15
