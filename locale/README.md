# Internationalization (i18n) / Internacionalização

This directory contains translation files for the Django Base project. Este
diretório contém arquivos de tradução para o projeto Django Base.

## Supported Languages / Idiomas Suportados

- **English (en)** - Default fallback / Fallback padrão
- **Português Brasil (pt-br)** - Default language / Idioma padrão

## Files / Arquivos

- `en/LC_MESSAGES/django.po` - English translations / Traduções em inglês
- `pt_BR/LC_MESSAGES/django.po` - Brazilian Portuguese translations / Traduções
  em português brasileiro

## Compiling Translations / Compilando Traduções

**Important:** Run inside Docker container to avoid module path issues.
**Importante:** Execute dentro do container Docker para evitar problemas de
caminho de módulo.

```bash
# Start containers / Inicie os containers
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Compile translations / Compile traduções
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py compilemessages

# Or update and compile / Ou atualize e compile
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py makemessages -l pt_BR -l en --ignore=.venv
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py compilemessages
```

## Changing Language / Mudando Idioma

Edit `.env` file and set: Edite o arquivo `.env` e defina:

```env
LANGUAGE_CODE=pt-br  # or 'en' for English / ou 'en' para inglês
```

## Adding New Translations / Adicionando Novas Traduções

1. **Mark strings for translation in code:** **Marque strings para tradução no
   código:**

```python
from django.utils.translation import gettext_lazy as _

# In models, forms, views
message = _("Welcome back, {username}!")
```

2. **Update translation files:** **Atualize arquivos de tradução:**

```bash
docker-compose exec web python manage.py makemessages -l pt_BR
```

3. **Edit `.po` files and add translations** **Edite arquivos `.po` e adicione
   traduções**

4. **Compile translations:** **Compile traduções:**

```bash
docker-compose exec web python manage.py compilemessages
```

5. **Restart server to apply changes** **Reinicie o servidor para aplicar
   mudanças**

## Current Coverage / Cobertura Atual

✅ Forms (Login, Register, Profile, UserUpdate) ✅ Models (UserProfile,
Category, Tag, Product) ✅ Views messages (welcome, errors, success) ✅ Admin
labels (User Info, Contact, Location, Status) ✅ Common UI (Home, Login,
Register, Profile, Admin)

## Notes / Notas

- `.po` files are human-editable text / arquivos `.po` são texto editável por
  humanos
- `.mo` files are compiled binaries (gitignored) / arquivos `.mo` são binários
  compilados (no gitignore)
- Always run `compilemessages` after editing `.po` files / Sempre execute
  `compilemessages` após editar arquivos `.po`
- Translations are loaded on server start / Traduções são carregadas ao iniciar
  servidor

## Django Settings / Configurações Django

The following settings are configured in `settings/base.py`: As seguintes
configurações estão em `settings/base.py`:

```python
USE_I18N = True
LANGUAGE_CODE = 'pt-br'  # Default from .env
LANGUAGES = [
    ('en', 'English'),
    ('pt-br', 'Português (Brasil)'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',  # After SessionMiddleware
    ...
]
```
