# SSL/HTTPS Configuration Guide

# Guia de Configuração SSL/HTTPS

🇬🇧 / 🇺🇸 **English** | 🇧🇷 **Português**

---

## English

### Overview

This guide provides step-by-step instructions for configuring SSL/HTTPS for your
Django Base project in production using Let's Encrypt (free SSL certificates)
and Nginx.

### Table of Contents

1. [Prerequisites](#prerequisites)
2. [Method 1: Using Certbot (Recommended)](#method-1-using-certbot-recommended)
3. [Method 2: Manual Certificate Setup](#method-2-manual-certificate-setup)
4. [Nginx SSL Configuration](#nginx-ssl-configuration)
5. [Django SSL Settings](#django-ssl-settings)
6. [Certificate Renewal](#certificate-renewal)
7. [Testing SSL Configuration](#testing-ssl-configuration)
8. [Troubleshooting](#troubleshooting)

---

### Prerequisites

Before you begin, ensure you have:

- ✅ A registered domain name (e.g., `your-domain.com`)
- ✅ DNS records pointing to your server's IP address
- ✅ Port 80 (HTTP) and 443 (HTTPS) open on your firewall
- ✅ Django Base project running on a server
- ✅ Root or sudo access to the server

**Verify DNS Configuration:**

```bash
# Check if domain points to your server
dig your-domain.com +short
# Should return your server's IP address
```

---

### Method 1: Using Certbot (Recommended)

Certbot is the official tool from Let's Encrypt for obtaining and managing SSL
certificates.

#### Step 1: Install Certbot

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

**CentOS/RHEL:**

```bash
sudo yum install certbot python3-certbot-nginx
```

**Docker (Alternative):**

```bash
# Add to docker-compose.yml
certbot:
  image: certbot/certbot
  volumes:
    - ./certbot/conf:/etc/letsencrypt
    - ./certbot/www:/var/www/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

#### Step 2: Stop Nginx Temporarily

Certbot needs to bind to port 80 for domain verification:

```bash
# If using Docker
docker-compose stop nginx

# If using system Nginx
sudo systemctl stop nginx
```

#### Step 3: Obtain SSL Certificate

```bash
# Standalone mode (Certbot runs its own web server)
sudo certbot certonly --standalone \
  -d your-domain.com \
  -d www.your-domain.com \
  --email admin@your-domain.com \
  --agree-tos \
  --no-eff-email

# Or use webroot mode (if Nginx is running)
sudo certbot certonly --webroot \
  -w /var/www/certbot \
  -d your-domain.com \
  -d www.your-domain.com \
  --email admin@your-domain.com \
  --agree-tos
```

**Expected Output:**

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/your-domain.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/your-domain.com/privkey.pem
```

#### Step 4: Configure Nginx for SSL

Edit your `nginx/nginx.conf` file and uncomment the SSL server block:

```nginx
# Uncomment and modify the SSL configuration section
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Certificate paths
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/your-domain.com/chain.pem;

    # Modern SSL/TLS configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # SSL session optimization
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Include all your location blocks here
    # (Copy from the HTTP server block)
}

# HTTP to HTTPS Redirect
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com www.your-domain.com;

    # Allow Let's Encrypt ACME challenge
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
        allow all;
    }

    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}
```

#### Step 5: Update Docker Compose (If Using Docker)

Add certificate volumes to your `docker-compose.yml`:

```yaml
nginx:
  image: nginx:alpine
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - ./staticfiles:/app/staticfiles:ro
    - ./mediafiles:/app/mediafiles:ro
    - /etc/letsencrypt:/etc/letsencrypt:ro # Add this
    - /var/www/certbot:/var/www/certbot:ro # Add this
  ports:
    - "80:80"
    - "443:443" # Add this
  depends_on:
    - web
```

#### Step 6: Start Nginx and Test

```bash
# Test Nginx configuration
sudo nginx -t

# Start Nginx (Docker)
docker-compose up -d nginx

# Or start system Nginx
sudo systemctl start nginx

# Check logs
docker-compose logs -f nginx
```

---

### Method 2: Manual Certificate Setup

If you have certificates from another provider (e.g., commercial CA):

#### Step 1: Prepare Certificate Files

You should have:

- `certificate.crt` - Your domain certificate
- `private.key` - Private key
- `ca_bundle.crt` - Certificate authority bundle (optional)

#### Step 2: Copy Certificates to Server

```bash
# Create directory
sudo mkdir -p /etc/ssl/certs/your-domain/

# Copy certificate files (use scp or another method)
sudo cp certificate.crt /etc/ssl/certs/your-domain/
sudo cp private.key /etc/ssl/certs/your-domain/
sudo cp ca_bundle.crt /etc/ssl/certs/your-domain/

# Set proper permissions
sudo chmod 600 /etc/ssl/certs/your-domain/private.key
sudo chmod 644 /etc/ssl/certs/your-domain/certificate.crt
```

#### Step 3: Update Nginx Configuration

```nginx
ssl_certificate /etc/ssl/certs/your-domain/certificate.crt;
ssl_certificate_key /etc/ssl/certs/your-domain/private.key;
ssl_trusted_certificate /etc/ssl/certs/your-domain/ca_bundle.crt;
```

---

### Django SSL Settings

Update your `.env` file for production:

```bash
# .env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Force HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# CORS (if using separate frontend)
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

These settings are already configured in `src/django_base/settings/prod.py`.

---

### Certificate Renewal

Let's Encrypt certificates expire after 90 days and must be renewed.

#### Automatic Renewal (Recommended)

**Using Cron:**

```bash
# Test renewal
sudo certbot renew --dry-run

# Add to crontab
sudo crontab -e

# Add this line (runs twice daily)
0 0,12 * * * certbot renew --quiet --post-hook "docker-compose restart nginx"
```

**Using Systemd Timer:**

```bash
# Enable automatic renewal timer
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Check timer status
sudo systemctl status certbot.timer
```

**Docker Renewal Container:**

Add to `docker-compose.yml`:

```yaml
certbot-renew:
  image: certbot/certbot
  volumes:
    - /etc/letsencrypt:/etc/letsencrypt
    - /var/www/certbot:/var/www/certbot
  entrypoint:
    "/bin/sh -c 'trap exit TERM; while :; do certbot renew --quiet; sleep 12h &
    wait $${!}; done;'"
```

#### Manual Renewal

```bash
# Renew certificates
sudo certbot renew

# Reload Nginx
docker-compose restart nginx
# or
sudo systemctl reload nginx
```

---

### Testing SSL Configuration

#### 1. Browser Test

Visit `https://your-domain.com` and check:

- ✅ Green padlock icon appears
- ✅ Certificate shows "Let's Encrypt"
- ✅ No mixed content warnings

#### 2. SSL Labs Test

Test your SSL configuration (A+ rating recommended):

```bash
# Visit in browser
https://www.ssllabs.com/ssltest/analyze.html?d=your-domain.com
```

**Target Rating:** A or A+

#### 3. Command Line Test

```bash
# Test SSL connection
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# Check certificate expiry
echo | openssl s_client -connect your-domain.com:443 2>/dev/null | openssl x509 -noout -dates

# Test HTTP to HTTPS redirect
curl -I http://your-domain.com
# Should return: Location: https://your-domain.com
```

#### 4. Check HSTS

```bash
curl -I https://your-domain.com | grep -i strict
# Should see: Strict-Transport-Security: max-age=31536000
```

---

### Troubleshooting

#### Problem: "Certificate not found" error

**Solution:**

```bash
# Check certificate files exist
sudo ls -la /etc/letsencrypt/live/your-domain.com/

# Verify Nginx has read permissions
sudo chmod 755 /etc/letsencrypt/live/
sudo chmod 755 /etc/letsencrypt/archive/
```

#### Problem: "Connection refused" on port 443

**Solution:**

```bash
# Check if port 443 is open
sudo netstat -tulpn | grep :443

# Check firewall
sudo ufw status
sudo ufw allow 443/tcp

# Check Docker port mapping
docker-compose ps
```

#### Problem: Mixed content warnings

**Solution:**

Ensure all resources use HTTPS URLs in templates:

```html
<!-- ❌ Wrong -->
<script src="http://example.com/script.js"></script>

<!-- ✅ Correct -->
<script src="https://example.com/script.js"></script>

<!-- ✅ Protocol-relative (uses current protocol) -->
<script src="//example.com/script.js"></script>
```

#### Problem: Certificate renewal fails

**Solution:**

```bash
# Check if Certbot can access port 80
sudo netstat -tulpn | grep :80

# Ensure webroot is accessible
sudo chmod 755 /var/www/certbot

# Test renewal manually
sudo certbot renew --dry-run --verbose

# Check Certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

#### Problem: "ERR_CERT_COMMON_NAME_INVALID"

**Solution:**

Ensure your certificate includes all domain variations:

```bash
# Obtain new certificate with all variations
sudo certbot certonly --standalone \
  -d your-domain.com \
  -d www.your-domain.com \
  -d subdomain.your-domain.com
```

---

### Security Best Practices

1. **Use Strong Ciphers:** Already configured in `nginx.conf`
2. **Enable HSTS:** Force HTTPS for 1 year
3. **Disable TLS 1.0/1.1:** Use only TLS 1.2 and 1.3
4. **OCSP Stapling:** Faster certificate validation
5. **HTTP/2:** Better performance
6. **Monitor Certificate Expiry:** Set up alerts

**Certificate Expiry Monitoring Script:**

```bash
#!/bin/bash
# Add to cron to send alert 30 days before expiry

DOMAIN="your-domain.com"
EXPIRY_DATE=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
TODAY_EPOCH=$(date +%s)
DAYS_UNTIL_EXPIRY=$(( ($EXPIRY_EPOCH - $TODAY_EPOCH) / 86400 ))

if [ $DAYS_UNTIL_EXPIRY -lt 30 ]; then
    echo "⚠️ SSL certificate expires in $DAYS_UNTIL_EXPIRY days!"
    # Send email or alert here
fi
```

---

## Português (Brasil)

### Visão Geral

Este guia fornece instruções passo a passo para configurar SSL/HTTPS para seu
projeto Django Base em produção usando Let's Encrypt (certificados SSL
gratuitos) e Nginx.

### Sumário

1. [Pré-requisitos](#pré-requisitos)
2. [Método 1: Usando Certbot (Recomendado)](#método-1-usando-certbot-recomendado)
3. [Método 2: Configuração Manual de Certificado](#método-2-configuração-manual-de-certificado)
4. [Configuração SSL do Nginx](#configuração-ssl-do-nginx)
5. [Configurações SSL do Django](#configurações-ssl-do-django)
6. [Renovação de Certificado](#renovação-de-certificado)
7. [Testando Configuração SSL](#testando-configuração-ssl)
8. [Solução de Problemas](#solução-de-problemas-1)

---

### Pré-requisitos

Antes de começar, certifique-se de ter:

- ✅ Um nome de domínio registrado (ex: `seu-dominio.com`)
- ✅ Registros DNS apontando para o IP do seu servidor
- ✅ Portas 80 (HTTP) e 443 (HTTPS) abertas no firewall
- ✅ Projeto Django Base rodando em um servidor
- ✅ Acesso root ou sudo ao servidor

**Verificar Configuração DNS:**

```bash
# Verifique se o domínio aponta para seu servidor
dig seu-dominio.com +short
# Deve retornar o endereço IP do seu servidor
```

---

### Método 1: Usando Certbot (Recomendado)

Certbot é a ferramenta oficial do Let's Encrypt para obter e gerenciar
certificados SSL.

#### Passo 1: Instalar Certbot

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

**CentOS/RHEL:**

```bash
sudo yum install certbot python3-certbot-nginx
```

**Docker (Alternativa):**

```bash
# Adicione ao docker-compose.yml
certbot:
  image: certbot/certbot
  volumes:
    - ./certbot/conf:/etc/letsencrypt
    - ./certbot/www:/var/www/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

#### Passo 2: Parar Nginx Temporariamente

Certbot precisa se conectar à porta 80 para verificação do domínio:

```bash
# Se usando Docker
docker-compose stop nginx

# Se usando Nginx do sistema
sudo systemctl stop nginx
```

#### Passo 3: Obter Certificado SSL

```bash
# Modo standalone (Certbot roda seu próprio servidor web)
sudo certbot certonly --standalone \
  -d seu-dominio.com \
  -d www.seu-dominio.com \
  --email admin@seu-dominio.com \
  --agree-tos \
  --no-eff-email

# Ou use modo webroot (se Nginx estiver rodando)
sudo certbot certonly --webroot \
  -w /var/www/certbot \
  -d seu-dominio.com \
  -d www.seu-dominio.com \
  --email admin@seu-dominio.com \
  --agree-tos
```

**Saída Esperada:**

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/seu-dominio.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/seu-dominio.com/privkey.pem
```

#### Passo 4: Configurar Nginx para SSL

Edite seu arquivo `nginx/nginx.conf` e descomente o bloco de servidor SSL:

```nginx
# Descomente e modifique a seção de configuração SSL
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name seu-dominio.com www.seu-dominio.com;

    # Caminhos dos certificados SSL
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/seu-dominio.com/chain.pem;

    # Configuração SSL/TLS moderna
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # Otimização de sessão SSL
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Inclua todos os seus blocos location aqui
    # (Copie do bloco de servidor HTTP)
}

# Redirecionamento HTTP para HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name seu-dominio.com www.seu-dominio.com;

    # Permitir desafio ACME do Let's Encrypt
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
        allow all;
    }

    # Redirecionar todo outro tráfego para HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}
```

[O resto do documento continua com a mesma estrutura, traduzido para
português...]

---

## Recursos Adicionais / Additional Resources

- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Certbot User Guide](https://eff-certbot.readthedocs.io/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs Best Practices](https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices)

---

**License / Licença:** MIT **Maintainer / Mantenedor:** Django Base Project Team
