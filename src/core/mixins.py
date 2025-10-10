# Custom Mixins - Core Application
# Mixins Customizados - Aplicação Core

"""
This module defines reusable mixins for Django views and models.

Model Mixins:
    - TimeStampedModelMixin: Auto-tracking of created_at/updated_at
    - SoftDeleteModelMixin: Soft delete with is_deleted flag
    - UserTrackingModelMixin: Track created_by/updated_by
    - PublishableModelMixin: Publish/unpublish functionality

View Mixins:
    - AdminRequiredMixin: Require staff permissions
    - SuperuserRequiredMixin: Require superuser permissions
    - VerifiedRequiredMixin: Require verified user profile
    - OwnerRequiredMixin: Require object ownership
    - SetOwnerOnCreateMixin: Auto-set owner on creation
    - MessageMixin: Auto-add success/error messages
    - PaginationMixin: Configurable pagination
    - AjaxResponseMixin: JSON responses for AJAX
    - ActiveOnlyQuerySetMixin: Filter to active records only

Este módulo define mixins reutilizáveis para views e modelos Django.

Mixins de Modelo:
    - TimeStampedModelMixin: Rastreamento automático de created_at/updated_at
    - SoftDeleteModelMixin: Soft delete com flag is_deleted
    - UserTrackingModelMixin: Rastreia created_by/updated_by
    - PublishableModelMixin: Funcionalidade de publicar/despublicar

Mixins de View:
    - AdminRequiredMixin: Requer permissões de staff
    - SuperuserRequiredMixin: Requer permissões de superusuário
    - VerifiedRequiredMixin: Requer perfil de usuário verificado
    - OwnerRequiredMixin: Requer propriedade do objeto
    - SetOwnerOnCreateMixin: Define owner automaticamente na criação
    - MessageMixin: Adiciona mensagens de sucesso/erro automaticamente
    - PaginationMixin: Paginação configurável
    - AjaxResponseMixin: Respostas JSON para AJAX
    - ActiveOnlyQuerySetMixin: Filtra apenas registros ativos

Examples:
    Model with timestamps and soft delete:
        class Article(TimeStampedModelMixin, SoftDeleteModelMixin):
            title = models.CharField(max_length=200)
            content = models.TextField()

    View requiring admin and auto-messages:
        class ArticleCreateView(AdminRequiredMixin, MessageMixin, CreateView):
            model = Article
            success_message = "Article created successfully!"

    Owner-restricted update view:
        class ArticleUpdateView(OwnerRequiredMixin, UpdateView):
            model = Article
            owner_field = 'author'
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Model Mixins / Mixins de Modelo


class TimeStampedModelMixin(models.Model):
    """
    Abstract base class with creation and modification timestamps.
    Classe base abstrata com timestamps de criação e modificação.

    Usage:
        class MyModel(TimeStampedModelMixin):
            name = models.CharField(max_length=100)

    Provides:
        - created_at: Auto-set on creation
        - updated_at: Auto-updated on save
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Timestamp when the record was created"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Timestamp when the record was last updated"),
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteModelMixin(models.Model):
    """
    Abstract base class with soft delete functionality.
    Classe base abstrata com funcionalidade de soft delete.

    Usage:
        class MyModel(SoftDeleteModelMixin):
            name = models.CharField(max_length=100)

        # Instead of instance.delete(), use:
        instance.soft_delete()

        # To restore:
        instance.restore()

    Provides:
        - is_deleted: Boolean flag for soft delete
        - deleted_at: Timestamp when deleted
        - soft_delete(): Mark as deleted
        - restore(): Restore deleted record
    """

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Is Deleted"),
        help_text=_("Indicates if the record is soft deleted"),
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Deleted At"),
        help_text=_("Timestamp when the record was deleted"),
    )

    class Meta:
        abstract = True

    def soft_delete(self):
        """Soft delete the record."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """Restore a soft deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class UserTrackingModelMixin(models.Model):
    """
    Abstract base class that tracks which user created/modified a record.
    Classe base abstrata que rastreia qual usuário criou/modificou um registro.

    Usage:
        class MyModel(UserTrackingModelMixin):
            name = models.CharField(max_length=100)

    Provides:
        - created_by: ForeignKey to User (who created)
        - updated_by: ForeignKey to User (who last updated)
    """

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name=_("Created By"),
        help_text=_("User who created this record"),
    )

    updated_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        verbose_name=_("Updated By"),
        help_text=_("User who last updated this record"),
    )

    class Meta:
        abstract = True


class PublishableModelMixin(models.Model):
    """
    Abstract base class for models that can be published/unpublished.
    Classe base abstrata para modelos que podem ser publicados/despublicados.

    Usage:
        class Article(PublishableModelMixin):
            title = models.CharField(max_length=200)

    Provides:
        - is_published: Boolean flag
        - published_at: Publication timestamp
        - publish(): Publish the record
        - unpublish(): Unpublish the record
    """

    is_published = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Is Published"),
        help_text=_("Indicates if the record is published"),
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Published At"),
        help_text=_("Timestamp when the record was published"),
    )

    class Meta:
        abstract = True

    def publish(self):
        """Publish the record."""
        if not self.is_published:
            self.is_published = True
            self.published_at = timezone.now()
            self.save(update_fields=["is_published", "published_at"])

    def unpublish(self):
        """Unpublish the record."""
        if self.is_published:
            self.is_published = False
            self.published_at = None
            self.save(update_fields=["is_published", "published_at"])


