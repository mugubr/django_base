"""
Core Application Signal Handlers.

This module defines Django signal handlers for models in the core application.
Provides automatic profile creation, change tracking, logging, and async task
scheduling with robust error handling.

Handlers de Sinal da Aplicação Core.

Este módulo define handlers de sinal Django para modelos da aplicação core.
Provê criação automática de perfil, rastreamento de mudanças, logging e
agendamento de tarefas assíncronas com tratamento robusto de erros.

Signal Handlers / Handlers de Sinal:
    create_user_profile: Auto-creates UserProfile on User creation
    save_user_profile: Saves profile when User is saved
    product_pre_save_handler: Tracks changes before Product save
    schedule_product_notification: Schedules async notifications
    update_search_index: Updates search index (placeholder)
    product_post_delete_handler: Cleanup after Product deletion

Features / Recursos:
    - Automatic profile creation / Criação automática de perfil
    - Change tracking / Rastreamento de mudanças
    - Async task scheduling / Agendamento de tarefas assíncronas
    - Robust error handling / Tratamento robusto de erros
    - Comprehensive logging / Logging abrangente
    - Graceful degradation / Degradação graciosa

Important Notes / Notas Importantes:
    - Signal handlers NEVER raise exceptions that could break saves
    - All errors are logged but operations continue
    - Handlers nunca lançam exceções que possam quebrar saves
    - Todos os erros são logados mas operações continuam

Examples / Exemplos:
    # User creation automatically creates profile
    # Criação de usuário cria automaticamente perfil
    user = User.objects.create_user('john', 'john@example.com')
    # user.profile now exists / user.profile agora existe

    # Product price changes are tracked
    # Mudanças de preço de produto são rastreadas
    product.price = Decimal('99.99')
    product.save()  # Logs price change / Loga mudança de preço
"""

import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django_q.tasks import async_task

from .models import Product, UserProfile

User = get_user_model()

# Configure logger for this module
# Configura logger para este módulo
logger = logging.getLogger(__name__)


# User Profile Auto-Creation Signal
# Sinal de Auto-Criação de Perfil de Usuário


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a UserProfile when a new User is created.
    This ensures every user has an associated profile.

    Cria automaticamente um UserProfile quando um novo User é criado.
    Isso garante que todo usuário tenha um perfil associado.

    Args:
        sender: The User model class
        instance: The User instance that was saved
        created (bool): True if a new User was created
        **kwargs: Additional signal parameters
    """
    try:
        if created:
            UserProfile.objects.create(user=instance)
            logger.info(
                f"UserProfile created for user {instance.username} (ID: {instance.id})"
            )
    except Exception as e:
        # Don't let profile creation errors prevent user creation
        # Não deixe erros de criação de perfil prevenir criação de usuário
        logger.error(
            f"Failed to create UserProfile for user {instance.username} (ID: {instance.id}): {e}",
            exc_info=True,
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the UserProfile whenever the User is saved.
    Creates profile if it doesn't exist (fallback for edge cases).

    Salva o UserProfile sempre que o User é salvo.
    Cria perfil se não existir (fallback para casos extremos).

    Args:
        sender: The User model class
        instance: The User instance that was saved
        **kwargs: Additional signal parameters
    """
    try:
        # Try to save existing profile, create if doesn't exist
        # Tenta salvar perfil existente, cria se não existir
        if hasattr(instance, "profile"):
            instance.profile.save()
        else:
            # Edge case: profile doesn't exist, create it
            # Caso extremo: perfil não existe, cria
            UserProfile.objects.create(user=instance)
            logger.warning(
                f"UserProfile was missing for user {instance.username} (ID: {instance.id}), created now"
            )
    except Exception as e:
        logger.error(
            f"Error saving UserProfile for user {instance.username} (ID: {instance.id}): {e}",
            exc_info=True,
        )


# Pre-Save Signal Handlers
# Handlers de Sinal Pre-Save


