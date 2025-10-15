# Environment Variables Validator
# Validador de Variáveis de Ambiente

"""
Environment variables validation module for Django Base project.
Validates critical environment variables on application startup to prevent
configuration errors in production.

Módulo de validação de variáveis de ambiente para o projeto Django Base.
Valida variáveis de ambiente críticas na inicialização da aplicação para prevenir
erros de configuração em produção.

Usage / Uso:
    from django_base.settings.env_validator import validate_environment

    # Call at the end of settings file / Chame no final do arquivo settings
    validate_environment(
        environment='production',
        debug=False,
        secret_key=SECRET_KEY,
        allowed_hosts=ALLOWED_HOSTS,
        database_url=DATABASES['default']['HOST']
    )
"""

import os
import warnings
from typing import Any


class EnvironmentValidationError(Exception):
    """
    Exception raised when critical environment validation fails.
    Exceção levantada quando validação crítica de ambiente falha.
    """

    pass


class EnvironmentValidator:
    """
    Validates environment variables for Django application.
    Valida variáveis de ambiente para aplicação Django.

    This class checks critical configuration values on startup and raises
    errors or warnings for missing/invalid settings.

    Esta classe verifica valores críticos de configuração na inicialização e levanta
    erros ou avisos para configurações ausentes/inválidas.
    """

    # Required environment variables for all environments
    # Variáveis de ambiente obrigatórias para todos os ambientes
    REQUIRED_VARS = [
        "SECRET_KEY",
        "DJANGO_SETTINGS_MODULE",
    ]

    # Required for production environment
    # Obrigatórias para ambiente de produção
    PRODUCTION_REQUIRED_VARS = [
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "ALLOWED_HOSTS",
    ]

    # Recommended but not required
    # Recomendadas mas não obrigatórias
    RECOMMENDED_VARS = [
        "REDIS_HOST",
        "REDIS_PORT",
        "EMAIL_HOST",
        "EMAIL_HOST_USER",
    ]

    def __init__(self, environment: str = "development"):
        """
        Initialize validator with environment type.
        Inicializa validador com tipo de ambiente.

        Args / Argumentos:
            environment (str): 'development', 'production', or 'test'
        """
        self.environment = environment.lower()
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_required_vars(self) -> None:
        """
        Validate that all required environment variables are set.
        Valida que todas as variáveis de ambiente obrigatórias estão definidas.

        Raises / Levanta:
            EnvironmentValidationError: If critical variables are missing
        """
        missing_vars = []

        # Check basic required vars / Verifica variáveis básicas obrigatórias
        for var in self.REQUIRED_VARS:
            if not os.getenv(var):
                missing_vars.append(var)

        # Check production-specific vars / Verifica variáveis específicas de produção
        if self.environment == "production":
            for var in self.PRODUCTION_REQUIRED_VARS:
                if not os.getenv(var):
                    missing_vars.append(var)

        if missing_vars:
            self.errors.append(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    def validate_secret_key(self, secret_key: str) -> None:
        """
        Validate SECRET_KEY strength and security.
        Valida força e segurança da SECRET_KEY.

        Args / Argumentos:
            secret_key (str): Django SECRET_KEY value
        """
        if not secret_key:
            self.errors.append("SECRET_KEY is empty")
            return

        # Check if using default/insecure key
        # Verifica se está usando chave padrão/insegura
        insecure_keys = [
            "django-insecure-",
            "changeme",
            "pleasechangeme",
            "secret",
            "your-secret-key-here",
        ]

        if any(insecure in secret_key.lower() for insecure in insecure_keys):
            self.errors.append(
                "SECRET_KEY appears to be insecure or default. "
                "Please generate a strong, unique key for production."
            )

        # Check minimum length / Verifica comprimento mínimo
        if len(secret_key) < 50:
            self.warnings.append(
                f"SECRET_KEY is only {len(secret_key)} characters. "
                "Recommended minimum is 50 characters."
            )

    def validate_debug_mode(self, debug: bool) -> None:
        """
        Validate DEBUG setting based on environment.
        Valida configuração DEBUG baseado no ambiente.

        Args / Argumentos:
            debug (bool): Django DEBUG setting value
        """
        if self.environment == "production" and debug:
            self.errors.append(
                "DEBUG=True in production environment! "
                "This is a critical security risk."
            )

    def validate_allowed_hosts(self, allowed_hosts: list[str]) -> None:
        """
        Validate ALLOWED_HOSTS configuration.
        Valida configuração de ALLOWED_HOSTS.

        Args / Argumentos:
            allowed_hosts (List[str]): Django ALLOWED_HOSTS value
        """
        if self.environment == "production":
            if not allowed_hosts:
                self.errors.append("ALLOWED_HOSTS is empty in production")
            elif "*" in allowed_hosts:
                self.errors.append(
                    "ALLOWED_HOSTS contains '*' (wildcard) in production. "
                    "This is insecure. Specify exact domains."
                )
            elif "localhost" in allowed_hosts or "127.0.0.1" in allowed_hosts:
                self.warnings.append(
                    "ALLOWED_HOSTS contains 'localhost' or '127.0.0.1' in production. "
                    "This may not be intended."
                )

    def validate_database_config(self, database_config: dict[str, Any]) -> None:
        """
        Validate database configuration.
        Valida configuração do banco de dados.

        Args / Argumentos:
            database_config (Dict): Django DATABASES['default'] config
        """
        if not database_config.get("NAME"):
            self.errors.append("Database NAME is not configured")

        if not database_config.get("USER"):
            self.errors.append("Database USER is not configured")

        if not database_config.get("PASSWORD"):
            if self.environment == "production":
                self.errors.append("Database PASSWORD is not configured in production")
            else:
                self.warnings.append("Database PASSWORD is not configured")

        # Check for weak passwords in production
        # Verifica senhas fracas em produção
        if self.environment == "production":
            password = database_config.get("PASSWORD", "")
            weak_passwords = ["postgres", "password", "123456", "admin"]
            if password.lower() in weak_passwords:
                self.errors.append(
                    "Database password appears to be weak. "
                    "Use a strong, unique password in production."
                )

    def validate_ssl_settings(
        self,
        secure_ssl_redirect: bool,
        session_cookie_secure: bool,
        csrf_cookie_secure: bool,
    ) -> None:
        """
        Validate SSL/HTTPS security settings.
        Valida configurações de segurança SSL/HTTPS.

        Args / Argumentos:
            secure_ssl_redirect (bool): SECURE_SSL_REDIRECT value
            session_cookie_secure (bool): SESSION_COOKIE_SECURE value
            csrf_cookie_secure (bool): CSRF_COOKIE_SECURE value
        """
        if self.environment == "production":
            if not secure_ssl_redirect:
                self.warnings.append(
                    "SECURE_SSL_REDIRECT is False in production. "
                    "Consider enabling HTTPS redirect."
                )

            if not session_cookie_secure:
                self.warnings.append(
                    "SESSION_COOKIE_SECURE is False in production. "
                    "Session cookies should be sent over HTTPS only."
                )

            if not csrf_cookie_secure:
                self.warnings.append(
                    "CSRF_COOKIE_SECURE is False in production. "
                    "CSRF cookies should be sent over HTTPS only."
                )

    def validate_recommended_vars(self) -> None:
        """
        Check recommended (but not required) environment variables.
        Verifica variáveis de ambiente recomendadas (mas não obrigatórias).
        """
        missing_recommended = []
        for var in self.RECOMMENDED_VARS:
            if not os.getenv(var):
                missing_recommended.append(var)

        if missing_recommended:
            self.warnings.append(
                f"Recommended environment variables not set: {', '.join(missing_recommended)}"
            )

    def report(self) -> None:
        """
        Print validation report with errors and warnings.
        Imprime relatório de validação com erros e avisos.

        Raises / Levanta:
            EnvironmentValidationError: If critical errors found
        """
        print("\n" + "=" * 70)
        print("🔍 Environment Variables Validation Report")
        print("🔍 Relatório de Validação de Variáveis de Ambiente")
        print("=" * 70)
        print(f"Environment / Ambiente: {self.environment.upper()}")
        print("=" * 70 + "\n")

        # Print warnings / Imprime avisos
        if self.warnings:
            print("⚠️  WARNINGS / AVISOS:")
            for warning in self.warnings:
                print(f"  - {warning}")
                warnings.warn(warning, UserWarning)  # noqa: B028
            print()

        # Print errors / Imprime erros
        if self.errors:
            print("❌ ERRORS / ERROS:")
            for error in self.errors:
                print(f"  - {error}")
            print()
            print("=" * 70)
            print("❌ Environment validation FAILED / Validação de ambiente FALHOU")
            print("=" * 70 + "\n")
            raise EnvironmentValidationError(
                f"Environment validation failed with {len(self.errors)} error(s). "
                "Please fix the issues above before starting the application."
            )

        # Success message / Mensagem de sucesso
        if not self.errors:
            status = "✅ PASSED" if not self.warnings else "✅ PASSED (with warnings)"
            print(
                f"{status} / {'PASSOU' if not self.warnings else 'PASSOU (com avisos)'}"
            )
            print("=" * 70 + "\n")


def validate_environment(
    environment: str | None = None,
    debug: bool = False,
    secret_key: str = "",
    allowed_hosts: list[str] | None = None,
    database_config: dict[str, Any] | None = None,
    secure_ssl_redirect: bool = False,
    session_cookie_secure: bool = False,
    csrf_cookie_secure: bool = False,
) -> None:
    """
    Main validation function to be called from settings.
    Função principal de validação para ser chamada dos settings.

    This function should be called at the end of your settings file to validate
    all critical configuration before the application starts.

    Esta função deve ser chamada no final do arquivo settings para validar
    toda configuração crítica antes da aplicação iniciar.

    Args / Argumentos:
        environment (str): Current environment ('development', 'production', 'test')
        debug (bool): DEBUG setting value
        secret_key (str): SECRET_KEY value
        allowed_hosts (List[str]): ALLOWED_HOSTS value
        database_config (Dict): DATABASES['default'] configuration
        secure_ssl_redirect (bool): SECURE_SSL_REDIRECT value
        session_cookie_secure (bool): SESSION_COOKIE_SECURE value
        csrf_cookie_secure (bool): CSRF_COOKIE_SECURE value

    Raises / Levanta:
        EnvironmentValidationError: If validation fails with critical errors

    Example / Exemplo:
        ```python
        # At the end of settings/prod.py / No final de settings/prod.py
        from django_base.settings.env_validator import validate_environment

        validate_environment(
            environment='production',
            debug=DEBUG,
            secret_key=SECRET_KEY,
            allowed_hosts=ALLOWED_HOSTS,
            database_config=DATABASES['default'],
            secure_ssl_redirect=SECURE_SSL_REDIRECT,
            session_cookie_secure=SESSION_COOKIE_SECURE,
            csrf_cookie_secure=CSRF_COOKIE_SECURE,
        )
        ```
    """
    # Auto-detect environment if not provided
    # Auto-detecta ambiente se não fornecido
    if environment is None:
        settings_module = os.getenv("DJANGO_SETTINGS_MODULE", "")
        if "prod" in settings_module:
            environment = "production"
        elif "test" in settings_module:
            environment = "test"
        else:
            environment = "development"

    # Skip validation in test environment
    # Pula validação em ambiente de teste
    if environment == "test":
        return

    # Initialize validator / Inicializa validador
    validator = EnvironmentValidator(environment=environment)

    # Run all validations / Executa todas as validações
    validator.validate_required_vars()
    validator.validate_secret_key(secret_key)
    validator.validate_debug_mode(debug)

    if allowed_hosts is not None:
        validator.validate_allowed_hosts(allowed_hosts)

    if database_config is not None:
        validator.validate_database_config(database_config)

    validator.validate_ssl_settings(
        secure_ssl_redirect, session_cookie_secure, csrf_cookie_secure
    )
    validator.validate_recommended_vars()

    # Print report and raise if errors found
    # Imprime relatório e levanta exceção se erros encontrados
    validator.report()
