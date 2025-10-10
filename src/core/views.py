# Views - Core Application
# Views - Aplicação Core

# This module defines view functions for the core application with:
# - Authentication views (home, login, register, logout, profile)
# - Health check endpoint for monitoring
# - Custom error handlers
# - Example API endpoints
# - Proper error handling and logging
#
# Este módulo define funções de view para a aplicação core com:
# - Views de autenticação (home, login, register, logout, profile)
# - Endpoint de health check para monitoramento
# - Handlers de erro customizados
# - Endpoints de API de exemplo
# - Tratamento de erros e logging apropriado

import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import LoginForm, ProductForm, RegisterForm, UserProfileForm, UserUpdateForm
from .models import Category, Product, Tag

# Configure logger for this module
# Configura logger para este módulo
logger = logging.getLogger(__name__)


# Home View / View da Home


def home(request):
    """
    Homepage view with different content for authenticated vs anonymous users.
    Displays welcome message and navigation options based on authentication status.

    View da homepage com conteúdo diferente para usuários autenticados vs anônimos.
    Exibe mensagem de boas-vindas e opções de navegação baseado no status de autenticação.

    Args / Argumentos:
        request (HttpRequest): HTTP request object / Objeto de requisição HTTP

    Returns / Retorna:
        HttpResponse: Rendered home template / Template home renderizado

    Template / Template:
        auth/home.html

    Context Variables / Variáveis de Contexto:
        title (str): Page title / Título da página
        user (User): Current user object (anonymous or authenticated) / Objeto do usuário atual
    """
    context = {
        "title": _("Welcome to Django Base"),
        "user": request.user,
    }
    return render(request, "auth/home.html", context)


# Authentication Views / Views de Autenticação


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    User login view with form validation and error handling.
    Authenticates users and manages session duration based on "remember me" option.

    View de login com validação de formulário e tratamento de erros.
    Autentica usuários e gerencia duração da sessão baseado na opção "lembrar-me".

    Features / Recursos:
        - Custom LoginForm with Bootstrap styling / LoginForm customizado com Bootstrap
        - Remember me functionality (2 weeks session) / Funcionalidade lembrar-me (sessão de 2 semanas)
        - Redirect to next URL or home after login / Redireciona para próximo URL ou home
        - Error messages for invalid credentials / Mensagens de erro para credenciais inválidas
        - Automatic redirect if already authenticated / Redirecionamento automático se já autenticado

    Args / Argumentos:
        request (HttpRequest): HTTP request object / Objeto de requisição HTTP

    Returns / Retorna:
        HttpResponse: Rendered login template or redirect / Template de login ou redirecionamento

    HTTP Methods / Métodos HTTP:
        GET: Display login form / Exibe formulário de login
        POST: Process login credentials / Processa credenciais de login

    Template / Template:
        auth/login.html

    Session Behavior / Comportamento da Sessão:
        - remember_me=False: Session expires on browser close / Sessão expira ao fechar navegador
        - remember_me=True: Session lasts 2 weeks (1209600 seconds) / Sessão dura 2 semanas
    """
    # Redirect authenticated users to home
    # Redireciona usuários autenticados para home
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me", False)

            # Authenticate user
            # Autentica usuário
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Login user
                # Faz login do usuário
                login(request, user)

                # Set session expiry based on remember_me
                # Define expiração da sessão baseado em remember_me
                if not remember_me:
                    # Session expires when browser closes
                    # Sessão expira quando navegador fecha
                    request.session.set_expiry(0)
                else:
                    # Session expires after 2 weeks
                    # Sessão expira após 2 semanas
                    request.session.set_expiry(1209600)  # 2 weeks in seconds

                messages.success(
                    request,
                    _("Welcome back, {username}!").format(username=user.username),
                )

                # Redirect to next URL or home
                # Redireciona para próximo URL ou home
                next_url = request.GET.get("next", "home")
                return redirect(next_url)
            else:
                messages.error(request, _("Invalid username or password."))
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = LoginForm()

    context = {"form": form, "title": _("Login")}
    return render(request, "auth/login.html", context)


@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    User registration view with form validation and automatic login.
    View de registro com validação de formulário e login automático.

    Features:
        - Custom RegisterForm with email validation
        - Automatic UserProfile creation via signals
        - Automatic login after successful registration
        - Success messages

    Args:
        request: HTTP request object

    Returns:
        Rendered registration template or redirect after successful registration
    """
    # Redirect authenticated users to home
    # Redireciona usuários autenticados para home
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save new user
            # Salva novo usuário
            user = form.save()

            # UserProfile is automatically created via signal
            # UserProfile é criado automaticamente via sinal

            # Login user automatically
            # Faz login do usuário automaticamente
            login(request, user)

            messages.success(
                request,
                _("Account created successfully! Welcome, {username}!").format(
                    username=user.username
                ),
            )

            return redirect("home")
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = RegisterForm()

    context = {"form": form, "title": _("Register")}
    return render(request, "auth/register.html", context)


