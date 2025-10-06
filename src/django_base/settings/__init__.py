# Settings Package Initialization
# Inicialização do Pacote Settings

# This file automatically imports the correct settings module based on
# the DJANGO_SETTINGS_MODULE environment variable.
#
# Este arquivo importa automaticamente o módulo de settings correto baseado
# na variável de ambiente DJANGO_SETTINGS_MODULE.
#
# Usage / Uso:
# - Development: DJANGO_SETTINGS_MODULE=django_base.settings.dev
# - Production: DJANGO_SETTINGS_MODULE=django_base.settings.prod
# - Default: DJANGO_SETTINGS_MODULE=django_base.settings (uses base)

import os

# Detect which settings module to use
# Detecta qual módulo de settings usar
settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "django_base.settings.base")

# Import the appropriate settings
# Importa as settings apropriadas
if "dev" in settings_module or "development" in settings_module:
    from .dev import *  # noqa: F403
elif "prod" in settings_module or "production" in settings_module:
    from .prod import *  # noqa: F403
else:
    # Default to base settings
    # Padrão para settings base
    from .base import *  # noqa: F403
