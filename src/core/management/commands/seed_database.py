"""
Django management command to seed the database with sample data.
Comando Django para popular o banco de dados com dados de exemplo.

Usage / Uso:
    python manage.py seed_database
    python manage.py seed_database --clear  # Clear existing data first
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Category, Product, Tag, UserProfile

User = get_user_model()


class Command(BaseCommand):
    """
    Seed database with sample data for development and testing.
    Popula banco de dados com dados de exemplo para desenvolvimento e testes.
    """

    help = "Seed database with sample data / Popular banco com dados de exemplo"

    def add_arguments(self, parser):
        """
        Add command line arguments.
        Adiciona argumentos de linha de comando.
        """
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding / Limpar dados antes de popular",
        )

    def handle(self, *args, **options):
        """
        Execute the command.
        Executa o comando.
        """
        clear = options.get("clear", False)

        if clear:
            self.stdout.write(
                "Clearing existing data... / Limpando dados existentes..."
            )
            self.clear_data()

        self.stdout.write("Seeding database... / Populando banco de dados...")

        with transaction.atomic():
            users = self.create_users()
            categories = self.create_categories()
            tags = self.create_tags()
            products = self.create_products(users, categories, tags)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDatabase seeded successfully! / Banco populado com sucesso!\n"
                f"- {len(users)} users / usuários\n"
                f"- {len(categories)} categories / categorias\n"
                f"- {len(tags)} tags\n"
                f"- {len(products)} products / produtos"
            )
        )

    def clear_data(self):
        """
        Clear existing data from database.
        Limpa dados existentes do banco de dados.
        """
        Product.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        UserProfile.objects.exclude(user__is_superuser=True).delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.WARNING("Data cleared / Dados limpos"))

    def create_users(self):
        """
        Create sample users with profiles.
        Cria usuários de exemplo com perfis.
        """
        self.stdout.write("Creating users... / Criando usuários...")

        users = []
        user_data = [
            {
                "username": "alice",
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Silva",
                "bio": "Full-stack developer passionate about Django and React.",
                "city": "São Paulo",
                "country": "Brazil",
                "phone": "+55 11 98765-4321",
            },
            {
                "username": "bob",
                "email": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Santos",
                "bio": "Backend engineer specializing in Python and microservices.",
                "city": "Rio de Janeiro",
                "country": "Brazil",
                "phone": "+55 21 91234-5678",
            },
            {
                "username": "carol",
                "email": "carol@example.com",
                "first_name": "Carol",
                "last_name": "Oliveira",
                "bio": "Product manager with a passion for user experience.",
                "city": "Belo Horizonte",
                "country": "Brazil",
            },
        ]

        for data in user_data:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                },
            )

            if created:
                user.set_password("password123")
                user.save()

                # Update profile
                profile = user.profile
                profile.bio = data.get("bio", "")
                profile.city = data.get("city", "")
                profile.country = data.get("country", "")
                profile.phone = data.get("phone", "")
                profile.save()

                users.append(user)
                self.stdout.write(f"  ✓ Created user: {user.username}")
            else:
                users.append(user)
                self.stdout.write(f"  → User exists: {user.username}")

        return users

    def create_categories(self):
        """
        Create sample categories with hierarchy.
        Cria categorias de exemplo com hierarquia.
        """
        self.stdout.write("Creating categories... / Criando categorias...")

        categories = []
        category_data = [
            {"name": "Electronics", "description": "Electronic devices and gadgets"},
            {
                "name": "Computers",
                "parent": "Electronics",
                "description": "Desktop and laptop computers",
            },
            {
                "name": "Smartphones",
                "parent": "Electronics",
                "description": "Mobile phones and tablets",
            },
            {"name": "Clothing", "description": "Apparel and fashion items"},
            {
                "name": "Men's Clothing",
                "parent": "Clothing",
                "description": "Clothing for men",
            },
            {
                "name": "Women's Clothing",
                "parent": "Clothing",
                "description": "Clothing for women",
            },
            {
                "name": "Home & Garden",
                "description": "Home improvement and garden supplies",
            },
            {"name": "Books", "description": "Physical and digital books"},
        ]

        parent_map = {}

        for data in category_data:
            parent_name = data.pop("parent", None)
            parent = parent_map.get(parent_name) if parent_name else None

            category, created = Category.objects.get_or_create(
                name=data["name"], defaults={**data, "parent": parent}
            )

            categories.append(category)
            parent_map[category.name] = category

            if created:
                self.stdout.write(f"  ✓ Created category: {category.name}")
            else:
                self.stdout.write(f"  → Category exists: {category.name}")

        return categories

    def create_tags(self):
        """
        Create sample tags with colors.
        Cria tags de exemplo com cores.
        """
        self.stdout.write("Creating tags... / Criando tags...")

        tags = []
        tag_data = [
            {"name": "New", "color": "#28a745"},
            {"name": "Popular", "color": "#007bff"},
            {"name": "Sale", "color": "#dc3545"},
            {"name": "Featured", "color": "#ffc107"},
            {"name": "Limited Edition", "color": "#6f42c1"},
            {"name": "Bestseller", "color": "#17a2b8"},
            {"name": "Eco-Friendly", "color": "#20c997"},
        ]

        for data in tag_data:
            tag, created = Tag.objects.get_or_create(name=data["name"], defaults=data)

            tags.append(tag)

            if created:
                self.stdout.write(f"  ✓ Created tag: {tag.name}")
            else:
                self.stdout.write(f"  → Tag exists: {tag.name}")

        return tags

    def create_products(self, users, categories, tags):
        """
        Create sample products.
        Cria produtos de exemplo.
        """
        self.stdout.write("Creating products... / Criando produtos...")

        products = []

        # Get specific categories for products
        electronics = next((c for c in categories if c.name == "Electronics"), None)
        computers = next((c for c in categories if c.name == "Computers"), None)
        smartphones = next((c for c in categories if c.name == "Smartphones"), None)
        books = next((c for c in categories if c.name == "Books"), None)

        product_data = [
            {
                "name": 'MacBook Pro 16"',
                "price": Decimal("2499.99"),
                "category": computers,
                "created_by": users[0] if users else None,
                "tags": [tags[0], tags[1]],  # New, Popular
            },
            {
                "name": "iPhone 15 Pro",
                "price": Decimal("999.99"),
                "category": smartphones,
                "created_by": users[0] if users else None,
                "tags": [tags[0], tags[5]],  # New, Bestseller
            },
            {
                "name": "Samsung Galaxy S24 Ultra",
                "price": Decimal("1199.99"),
                "category": smartphones,
                "created_by": users[1] if len(users) > 1 else None,
                "tags": [tags[0], tags[1]],  # New, Popular
            },
            {
                "name": "Dell XPS 15",
                "price": Decimal("1799.99"),
                "category": computers,
                "created_by": users[1] if len(users) > 1 else None,
                "tags": [tags[1], tags[3]],  # Popular, Featured
            },
            {
                "name": "Sony WH-1000XM5",
                "price": Decimal("399.99"),
                "category": electronics,
                "created_by": users[2] if len(users) > 2 else None,
                "tags": [tags[1], tags[5]],  # Popular, Bestseller
            },
            {
                "name": "Clean Code Book",
                "price": Decimal("42.99"),
                "category": books,
                "created_by": users[0] if users else None,
                "tags": [tags[5]],  # Bestseller
            },
            {
                "name": "The Pragmatic Programmer",
                "price": Decimal("45.99"),
                "category": books,
                "created_by": users[1] if len(users) > 1 else None,
                "tags": [tags[5]],  # Bestseller
            },
            {
                "name": 'iPad Pro 12.9"',
                "price": Decimal("1099.99"),
                "category": smartphones,
                "created_by": users[2] if len(users) > 2 else None,
                "tags": [tags[1], tags[3]],  # Popular, Featured
            },
            {
                "name": "Logitech MX Master 3S",
                "price": Decimal("99.99"),
                "category": electronics,
                "created_by": users[0] if users else None,
                "tags": [tags[1]],  # Popular
            },
            {
                "name": 'LG UltraWide Monitor 34"',
                "price": Decimal("599.99"),
                "category": electronics,
                "created_by": users[1] if len(users) > 1 else None,
                "tags": [tags[3]],  # Featured
            },
        ]

        for data in product_data:
            product_tags = data.pop("tags", [])

            product, created = Product.objects.get_or_create(
                name=data["name"], defaults=data
            )

            if created:
                product.tags.set(product_tags)
                products.append(product)
                self.stdout.write(f"  ✓ Created product: {product.name}")
            else:
                products.append(product)
                self.stdout.write(f"  → Product exists: {product.name}")

        return products