# View Mixins / Mixins de View


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin that requires user to be an admin (staff).
    Mixin que requer que o usuário seja um admin (staff).

    Usage:
        class MyView(AdminRequiredMixin, ListView):
            model = MyModel
    """

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, _("You must be an admin to access this page."))
        return redirect("home")


class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin that requires user to be a superuser.
    Mixin que requer que o usuário seja um superusuário.

    Usage:
        class MyView(SuperuserRequiredMixin, ListView):
            model = MyModel
    """

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, _("You must be a superuser to access this page."))
        return redirect("home")


class VerifiedRequiredMixin(LoginRequiredMixin):
    """
    Mixin that requires user to have a verified profile.
    Mixin que requer que o usuário tenha um perfil verificado.

    Usage:
        class MyView(VerifiedRequiredMixin, ListView):
            model = MyModel
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not hasattr(request.user, "profile") or not request.user.profile.is_verified:
            messages.warning(
                request,
                _(
                    "You must have a verified profile to access this page. "
                    "Please complete your profile and wait for verification."
                ),
            )
            return redirect("profile")

        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Mixin that requires user to be the owner of the object.
    Mixin que requer que o usuário seja o dono do objeto.

    Usage:
        class MyUpdateView(OwnerRequiredMixin, UpdateView):
            model = MyModel
            owner_field = 'user'  # Field that stores the owner

    Attributes:
        owner_field: Name of the field that contains the owner (default: 'user')
    """

    owner_field = "user"

    def test_func(self):
        obj = self.get_object()
        owner = getattr(obj, self.owner_field, None)
        return owner == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(
            self.request, _("You don't have permission to access this resource.")
        )
        return redirect("home")


class SetOwnerOnCreateMixin:
    """
    Mixin to automatically set the owner field when creating an object.
    Mixin para definir automaticamente o campo owner ao criar um objeto.

    Usage:
        class MyCreateView(SetOwnerOnCreateMixin, CreateView):
            model = MyModel
            fields = ['title', 'content']
            owner_field = 'created_by'

    Attributes:
        owner_field: Name of the field to set (default: 'created_by')
    """

    owner_field = "created_by"

    def form_valid(self, form):
        setattr(form.instance, self.owner_field, self.request.user)
        return super().form_valid(form)


class MessageMixin:
    """
    Mixin to add success/error messages to class-based views.
    Mixin para adicionar mensagens de sucesso/erro a views baseadas em classe.

    Usage:
        class MyView(MessageMixin, CreateView):
            model = MyModel
            success_message = "Item created successfully!"
            error_message = "Error creating item."
    """

    success_message = ""
    error_message = ""

    def form_valid(self, form):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.error_message:
            messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class PaginationMixin:
    """
    Mixin to add configurable pagination to list views.
    Mixin para adicionar paginação configurável a views de lista.

    Usage:
        class MyListView(PaginationMixin, ListView):
            model = MyModel
            default_page_size = 20
            max_page_size = 100

    Query Parameters:
        ?page_size=50 - Set custom page size
    """

    default_page_size = 10
    max_page_size = 100

    def get_paginate_by(self, queryset):
        """Get page size from query params or use default."""
        page_size = self.request.GET.get("page_size", self.default_page_size)

        try:
            page_size = int(page_size)
            return min(page_size, self.max_page_size)
        except (ValueError, TypeError):
            return self.default_page_size


class AjaxResponseMixin:
    """
    Mixin to return JSON responses for AJAX requests.
    Mixin para retornar respostas JSON para requisições AJAX.

    Usage:
        class MyView(AjaxResponseMixin, CreateView):
            model = MyModel
            fields = ['name']

            def get_ajax_data(self):
                return {'id': self.object.id, 'name': self.object.name}
    """

    def is_ajax(self):
        """Check if request is AJAX."""
        return self.request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def get_ajax_data(self):
        """Override this method to return custom AJAX response data."""
        return {"success": True}

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.is_ajax():
            from django.http import JsonResponse

            return JsonResponse(self.get_ajax_data())

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        if self.is_ajax():
            from django.http import JsonResponse

            return JsonResponse(
                {"success": False, "errors": form.errors.as_json()},
                status=400,
            )

        return response


# Queryset Mixins / Mixins de Queryset


class ActiveOnlyQuerySetMixin:
    """
    Mixin to filter queryset to only active records.
    Mixin para filtrar queryset apenas para registros ativos.

    Usage:
        class MyListView(ActiveOnlyQuerySetMixin, ListView):
            model = MyModel
            active_field = 'is_active'  # Field name to filter by

    Attributes:
        active_field: Name of the boolean field (default: 'is_active')
    """

    active_field = "is_active"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(**{self.active_field: True})
