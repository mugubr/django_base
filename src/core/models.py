"""
Ormar models for the core app.
Migrated from Django ORM to Ormar for better async support.
"""

import ormar
from django.conf import settings


class BaseMeta(ormar.ModelMeta):
    """Base metadata configuration for all Ormar models."""

    metadata = settings.metadata
    database = settings.database


class User(ormar.Model):
    """User model using Ormar ORM."""

    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True)
    email: str = ormar.String(max_length=255, unique=True)
    first_name: str = ormar.String(max_length=100, nullable=True)
    last_name: str = ormar.String(max_length=100, nullable=True)
    is_active: bool = ormar.Boolean(default=True)
    created_at = ormar.DateTime(server_default="now()")


class Post(ormar.Model):
    """Post model using Ormar ORM with foreign key to User."""

    class Meta(BaseMeta):
        tablename = "posts"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=200)
    content: str = ormar.Text()
    author = ormar.ForeignKey(User, related_name="posts")
    published: bool = ormar.Boolean(default=False)
    created_at = ormar.DateTime(server_default="now()")
    updated_at = ormar.DateTime(server_default="now()")
