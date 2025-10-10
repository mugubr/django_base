"""
ASGI Configuration for Django Base Project
Configuracao ASGI para o Projeto Django Base

This module configures ASGI (Asynchronous Server Gateway Interface) for the Django application.
ASGI is the spiritual successor to WSGI, designed to provide a standard interface between
async-capable Python web servers, frameworks, and applications.

Este modulo configura o ASGI (Asynchronous Server Gateway Interface) para a aplicacao Django.
ASGI e o sucessor espiritual do WSGI, projetado para fornecer uma interface padrao entre
servidores web Python capazes de async, frameworks e aplicacoes.

Key Components / Componentes Principais:
-----------------------------------------
- Exposes the ASGI callable as a module-level variable named 'application'
- Supports both synchronous and asynchronous request handling
- Enables WebSocket, HTTP/2, and long-polling connections
- Used by ASGI servers like Daphne, Uvicorn, or Hypercorn

- Expoe o callable ASGI como uma variavel de nivel de modulo chamada 'application'
- Suporta manipulacao de requisicoes sincronas e assincronas
- Habilita conexoes WebSocket, HTTP/2 e long-polling
- Usado por servidores ASGI como Daphne, Uvicorn ou Hypercorn

Usage / Uso:
------------
Production deployment with Uvicorn:
Implantacao em producao com Uvicorn:
    uvicorn django_base.asgi:application --host 0.0.0.0 --port 8000

Production deployment with Daphne:
Implantacao em producao com Daphne:
    daphne -b 0.0.0.0 -p 8000 django_base.asgi:application

For more information / Para mais informacoes:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set default Django settings module
# Define o modulo de configuracoes padrao do Django
# This environment variable tells Django which settings file to use
# Esta variavel de ambiente diz ao Django qual arquivo de configuracoes usar
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_base.settings")

# Create and expose the ASGI application callable
# Cria e expoe o callable da aplicacao ASGI
# This is the entry point for ASGI servers to interface with Django
# Este e o ponto de entrada para servidores ASGI interfacearem com Django
# Supports async views, middleware, and WebSocket connections
# Suporta views async, middleware e conexoes WebSocket
application = get_asgi_application()
