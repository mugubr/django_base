# Custom Template Tags - Core Application
# Tags de Template Customizadas - Aplicação Core

"""
This module defines custom template tags and filters for Django templates.

Simple Tags (generate output):
    - get_settings_value: Access Django settings in templates
    - current_year: Returns current year for copyright notices
    - badge: Bootstrap badge component
    - icon: Bootstrap icon component
    - alert: Bootstrap alert component
    - is_active_url: Returns 'active' class for current URL
    - query_string: Updates query string parameters

Inclusion Tags (render template snippets):
    - card: Renders Bootstrap card component
    - render_pagination: Renders pagination controls

Filters (transform values):
    - currency: Format as currency (R$ 99.99)
    - percentage: Format as percentage (85.0%)
    - truncate_chars_middle: Truncate text in middle
    - file_size: Format bytes as human-readable size
    - time_ago: Relative time ("2 hours ago")
    - class_name: Get object's class name
    - get_item: Get dictionary item by key
    - multiply/divide: Math operations
    - initials: Extract initials from name
    - active_badge: Bootstrap badge for active/inactive

Este módulo define tags e filtros customizados para templates Django.

Tags Simples (geram saída):
    - get_settings_value: Acessa configurações Django em templates
    - current_year: Retorna ano atual para avisos de copyright
    - badge: Componente badge Bootstrap
    - icon: Componente ícone Bootstrap
    - alert: Componente alerta Bootstrap
    - is_active_url: Retorna classe 'active' para URL atual
    - query_string: Atualiza parâmetros de query string

Tags de Inclusão (renderizam snippets de template):
    - card: Renderiza componente card Bootstrap
    - render_pagination: Renderiza controles de paginação

Filtros (transformam valores):
    - currency: Formata como moeda (R$ 99.99)
    - percentage: Formata como porcentagem (85.0%)
    - truncate_chars_middle: Trunca texto no meio
    - file_size: Formata bytes como tamanho legível
    - time_ago: Tempo relativo ("2 horas atrás")
    - class_name: Obtém nome da classe do objeto
    - get_item: Obtém item do dicionário por chave
    - multiply/divide: Operações matemáticas
    - initials: Extrai iniciais do nome
    - active_badge: Badge Bootstrap para ativo/inativo

Usage Examples:
    {% load core_tags %}

    <!-- Simple tags -->
    {% badge "New" "success" %}
    {% icon "heart-fill" "2rem" %}
    Copyright {% current_year %}

    <!-- Filters -->
    {{ product.price|currency }}
    {{ 0.85|percentage:1 }}
    {{ created_at|time_ago }}
    {{ file.size|file_size }}

    <!-- Inclusion tags -->
    {% card "Title" "Content" "icon-name" "primary" %}
    {% render_pagination page_obj %}
"""

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()


# Simple Tags / Tags Simples


@register.simple_tag
def get_settings_value(name):
    """
    Returns a value from Django settings.
    Retorna um valor das configurações do Django.

    Usage:
        {% load core_tags %}
        {% get_settings_value 'DEBUG' %}
    """
    from django.conf import settings

    return getattr(settings, name, "")


@register.simple_tag
def current_year():
    """
    Returns the current year.
    Retorna o ano atual.

    Usage:
        {% load core_tags %}
        Copyright {% current_year %}
    """
    from datetime import datetime

    return datetime.now().year


@register.simple_tag
def badge(text, color="primary"):
    """
    Generates a Bootstrap badge with specified text and color.
    Gera um badge Bootstrap com texto e cor especificados.

    Args:
        text: Badge text
        color: Bootstrap color (primary, secondary, success, danger, etc.)

    Usage:
        {% load core_tags %}
        {% badge "New" "success" %}
    """
    return format_html(
        '<span class="badge bg-{}">{}</span>',
        color,
        text,
    )


@register.simple_tag
def icon(name, size="1em"):
    """
    Generates a Bootstrap Icon.
    Gera um ícone Bootstrap.

    Args:
        name: Icon name (without 'bi-' prefix)
        size: Icon size (default: 1em)

    Usage:
        {% load core_tags %}
        {% icon "heart-fill" "2rem" %}
    """
    return format_html(
        '<i class="bi bi-{}" style="font-size: {};"></i>',
        name,
        size,
    )


@register.simple_tag
def alert(message, alert_type="info", dismissible=True):
    """
    Generates a Bootstrap alert.
    Gera um alerta Bootstrap.

    Args:
        message: Alert message
        alert_type: Alert type (success, info, warning, danger)
        dismissible: Whether alert can be dismissed

    Usage:
        {% load core_tags %}
        {% alert "Success!" "success" True %}
    """
    dismiss_btn = ""
    if dismissible:
        dismiss_btn = (
            '<button type="button" class="btn-close" '
            'data-bs-dismiss="alert" aria-label="Close"></button>'
        )

    return format_html(
        '<div class="alert alert-{} alert-dismissible fade show" role="alert">'
        "{}{}</div>",
        alert_type,
        conditional_escape(message),
        mark_safe(dismiss_btn),  # noqa: S308
    )


# Inclusion Tags / Tags de Inclusão


