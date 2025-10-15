"""
Django management command to validate environment variables.
Comando de gerenciamento Django para validar variáveis de ambiente.

This command checks if all required environment variables are set
and have valid values before starting the application.
Este comando verifica se todas variáveis de ambiente necessárias estão
definidas e têm valores válidos antes de iniciar a aplicação.
"""

import os
import sys

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Validate required environment variables and their values.
    Valida variáveis de ambiente obrigatórias e seus valores.
    """

    help = "Validate required environment variables / Valida variáveis de ambiente obrigatórias"

    # Required environment variables / Variáveis de ambiente obrigatórias
    REQUIRED_VARS = {
        "SECRET_KEY": {
            "description": "Django secret key for cryptographic signing / Chave secreta Django para assinatura criptográfica",
            "min_length": 50,
            "validate": lambda x: len(x) >= 50,
            "error_message": "SECRET_KEY must be at least 50 characters long / SECRET_KEY deve ter pelo menos 50 caracteres",
        },
        "DEBUG": {
            "description": "Debug mode (True/False) / Modo debug (True/False)",
            "allowed_values": ["True", "False", "true", "false", "1", "0"],
            "validate": lambda x: x in ["True", "False", "true", "false", "1", "0"],
            "error_message": "DEBUG must be True or False / DEBUG deve ser True ou False",
        },
        "DATABASE_URL": {
            "description": "Database connection URL / URL de conexão do banco de dados",
            "validate": lambda x: x.startswith(("postgres://", "postgresql://")),
            "error_message": "DATABASE_URL must be a valid PostgreSQL URL / DATABASE_URL deve ser uma URL PostgreSQL válida",
        },
        "REDIS_URL": {
            "description": "Redis connection URL / URL de conexão do Redis",
            "validate": lambda x: x.startswith("redis://"),
            "error_message": "REDIS_URL must be a valid Redis URL / REDIS_URL deve ser uma URL Redis válida",
        },
        "POSTGRES_DB": {
            "description": "PostgreSQL database name / Nome do banco de dados PostgreSQL",
            "validate": lambda x: len(x) > 0,
            "error_message": "POSTGRES_DB cannot be empty / POSTGRES_DB não pode estar vazio",
        },
        "POSTGRES_USER": {
            "description": "PostgreSQL user / Usuário PostgreSQL",
            "validate": lambda x: len(x) > 0,
            "error_message": "POSTGRES_USER cannot be empty / POSTGRES_USER não pode estar vazio",
        },
        "POSTGRES_PASSWORD": {
            "description": "PostgreSQL password / Senha PostgreSQL",
            "min_length": 8,
            "validate": lambda x: len(x) >= 8,
            "error_message": "POSTGRES_PASSWORD must be at least 8 characters / POSTGRES_PASSWORD deve ter pelo menos 8 caracteres",
        },
    }

    # Optional but recommended variables / Variáveis opcionais mas recomendadas
    RECOMMENDED_VARS = {
        "ALLOWED_HOSTS": {
            "description": "Comma-separated list of allowed hosts / Lista de hosts permitidos separados por vírgula",
        },
        "CSRF_TRUSTED_ORIGINS": {
            "description": "Comma-separated list of trusted origins for CSRF / Lista de origens confiáveis para CSRF",
        },
        "SENTRY_DSN": {
            "description": "Sentry DSN for error tracking / DSN do Sentry para rastreamento de erros",
        },
    }

    def add_arguments(self, parser):
        """
        Add command arguments.
        Adiciona argumentos do comando.
        """
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Fail if recommended variables are missing / Falha se variáveis recomendadas estiverem faltando",
        )
        parser.add_argument(
            "--exit-on-error",
            action="store_true",
            help="Exit with error code if validation fails / Sai com código de erro se validação falhar",
        )

    def handle(self, *args, **options):
        """
        Execute the command.
        Executa o comando.
        """
        self.stdout.write(
            self.style.SUCCESS(
                "\n🔍 Validating Environment Variables / Validando Variáveis de Ambiente\n"
            )
        )

        errors = []
        warnings = []

        # Check required variables / Verifica variáveis obrigatórias
        self.stdout.write("\n📋 Required Variables / Variáveis Obrigatórias:\n")
        for var_name, config in self.REQUIRED_VARS.items():
            var_value = os.environ.get(var_name)

            if var_value is None:
                error_msg = f"❌ {var_name}: MISSING / FALTANDO"
                self.stdout.write(self.style.ERROR(f"  {error_msg}"))
                self.stdout.write(f"     {config['description']}")
                errors.append(f"{var_name} is not set / não está definida")
            else:
                # Validate value / Valida valor
                if "validate" in config and not config["validate"](var_value):
                    error_msg = f"❌ {var_name}: INVALID / INVÁLIDO"
                    self.stdout.write(self.style.ERROR(f"  {error_msg}"))
                    self.stdout.write(f"     {config['error_message']}")
                    errors.append(config["error_message"])
                else:
                    # Mask sensitive values / Mascara valores sensíveis
                    if var_name in [
                        "SECRET_KEY",
                        "POSTGRES_PASSWORD",
                        "SENTRY_DSN",
                    ]:
                        display_value = var_value[:8] + "..." + var_value[-8:]
                    else:
                        display_value = var_value

                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ {var_name}: {display_value}")
                    )

        # Check recommended variables / Verifica variáveis recomendadas
        self.stdout.write("\n💡 Recommended Variables / Variáveis Recomendadas:\n")
        for var_name, config in self.RECOMMENDED_VARS.items():
            var_value = os.environ.get(var_name)

            if var_value is None:
                warning_msg = f"⚠️  {var_name}: NOT SET / NÃO DEFINIDA"
                self.stdout.write(self.style.WARNING(f"  {warning_msg}"))
                self.stdout.write(f"     {config['description']}")
                warnings.append(f"{var_name} is not set / não está definida")
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"  ✅ {var_name}: SET / DEFINIDA")
                )

        # Summary / Resumo
        self.stdout.write("\n" + "=" * 60)
        if errors:
            self.stdout.write(
                self.style.ERROR(
                    f"\n❌ Validation Failed / Validação Falhou: {len(errors)} error(s) / erro(s)\n"
                )
            )
            for error in errors:
                self.stdout.write(self.style.ERROR(f"  • {error}"))

            if options["exit_on_error"]:
                sys.exit(1)
            else:
                raise CommandError(
                    "Environment validation failed / Validação de ambiente falhou"
                )

        if warnings:
            self.stdout.write(
                self.style.WARNING(f"\n⚠️  {len(warnings)} warning(s) / aviso(s):\n")
            )
            for warning in warnings:
                self.stdout.write(self.style.WARNING(f"  • {warning}"))

            if options["strict"]:
                self.stdout.write(
                    self.style.ERROR(
                        "\n❌ Strict mode: Recommended variables are missing / Modo estrito: Variáveis recomendadas estão faltando"
                    )
                )
                if options["exit_on_error"]:
                    sys.exit(1)
                else:
                    raise CommandError(
                        "Strict mode: Recommended variables missing / Modo estrito: Variáveis recomendadas faltando"
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "\n✅ Environment validation passed! / Validação de ambiente passou!\n"
            )
        )
