# Custom Decorators - Core Application
# Decoradores Customizados - Aplicação Core

"""
This module defines custom decorators for views and functions.

Features:
    - Permission checking decorators (admin, verified, anonymous)
    - Caching decorators with configurable timeout
    - Logging decorators for execution time and errors
    - Rate limiting decorators to prevent API abuse
    - AJAX-specific decorators
    - Combined decorators for common patterns

Este módulo define decoradores customizados para views e funções.

Recursos:
    - Decoradores de verificação de permissão (admin, verified, anonymous)
    - Decoradores de cache com timeout configurável
    - Decoradores de logging para tempo de execução e erros
    - Decoradores de limitação de taxa para prevenir abuso de API
    - Decoradores específicos para AJAX
    - Decoradores combinados para padrões comuns

Examples:
    Permission decorators:
        @admin_required
        def admin_dashboard(request):
            return render(request, 'admin/dashboard.html')

    Caching:
        @cache_result(timeout=600, key_prefix='products')
        def get_all_products():
            return Product.objects.all()

    Rate limiting:
        @rate_limit(max_requests=10, period=60)
        def api_endpoint(request):
            return JsonResponse({'data': 'result'})

    Combined monitoring:
        @monitored_view
        def important_view(request):
            # Automatically logs errors and execution time
            pass
"""

import functools
import logging
import time
from collections import defaultdict

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


# Permission Decorators / Decoradores de Permissão


def admin_required(view_func):
    """
    Decorator that requires user to be an admin (staff).
    Decorador que requer que o usuário seja um admin (staff).

    Usage:
        @admin_required
        def my_view(request):
            ...
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You must be logged in to access this page."))
            return redirect(settings.LOGIN_URL)

        if not request.user.is_staff:
            messages.error(request, _("You must be an admin to access this page."))
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper


def superuser_required(view_func):
    """
    Decorator that requires user to be a superuser.
    Decorador que requer que o usuário seja um superusuário.

    Usage:
        @superuser_required
        def my_view(request):
            ...
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You must be logged in to access this page."))
            return redirect(settings.LOGIN_URL)

        if not request.user.is_superuser:
            messages.error(request, _("You must be a superuser to access this page."))
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper


def verified_required(view_func):
    """
    Decorator that requires user to have a verified profile.
    Decorador que requer que o usuário tenha um perfil verificado.

    Usage:
        @verified_required
        def my_view(request):
            ...
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You must be logged in to access this page."))
            return redirect(settings.LOGIN_URL)

        if not hasattr(request.user, "profile") or not request.user.profile.is_verified:
            messages.warning(
                request,
                _(
                    "You must have a verified profile to access this page. "
                    "Please complete your profile and wait for verification."
                ),
            )
            return redirect("profile")

        return view_func(request, *args, **kwargs)

    return wrapper


def anonymous_required(view_func):
    """
    Decorator that requires user to NOT be authenticated.
    Redirects to home if user is already logged in.

    Decorador que requer que o usuário NÃO esteja autenticado.
    Redireciona para home se o usuário já estiver logado.

    Usage:
        @anonymous_required
        def login_view(request):
            ...
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are already logged in."))
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper


# Caching Decorators / Decoradores de Cache


