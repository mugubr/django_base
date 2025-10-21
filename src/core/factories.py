"""
Test Data Factories for Core Models.
Fábricas de Dados de Teste para Modelos Core.

This module provides Factory Boy factories for generating test data.
Uses Faker for realistic dummy data generation.

Este módulo fornece fábricas Factory Boy para gerar dados de teste.
Usa Faker para geração de dados dummy realistas.

Usage / Uso:
    from core.factories import UserFactory, ProductFactory

    user = UserFactory()
    product = ProductFactory(created_by=user)
"""

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from faker import Faker

from .models import Category, Product, Tag, UserProfile

User = get_user_model()
fake = Faker(["pt_BR", "en_US"])


class UserFactory(DjangoModelFactory):
    """
    Factory for User model.
    Fábrica para modelo User.
    """

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        """
        Set password after user creation.
        Define senha após criação do usuário.
        """
        if create:
            obj.set_password(extracted or "testpass123")
            obj.save()


class UserProfileFactory(DjangoModelFactory):
    """
    Factory for UserProfile model.
    Fábrica para modelo UserProfile.
    """

    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("text", max_nb_chars=200)
    phone = factory.Faker("phone_number", locale="pt_BR")
    location = factory.Faker("city")
    website = factory.Faker("url")


class CategoryFactory(DjangoModelFactory):
    """
    Factory for Category model.
    Fábrica para modelo Category.
    """

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker("text", max_nb_chars=100)
    is_deleted = False
    parent = None
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SelfAttribute("created_by")


class TagFactory(DjangoModelFactory):
    """
    Factory for Tag model.
    Fábrica para modelo Tag.
    """

    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"tag{n}")
    created_by = factory.SubFactory(UserFactory)


class ProductFactory(DjangoModelFactory):
    """
    Factory for Product model.
    Fábrica para modelo Product.
    """

    class Meta:
        model = Product

    name = factory.Faker("catch_phrase")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    stock = factory.Faker("random_int", min=0, max=1000)
    is_deleted = False
    category = factory.SubFactory(CategoryFactory)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SelfAttribute("created_by")

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """
        Add tags after product creation.
        Adiciona tags após criação do produto.
        """
        if not create:
            return

        if extracted:
            for tag in extracted:
                obj.tags.add(tag)
        else:
            # Create 2-5 random tags / Cria 2-5 tags aleatórias
            for _ in range(fake.random_int(min=2, max=5)):
                obj.tags.add(TagFactory())