@receiver(pre_save, sender=Product)
def product_pre_save_handler(sender, instance, **kwargs):
    """
    Signal handler executed BEFORE a Product is saved.
    Used for validation, data normalization, or logging changes.

    Handler de sinal executado ANTES de um Product ser salvo.
    Usado para validação, normalização de dados ou logging de mudanças.

    Args:
        sender: The model class (Product)
        instance: The actual Product instance being saved
        **kwargs: Additional signal parameters

    Use Cases:
        - Audit logging (track who changed what)
        - Data normalization (clean/format data)
        - Validation (additional checks beyond model validation)
        - Price change tracking
    """
    try:
        # Check if this is an update (instance already exists in DB)
        # Verifica se é uma atualização (instância já existe no BD)
        if instance.pk:
            try:
                # Get the old version from database
                # Obtém a versão antiga do banco de dados
                old_instance = Product.objects.get(pk=instance.pk)

                # Track price changes for audit log
                # Rastreia mudanças de preço para log de auditoria
                if old_instance.price != instance.price:
                    logger.info(
                        f"Product {instance.pk} price changed: "
                        f"{old_instance.price} -> {instance.price}"
                    )
                    # Here you could:
                    # - Create an audit log entry
                    # - Send notification to admins
                    # - Update price history table
                    #
                    # Aqui você poderia:
                    # - Criar entrada de log de auditoria
                    # - Enviar notificação para admins
                    # - Atualizar tabela de histórico de preços

                # Track status changes
                # Rastreia mudanças de status
                if old_instance.is_deleted != instance.is_deleted:
                    status_change = (
                        "activated" if instance.is_deleted else "deactivated"
                    )
                    logger.info(f"Product {instance.pk} {status_change}")

            except Product.DoesNotExist:
                # This shouldn't happen, but handle gracefully
                # Isso não deveria acontecer, mas trata graciosamente
                logger.warning(
                    f"Product {instance.pk} not found in pre_save signal. "
                    f"This may indicate a race condition."
                )

    except Exception as e:
        # CRITICAL: Never let signal errors break the save operation
        # CRÍTICO: Nunca deixe erros de sinal quebrar a operação de save
        logger.error(
            f"Error in product_pre_save_handler for product {instance.pk}: {e}",
            exc_info=True,  # Include full traceback
        )
        # Don't re-raise the exception - allow save to continue
        # Não relança a exceção - permite que save continue


# Post-Save Signal Handlers
# Handlers de Sinal Post-Save


@receiver(post_save, sender=Product)
def schedule_product_notification(sender, instance, created, **kwargs):
    """
    Schedules an async task to notify about product creation/update.
    Includes robust error handling to prevent task scheduling failures
    from breaking product saves.

    Agenda uma tarefa assíncrona para notificar sobre
    criação/atualização de produto.
    Inclui tratamento robusto de erros para prevenir
    falhas de agendamento de tarefas
    de quebrar saves de produtos.

    Args:
        sender: The model class (Product)
        instance: The Product instance that was saved
        created (bool): True if a new record was created, False if updated
        **kwargs: Additional signal parameters (raw, using, update_fields)

    Technical Details:
        - Uses Django Q for async task processing
        - Gracefully degrades if Django Q is unavailable
        - Logs all scheduling attempts for monitoring
        - Never raises exceptions that could break the save

    Detalhes Técnicos:
        - Usa Django Q para processamento de tarefas assíncronas
        - Degrada graciosamente se Django Q estiver indisponível
        - Loga todas tentativas de agendamento para monitoramento
        - Nunca lança exceções que possam quebrar o save
    """
    try:
        # Only schedule task for new products, not updates
        # Apenas agenda tarefa para novos produtos, não atualizações
        if created:
            logger.info(
                f"""Product {instance.id} created. Scheduling
                notification task..."""
            )

            try:
                # Schedule async task with Django Q
                # Agenda tarefa assíncrona com Django Q
                task_id = async_task(
                    "core.tasks.notify_new_product",
                    product_id=instance.id,
                    product_name=instance.name,
                    # Optional: Add task options
                    # Opcional: Adicionar opções da tarefa
                    # timeout=300,  # Task timeout in seconds
                    # q_options={
                    #     'group': 'product-notifications',
                    #     'ack_failure': True,
                    # }
                )

                logger.info(
                    f"Notification task scheduled successfully for product {instance.id}. "
                    f"Task ID: {task_id}"
                )

            except ImportError as e:
                # Django Q not installed or not available
                # Django Q não instalado ou não disponível
                logger.warning(
                    f"Could not schedule notification task for product {instance.id}: "
                    f"Django Q not available. Error: {e}"
                )
                # Application continues to work, just without background tasks
                # Aplicação continua funcionando, apenas sem tarefas em background

            except Exception as e:
                # Any other error in task scheduling (DB connection, etc.)
                # Qualquer outro erro no agendamento de tarefa
                # (conexão BD, etc.)
                logger.error(
                    f"Failed to schedule notification task for product {instance.id}: {e}",
                    exc_info=True,
                )
                # Don't re-raise - allow the product save to
                # complete successfully
                # Não relança - permite que o save do produto
                # complete com sucesso

        else:
            # Product was updated, not created
            # Produto foi atualizado, não criado
            logger.debug(f"Product {instance.id} updated (no notification scheduled)")

    except Exception as e:
        # Catch-all for any unexpected errors in the entire signal handler
        # Captura tudo para quaisquer erros inesperados em todo o
        # handler de sinal
        logger.error(
            f"Unexpected error in schedule_product_notification signal for "
            f"product {instance.id}: {e}",
            exc_info=True,
        )
        # CRITICAL: Never let signal errors prevent the save from completing
        # CRÍTICO: Nunca deixe erros de sinal prevenir o save de completar


