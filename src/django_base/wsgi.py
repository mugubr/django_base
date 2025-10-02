"""
WSGI config for django_base project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/

---
Configuração WSGI para o projeto django_base.
Ele expõe o 'callable' WSGI como
uma variável de nível de módulo chamada ``application``.
O Gunicorn usa este arquivo para servir a aplicação.
Para mais informações sobre este arquivo, veja a documentação do Django.
"""

import os

from django.core.wsgi import get_wsgi_application

# Points to the settings file for the application
# Aponta para o arquivo de configurações da aplicação
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_base.settings")

# get_wsgi_application() returns the WSGI callable
# get_wsgi_application() retorna o 'callable' WSGI
application = get_wsgi_application()