@register.inclusion_tag("components/card.html")
def card(title, content, icon=None, color="primary"):
    """
    Renders a Bootstrap card component.
    Renderiza um componente card Bootstrap.

    Usage:
        {% load core_tags %}
        {% card "Card Title" "Card content here" "heart" "success" %}
    """
    return {
        "title": title,
        "content": content,
        "icon": icon,
        "color": color,
    }


@register.inclusion_tag("components/pagination.html")
def render_pagination(page_obj):
    """
    Renders pagination controls.
    Renderiza controles de paginação.

    Usage:
        {% load core_tags %}
        {% render_pagination page_obj %}
    """
    return {"page_obj": page_obj}


# Template Filters / Filtros de Template


@register.filter(name="currency")
def currency(value):
    """
    Formats a number as currency.
    Formata um número como moeda.

    Usage:
        {% load core_tags %}
        {{ product.price|currency }}
    """
    try:
        return f"R$ {float(value):,.2f}"
    except (ValueError, TypeError):
        return value


@register.filter(name="percentage")
def percentage(value, decimal_places=1):
    """
    Formats a number as percentage.
    Formata um número como porcentagem.

    Usage:
        {% load core_tags %}
        {{ 0.85|percentage:2 }}  -> 85.00%
    """
    try:
        return f"{float(value) * 100:.{decimal_places}f}%"
    except (ValueError, TypeError):
        return value


@register.filter
@stringfilter
def truncate_chars_middle(value, length=50):
    """
    Truncates text in the middle with ellipsis.
    Trunca texto no meio com reticências.

    Usage:
        {% load core_tags %}
        {{ long_text|truncate_chars_middle:30 }}
    """
    if len(value) <= length:
        return value

    # Calculate how many characters to show on each side
    # Calcula quantos caracteres mostrar de cada lado
    side_length = (length - 3) // 2

    return f"{value[:side_length]}...{value[-side_length:]}"


@register.filter
def file_size(bytes_value):
    """
    Formats bytes as human-readable file size.
    Formata bytes como tamanho de arquivo legível.

    Usage:
        {% load core_tags %}
        {{ file.size|file_size }}  -> "1.5 MB"
    """
    try:
        bytes_value = float(bytes_value)
        units = ["B", "KB", "MB", "GB", "TB"]

        for unit in units:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0

        return f"{bytes_value:.1f} PB"
    except (ValueError, TypeError):
        return bytes_value


@register.filter
def time_ago(date):
    """
    Returns human-readable time difference.
    Retorna diferença de tempo legível.

    Usage:
        {% load core_tags %}
        {{ product.created_at|time_ago }}  -> "2 hours ago"
    """

    from django.utils import timezone

    if not date:
        return ""

    now = timezone.now()
    diff = now - date

    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"


@register.filter
def class_name(obj):
    """
    Returns the class name of an object.
    Retorna o nome da classe de um objeto.

    Usage:
        {% load core_tags %}
        {{ object|class_name }}
    """
    return obj.__class__.__name__


@register.filter
def get_item(dictionary, key):
    """
    Gets an item from a dictionary by key.
    Obtém um item de um dicionário pela chave.

    Usage:
        {% load core_tags %}
        {{ my_dict|get_item:"key_name" }}
    """
    return dictionary.get(key)


@register.filter
def multiply(value, arg):
    """
    Multiplies value by argument.
    Multiplica valor por argumento.

    Usage:
        {% load core_tags %}
        {{ price|multiply:quantity }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value


@register.filter
def divide(value, arg):
    """
    Divides value by argument.
    Divide valor por argumento.

    Usage:
        {% load core_tags %}
        {{ total|divide:count }}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return value


@register.filter(is_safe=True)
def initials(name):
    """
    Returns initials from a full name.
    Retorna iniciais de um nome completo.

    Usage:
        {% load core_tags %}
        {{ user.get_full_name|initials }}  -> "JD" for "John Doe"
    """
    if not name:
        return ""

    parts = name.split()
    if len(parts) == 1:
        return parts[0][0].upper()

    return "".join([part[0].upper() for part in parts[:2]])


@register.filter
def active_badge(is_active):
    """
    Returns a Bootstrap badge for active/inactive status.
    Retorna um badge Bootstrap para status ativo/inativo.

    Usage:
        {% load core_tags %}
        {{ product.is_active|active_badge }}
    """
    if is_active:
        return mark_safe('<span class="badge bg-success">Active</span>')
    return mark_safe('<span class="badge bg-danger">Inactive</span>')


# Conditional Tags / Tags Condicionais


@register.simple_tag(takes_context=True)
def is_active_url(context, url_name):
    """
    Returns 'active' class if current URL matches the given URL name.
    Retorna classe 'active' se URL atual corresponde ao nome de URL fornecido.

    Usage:
        {% load core_tags %}
        <a class="nav-link {% is_active_url 'home' %}" href="{% url 'home' %}">Home</a>
    """
    from django.urls import resolve

    request = context.get("request")
    if request:
        current_url = resolve(request.path_info).url_name
        if current_url == url_name:
            return "active"
    return ""


@register.simple_tag
def query_string(request, **kwargs):
    """
    Updates query string with new parameters.
    Atualiza query string com novos parâmetros.

    Usage:
        {% load core_tags %}
        <a href="?{% query_string request page=2 %}">Next</a>
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            updated[key] = value
        elif key in updated:
            del updated[key]

    return updated.urlencode()