@receiver(post_save, sender=Product)
def update_search_index(sender, instance, created, **kwargs):
    """
    Updates search index when a product is created or modified.
    (Placeholder for future integration with search engines like Elasticsearch)

    Atualiza índice de busca quando um produto é criado ou modificado.
    (Placeholder para futura integração com engines de busca como
    Elasticsearch)

    Args:
        sender: The model class (Product)
        instance: The Product instance that was saved
        created (bool): True if a new record was created
        **kwargs: Additional signal parameters
    """
    try:
        # Skip if this is a raw save (e.g., from fixtures)
        # Pula se é um save raw (ex: de fixtures)
        if kwargs.get("raw", False):
            logger.debug(
                f"""Skipping search index update for product {instance.id}
                (raw save)"""
            )
            return

        # Future: Integrate with search engine
        # Futuro: Integrar com engine de busca
        #
        # from elasticsearch_dsl import Index
        # index = Index('products')
        # document = ProductDocument(
        #     meta={'id': instance.id},
        #     name=instance.name,
        #     price=float(instance.price),
        #     is_deleted=instance.is_deleted,
        # )
        # document.save()

        logger.debug(
            f"Search index update placeholder executed for product {instance.id}"
        )

    except Exception as e:
        logger.error(
            f"Error updating search index for product {instance.id}: {e}",
            exc_info=True,
        )
        # Don't re-raise - search index is not critical for product creation
        # Não relança - índice de busca não é crítico para criação de produto


# Post-Delete Signal Handlers
# Handlers de Sinal Post-Delete


@receiver(post_delete, sender=Product)
def product_post_delete_handler(sender, instance, **kwargs):
    """
    Signal handler executed AFTER a Product is deleted.
    Used for cleanup, logging, or cascading deletes.

    Handler de sinal executado APÓS um Product ser deletado.
    Usado para limpeza, logging ou deletes em cascata.

    Args:
        sender: The model class (Product)
        instance: The Product instance that was deleted
        **kwargs: Additional signal parameters

    Note:
        In this project, we use soft delete (is_deleted=False) instead of
        hard delete, so this signal rarely fires. It's here for completeness.

    Nota:
        Neste projeto, usamos soft delete (is_deleted=False) ao invés de
        hard delete, então este sinal raramente dispara. Está
        aqui por completude.
    """
    try:
        logger.info(
            f"""Product {instance.id} ('{instance.name}') was
            permanently deleted"""
        )

        # Here you could:
        # - Delete associated files (images, documents)
        # - Update related records
        # - Send notifications
        # - Remove from search index
        #
        # Aqui você poderia:
        # - Deletar arquivos associados (imagens, documentos)
        # - Atualizar registros relacionados
        # - Enviar notificações
        # - Remover do índice de busca

        # Example: Delete product images
        # Exemplo: Deletar imagens do produto
        # if instance.image:
        #     instance.image.delete(save=False)

    except Exception as e:
        logger.error(
            f"Error in product_post_delete_handler for product {instance.id}: {e}",
            exc_info=True,
        )
        # Don't re-raise - cleanup errors shouldn't prevent deletion
        # Não relança - erros de limpeza não devem prevenir deleção


# Signal Connection Status Logging
# Logging de Status de Conexão de Sinais

logger.info("Signal handlers registered successfully")
logger.debug(
    "Active signal handlers: "
    "create_user_profile, "
    "save_user_profile, "
    "product_pre_save_handler, "
    "schedule_product_notification, "
    "update_search_index, "
    "product_post_delete_handler"
)
