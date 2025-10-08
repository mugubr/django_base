"""
WSGI Configuration for Django Base Project
Configuracao WSGI para o Projeto Django Base

This module configures WSGI (Web Server Gateway Interface) for the Django application.
WSGI is a specification that describes how a web server communicates with web applications.

Este modulo configura o WSGI (Web Server Gateway Interface) para a aplicacao Django.
WSGI e uma especificacao que descreve como um servidor web se comunica com aplicacoes web.

Key Components / Componentes Principais:
-----------------------------------------
- Exposes the WSGI callable as a module-level variable named 'application'
- Used by WSGI servers like Gunicorn, uWSGI, or mod_wsgi to serve the application
- Handles synchronous HTTP requests (for async, see asgi.py)

- Expoe o callable WSGI como uma variavel de nivel de modulo chamada 'application'
- Usado por servidores WSGI como Gunicorn, uWSGI, ou mod_wsgi para servir a aplicacao
- Lida com requisicoes HTTP sincronas (para async, veja asgi.py)

Usage / Uso:
------------
Production deployment with Gunicorn:
Implantacao em producao com Gunicorn:
    gunicorn django_base.wsgi:application --bind 0.0.0.0:8000

For more information / Para mais informacoes:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set default Django settings module
# Define o modulo de configuracoes padrao do Django
# This environment variable tells Django which settings file to use
# Esta variavel de ambiente diz ao Django qual arquivo de configuracoes usar
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_base.settings")

# Create and expose the WSGI application callable
# Cria e expoe o callable da aplicacao WSGI
# This is the entry point for WSGI servers to interface with Django
# Este e o ponto de entrada para servidores WSGI interfacearem com Django
application = get_wsgi_application()
