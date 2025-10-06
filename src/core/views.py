# Views - Core Application
# Views - Aplicação Core

# This module defines view functions for the core application with:
# - Health check endpoint for monitoring
# - Custom error handlers
# - Example API endpoints
# - Proper error handling and logging
#
# Este módulo define funções de view para a aplicação core com:
# - Endpoint de health check para monitoramento
# - Handlers de erro customizados
# - Endpoints de API de exemplo
# - Tratamento de erros e logging apropriado

import logging
from datetime import datetime

from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Configure logger for this module
# Configura logger para este módulo
logger = logging.getLogger(__name__)


# Health Check Endpoint
# Endpoint de Health Check


@api_view(["GET"])
def health_check(request):
    """
    Health check endpoint for monitoring services (Docker, Kubernetes, load balancers).
    Returns application status and basic diagnostics.

    Endpoint de health check para serviços de monitoramento (Docker,
      Kubernetes, load balancers).
    Retorna status da aplicação e diagnósticos básicos.

    Returns:
        Response: JSON with health status and diagnostics

    HTTP Status Codes:
        200: Application is healthy
        503: Application has issues (database down, etc.)

    Example Response (Healthy):
        {
            "status": "healthy",
            "timestamp": "2024-01-15T10:30:00Z",
            "version": "1.0.0",
            "checks": {
                "database": "ok",
                "cache": "ok"
            }
        }
    """
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",  # Update this with your app version
            "environment": "production",  # Could read from settings
        }

        # Check database connectivity
        # Verifica conectividade com banco de dados
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health_status["checks"] = {"database": "ok"}
        except Exception as db_error:
            logger.error(f"Database health check failed: {db_error}")
            health_status["status"] = "unhealthy"
            health_status["checks"] = {
                "database": "error",
                "error": str(db_error),
            }
            return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Check cache (if configured)
        # Verifica cache (se configurado)
        try:
            from django.core.cache import cache

            cache.set("health_check", "ok", 10)
            cache_status = cache.get("health_check")
            health_status["checks"]["cache"] = (
                "ok" if cache_status == "ok" else "warning"
            )
        except Exception as cache_error:
            logger.warning(f"Cache health check failed: {cache_error}")
            health_status["checks"]["cache"] = "unavailable"
            # Cache failure is not critical - don't mark as unhealthy
            # Falha de cache não é crítica - não marca como unhealthy

        return Response(health_status, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Health check endpoint error: {e}", exc_info=True)
        return Response(
            {
                "status": "error",
                "message": "Health check failed",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# API Endpoints
# Endpoints da API


@api_view(["GET"])
def hello_api(request):
    """
    An example endpoint that returns a welcome message.
    Used to quickly test if the API is up and running.
    Um endpoint de exemplo que retorna uma mensagem de boas-vindas.
    Usado para testar rapidamente se a API está no ar e funcionando.
    """
    data = {"message": "Olá, API do Projeto Base Django!"}
    return Response(data, status=status.HTTP_200_OK)


# Custom Error Handlers
# Handlers de Erro Customizados


def custom_404(request, exception=None):
    """
    Custom handler for 404 Not Found errors.
    Returns a JSON response for API requests, HTML for browser requests.

    Handler customizado para erros 404 Not Found.
    Retorna resposta JSON para requisições de API, HTML
    para requisições de navegador.

    Args:
        request: The HTTP request
        exception: The exception that triggered this handler (optional)

    Returns:
        JsonResponse: Custom 404 error response
    """
    logger.warning(
        f"404 Not Found: {request.path} - Method: {request.method} - "
        f"IP: {request.META.get('REMOTE_ADDR')}"
    )

    # Check if this is an API request (Accept: application/json)
    # Verifica se é uma requisição de API (Accept: application/json)
    if request.accepts("application/json") or request.path.startswith("/api/"):
        return JsonResponse(
            {
                "error": "Not Found",
                "message": f"The requested resource '{request.path}' was not found.",
                "status_code": 404,
                "path": request.path,
            },
            status=404,
        )

    # For browser requests, could render a custom HTML template
    # Para requisições de navegador, poderia renderizar um
    # template HTML customizado
    # from django.shortcuts import render
    # return render(request, 'errors/404.html', status=404)

    # For now, return JSON for all requests
    # Por enquanto, retorna JSON para todas as requisições
    return JsonResponse(
        {
            "error": "Not Found",
            "message": "The requested page was not found.",
            "status_code": 404,
        },
        status=404,
    )


def custom_500(request):
    """
    Custom handler for 500 Internal Server Error.
    Logs the error and returns a user-friendly message.

    Handler customizado para erro 500 Internal Server Error.
    Loga o erro e retorna uma mensagem amigável ao usuário.

    Args:
        request: The HTTP request

    Returns:
        JsonResponse: Custom 500 error response
    """
    logger.error(
        f"500 Internal Server Error: {request.path} - Method: {request.method} - "
        f"IP: {request.META.get('REMOTE_ADDR')}",
        exc_info=True,
    )

    return JsonResponse(
        {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Our team has been notified.",
            "status_code": 500,
        },
        status=500,
    )


def custom_403(request, exception=None):
    """
    Custom handler for 403 Forbidden errors.
    Returns information about permission requirements.

    Handler customizado para erros 403 Forbidden.
    Retorna informações sobre requisitos de permissão.

    Args:
        request: The HTTP request
        exception: The exception that triggered this handler (optional)

    Returns:
        JsonResponse: Custom 403 error response
    """
    logger.warning(
        f"403 Forbidden: {request.path} - User: {request.user} - "
        f"IP: {request.META.get('REMOTE_ADDR')}"
    )

    return JsonResponse(
        {
            "error": "Forbidden",
            "message": "You don't have permission to access this resource.",
            "status_code": 403,
            "authentication_required": not request.user.is_authenticated,
        },
        status=403,
    )


def custom_400(request, exception=None):
    """
    Custom handler for 400 Bad Request errors.
    Provides details about what went wrong with the request.

    Handler customizado para erros 400 Bad Request.
    Fornece detalhes sobre o que deu errado com a requisição.

    Args:
        request: The HTTP request
        exception: The exception that triggered this handler (optional)

    Returns:
        JsonResponse: Custom 400 error response
    """
    logger.warning(f"400 Bad Request: {request.path} - Method: {request.method}")

    return JsonResponse(
        {
            "error": "Bad Request",
            "message": "The request could not be understood or "
            "was missing required parameters.",
            "status_code": 400,
        },
        status=400,
    )


# Utility Views
# Views Utilitárias


@api_view(["GET"])
def api_info(request):
    """
    Returns information about the API endpoints and version.
    Useful for API discovery and documentation.

    Retorna informações sobre os endpoints da API e versão.
    Útil para descoberta de API e documentação.

    Returns:
        Response: API information
    """
    info = {
        "api_version": "1.0.0",
        "endpoints": {
            "health": "/health/",
            "hello": "/api/hello/",
            "products": "/api/v1/products/",
            "info": "/api/info/",
        },
        "documentation": "/api/docs/",  # If using drf-spectacular
        "status": "operational",
    }

    return Response(info, status=status.HTTP_200_OK)
