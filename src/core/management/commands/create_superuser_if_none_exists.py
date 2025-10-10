"""
Custom Management Command: Create Superuser if None Exists
Comando de Gerenciamento Customizado: Criar Superusuário se Nenhum Existir

This command creates a default superuser account if
no superuser exists in the database.
Useful for automated deployments, Docker containers, and CI/CD pipelines.

Este comando cria uma conta de superusuário padrão se
nenhum superusuário existir no banco.
Útil para deploys automatizados, containers Docker e pipelines CI/CD.

Usage / Uso:
    python manage.py create_superuser_if_none_exists
    python manage.py create_superuser_if_none_exists --username admin --password secret
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django management command to create a superuser if none exists.
    Comando de gerenciamento Django para criar um superusuário
    se nenhum existir.
    """

    help = """Create a superuser if none exists
    / Cria um superusuário se nenhum existir"""

    def add_arguments(self, parser):
        """
        Add command arguments.
        Adiciona argumentos do comando.
        """
        parser.add_argument(
            "--username",
            type=str,
            default="admin",
            help="Superuser username / Nome de usuário do superusuário (padrão: admin)",
        )
        parser.add_argument(
            "--email",
            type=str,
            default="admin@example.com",
            help="Superuser email / Email do superusuário (padrão: admin@example.com)",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="admin",
            help="Superuser password / Senha do superusuário (padrão: admin)",
        )

    def handle(self, *args, **options):
        """
        Handle the command execution.
        Manipula a execução do comando.
        """
        User = get_user_model()

        # Check if any superuser exists
        # Verifica se algum superusuário existe
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  Superuser already exists. Skipping creation. / "
                    "Superusuário já existe. Pulando criação."
                )
            )
            return

        # Get command arguments
        # Obtem argumentos do comando
        username = options["username"]
        email = options["email"]
        password = options["password"]

        # Create superuser
        # Cria superusuário
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Superuser '{username}' created successfully! / "
                    f"Superusuário '{username}' criado com sucesso!\n"
                    f"   Username/Usuário: {username}\n"
                    f"   Email: {email}\n"
                    f"   Password/Senha: {password}"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Error creating superuser / Erro ao criar superusuário: {e}"
                )
            )