@require_http_methods(["POST", "GET"])
def logout_view(request):
    """
    User logout view with confirmation message.
    View de logout com mensagem de confirmação.

    Args:
        request: HTTP request object

    Returns:
        Redirect to home page
    """
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, _("Goodbye, {username}!").format(username=username))
    return redirect("home")


# Profile Views / Views de Perfil


@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request):
    """
    User profile view for viewing and editing profile information.
    View de perfil para visualizar e editar informações do perfil.

    Features:
        - Displays user information and profile data
        - Allows editing both User and UserProfile models
        - Form validation and error handling
        - Success messages after updates

    Args:
        request: HTTP request object

    Returns:
        Rendered profile template
    """
    # Get or create user profile (should exist via signal)
    # Obtém ou cria perfil do usuário (deve existir via sinal)
    user_profile = request.user.profile

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile updated successfully!"))
            return redirect("profile")
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "title": _("My Profile"),
    }
    return render(request, "auth/profile.html", context)


@require_http_methods(["GET"])
def products_view(request):
    """
    Product listing page with filters and pagination.
    Página de listagem de produtos com filtros e paginação.
    """
    products = (
        Product.objects.filter(is_active=True)
        .select_related("category", "created_by")
        .prefetch_related("tags")
    )

    # Filters
    category_id = request.GET.get("category")
    tag_slug = request.GET.get("tag")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    search_query = request.GET.get("search")

    if category_id:
        products = products.filter(category_id=category_id)
    if tag_slug:
        products = products.filter(tags__slug=tag_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Pagination
    from django.core.paginator import Paginator

    paginator = Paginator(products, 9)
    page = request.GET.get("page", 1)
    products_page = paginator.get_page(page)

    context = {
        "products": products_page,
        "categories": Category.objects.filter(is_active=True),
        "tags": Tag.objects.all()[:10],
        "title": _("Products"),
    }
    return render(request, "auth/products.html", context)


@require_http_methods(["GET"])
def health_check_page(request):
    """
    Beautiful health check page for visual monitoring.
    Página bonita de health check para monitoramento visual.
    """
    return render(request, "health/health_check.html", {"title": "Health Check"})


def about_view(request):
    """
    About page with project information and developer details.
    Página sobre com informações do projeto e detalhes do desenvolvedor.

    Displays:
        - Project technology stack
        - Main features
        - Developer information (@mugubr)
        - Repository links
        - Contributing guidelines

    Exibe:
        - Stack de tecnologia do projeto
        - Principais recursos
        - Informações do desenvolvedor (@mugubr)
        - Links do repositório
        - Diretrizes de contribuição

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered about.html template

    Args:
        request: Objeto HttpRequest

    Retorna:
        HttpResponse: Template about.html renderizado
    """
    return render(request, "auth/about.html", {"title": _("About")})


# Health Check Endpoint
# Endpoint de Health Check


@extend_schema(
    responses={
        200: {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"},
                "version": {"type": "string"},
                "checks": {"type": "object"},
            },
        }
    },
    summary="Performs a health check of the application and its services",
)
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
        ```
        {
            "status": "healthy",
            "timestamp": "2024-01-15T10:30:00Z",
            "version": "1.0.0",
            "checks": {
                "database": "ok",
                "cache": "ok"
            }
        }
        ```
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


@extend_schema(
    # Descreve o que a view retorna em caso de sucesso (200 OK)
    # Describes what the view returns on success (200 OK)
    responses={
        200: {
            "type": "object",
            "properties": {"message": {"type": "string"}},
        }
    },
    # Adiciona um resumo para a documentação da API
    # Adds a summary for the API documentation
    summary="Returns a simple hello message",
)
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


@extend_schema(
    responses={
        200: {
            "type": "object",
            "properties": {
                "api_version": {"type": "string"},
                "endpoints": {"type": "object"},
                "documentation": {"type": "string"},
                "status": {"type": "string"},
            },
        }
    },
    summary="Returns general information about the API",
)
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


@login_required
@require_http_methods(["GET", "POST"])
def product_create_view(request):
    """Product creation view / View de criação de produto"""
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            form.save_m2m()  # Save tags
            messages.success(request, _("Product created successfully!"))
            return redirect("products")
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = ProductForm()

    return render(
        request,
        "auth/product_create.html",
        {"title": _("Create Product"), "form": form},
    )