def cache_result(timeout=300, key_prefix=""):
    """
    Decorator to cache function results.
    Decorador para cachear resultados de função.

    Args:
        timeout: Cache timeout in seconds (default: 300 = 5 minutes)
        key_prefix: Prefix for cache key

    Usage:
        @cache_result(timeout=600, key_prefix='my_func')
        def expensive_function(arg1, arg2):
            ...
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            # Gera chave de cache do nome da função e argumentos
            cache_key = f"{key_prefix}:{func.__name__}:{args!s}:{kwargs!s}"

            # Try to get from cache
            # Tenta obter do cache
            result = cache.get(cache_key)

            if result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return result

            # Not in cache, execute function
            # Não está no cache, executa função
            logger.debug(f"Cache miss for {cache_key}")
            result = func(*args, **kwargs)

            # Store in cache
            # Armazena no cache
            cache.set(cache_key, result, timeout)

            return result

        return wrapper

    return decorator


# Logging Decorators / Decoradores de Logging


def log_execution_time(view_func):
    """
    Decorator to log function execution time.
    Decorador para logar tempo de execução da função.

    Usage:
        @log_execution_time
        def slow_function():
            ...
    """

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = view_func(*args, **kwargs)

        end_time = time.time()
        execution_time = end_time - start_time

        logger.info(f"{view_func.__name__} executed in {execution_time:.4f} seconds")

        return result

    return wrapper


def log_errors(view_func):
    """
    Decorator to log exceptions that occur in a function.
    Decorador para logar exceções que ocorrem em uma função.

    Usage:
        @log_errors
        def risky_function():
            ...
    """

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Error in {view_func.__name__}: {e!s}",
                exc_info=True,
                extra={
                    "function": view_func.__name__,
                    "args": args,
                    "kwargs": kwargs,
                },
            )
            raise

    return wrapper


# Rate Limiting Decorators / Decoradores de Limitação de Taxa


class SimpleRateLimiter:
    """
    Simple in-memory rate limiter.
    Limitador de taxa simples em memória.

    Note: For production, use Redis-based rate limiting.
    Nota: Para produção, use limitação de taxa baseada em Redis.
    """

    def __init__(self):
        self.requests = defaultdict(list)

    def is_rate_limited(self, identifier, max_requests, period):
        """
        Check if identifier has exceeded rate limit.
        Verifica se identificador excedeu limite de taxa.

        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            max_requests: Maximum requests allowed
            period: Time period in seconds

        Returns:
            bool: True if rate limited, False otherwise
        """
        now = time.time()

        # Remove old requests outside the time window
        # Remove requisições antigas fora da janela de tempo
        self.requests[identifier] = [
            req_time
            for req_time in self.requests[identifier]
            if now - req_time < period
        ]

        # Check if limit exceeded
        # Verifica se limite foi excedido
        if len(self.requests[identifier]) >= max_requests:
            return True

        # Add current request
        # Adiciona requisição atual
        self.requests[identifier].append(now)
        return False


# Global rate limiter instance
# Instância global do limitador de taxa
rate_limiter = SimpleRateLimiter()


def rate_limit(max_requests=10, period=60, identifier_func=None):
    """
    Decorator to rate limit function calls.
    Decorador para limitar taxa de chamadas de função.

    Args:
        max_requests: Maximum requests allowed (default: 10)
        period: Time period in seconds (default: 60)
        identifier_func: Function to get unique identifier (default: uses IP)

    Usage:
        @rate_limit(max_requests=5, period=60)
        def my_api_view(request):
            ...
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get identifier
            # Obtém identificador
            if identifier_func:
                identifier = identifier_func(request)
            else:
                identifier = request.META.get("REMOTE_ADDR", "unknown")

            # Check rate limit
            # Verifica limite de taxa
            if rate_limiter.is_rate_limited(identifier, max_requests, period):
                logger.warning(f"Rate limit exceeded for {identifier}")

                if request.accepts("application/json"):
                    return JsonResponse(
                        {
                            "error": "Rate limit exceeded. Please try again later.",
                            "detail": f"Maximum {max_requests} requests "
                            f"per {period} seconds.",
                        },
                        status=429,
                    )

                return HttpResponseForbidden(
                    "Rate limit exceeded. Please try again later."
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# API Decorators / Decoradores de API


def require_ajax(view_func):
    """
    Decorator to require AJAX requests.
    Decorador para requerer requisições AJAX.

    Usage:
        @require_ajax
        def my_ajax_view(request):
            ...
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {"error": "This endpoint requires an AJAX request."},
                status=400,
            )

        return view_func(request, *args, **kwargs)

    return wrapper


def json_response(view_func):
    """
    Decorator to automatically convert return value to JSON response.
    Decorador para converter automaticamente valor de retorno para resposta JSON.

    Usage:
        @json_response
        def my_api_view(request):
            return {"status": "success", "data": [...]}
    """

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        result = view_func(*args, **kwargs)

        # If result is already a response, return it
        # Se resultado já é uma resposta, retorna
        if hasattr(result, "status_code"):
            return result

        # Convert to JSON response
        # Converte para resposta JSON
        return JsonResponse(result, safe=False)

    return wrapper


# Combined Decorators / Decoradores Combinados


def monitored_view(view_func):
    """
    Combines logging and timing decorators.
    Combina decoradores de logging e tempo.

    Usage:
        @monitored_view
        def my_view(request):
            ...
    """
    return log_errors(log_execution_time(view_func))
