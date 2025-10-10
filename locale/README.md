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
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up

# Compile translations / Compile traduções
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec web python manage.py compilemessages

# Or update and compile / Ou atualize e compile
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec web python manage.py makemessages -l pt_BR -l en --ignore=.venv
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev exec web python manage.py compilemessages
```

## Changing Language / Mudando Idioma

Edit `.env` file and set: Edite o arquivo `.env` e defina:

```env
LANGUAGE_CODE=pt-br  # or 'en' for English / ou 'en' para inglês
```

## Adding New Translations / Adicionando Novas Traduções

1. **Mark strings for translation in code:** **Marque strings para tradução no
   código:**

   **In Python code (models, forms, views):**

   ```python
   from django.utils.translation import gettext_lazy as _

   # In models, forms, views
   message = _("Welcome back, {username}!")
   ```

   **In templates:**

   ```django
   {% load i18n %}

   {# Simple translation #}
   <h1>{% trans "Welcome" %}</h1>

   {# Translation with variables #}
   {% blocktrans with name=user.username %}Hello {{ name }}!{% endblocktrans %}

   {# JavaScript translations #}
   <script>
   const msg = "{% trans 'Click here' %}";
   </script>
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

✅ **Forms** - Login, Register, Profile, UserUpdate ✅ **Models** - UserProfile,
Category, Tag, Product ✅ **Views** - Welcome messages, errors, success
notifications ✅ **Admin** - User Info, Contact, Location, Status labels ✅
**Templates** - All HTML templates with proper i18n tags:

- `home.html` - Hero section, features cards, dashboard
- `login.html` - Authentication form
- `register.html` - User registration + Terms modal
- `profile.html` - User profile editor
- `products.html` - Product catalog with filters
- `about.html` - Project information
- `health_check.html` - System health monitoring (including JS)
- `base.html` - Navigation, footer, Terms modal
- Components: pagination, cards

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
    ('pt-br', 'Português (Brasil)'),  # Primary language
    ('en', 'English'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',  # After SessionMiddleware
    ...
]
```

## Troubleshooting / Solução de Problemas

**Traduções não aparecem:**

1. Verifique se compilou:
   `docker-compose exec web python manage.py compilemessages`
2. Confirme o `LANGUAGE_CODE` no `.env`
3. Reinicie o container: `docker-compose restart web`
4. Limpe o cache: `docker-compose exec web python manage.py clear_cache` (se
   aplicável)

**Strings em inglês mesmo com pt-br:**

- Verifique se a string tem `{% trans %}` ou `_()` no código
- Confirme que a tradução existe no arquivo `.po`
- Certifique-se que o arquivo `.mo` foi compilado
