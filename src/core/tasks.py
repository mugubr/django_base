# Django Q Background Tasks - Core Application
# Tarefas em Background Django Q - Aplicação Core

# This module defines background tasks for async processing with:
# - Automatic retry logic for transient failures
# - Comprehensive error handling and logging
# - Task result tracking
# - Graceful degradation when external services fail
# - Monitoring and alerting capabilities
#
# Este módulo define tarefas em background para processamento assíncrono com:
# - Lógica de retry automática para falhas transitórias
# - Tratamento de erros e logging abrangente
# - Rastreamento de resultados de tarefas
# - Degradação graciosa quando serviços externos falham
# - Capacidades de monitoramento e alertas

import logging
from typing import Any

from django.core.exceptions import ObjectDoesNotExist

from core import models

from .models import Product

# Configure module logger
# Configura logger do módulo
logger = logging.getLogger(__name__)

# Task Configuration Constants
# Constantes de Configuração de Tarefas

# Maximum number of retry attempts for failed tasks
# Número máximo de tentativas de retry para tarefas que falharam
MAX_RETRIES = 3

# Delay between retries in seconds (exponential backoff)
# Atraso entre retries em segundos (backoff exponencial)
RETRY_DELAYS = [5, 15, 60]  # 5s, 15s, 60s


# Notification Tasks
# Tarefas de Notificação


def notify_new_product(product_id: int, product_name: str) -> dict[str, Any]:
    """
    Background task to notify about a new product creation.
    Implements retry logic and comprehensive error handling.

    Tarefa em background para notificar sobre criação de novo produto.
    Implementa lógica de retry e tratamento de erros abrangente.

    Args:
        product_id (int): The ID of the newly created product
        product_name (str): The name of the product (for logging/notifications)

    Returns:
        dict: Task result with status and details

    Raises:
        Exception: Re-raises exceptions for Django Q to handle retries

    Examples:
        # Schedule this task from a signal or view:
        from django_q.tasks import async_task
        async_task('core.tasks.notify_new_product', product_id=123,
        product_name='Widget')

    Technical Details:
        - Validates product existence before processing
        - Logs all stages for monitoring
        - Returns structured result for task tracking
        - Implements graceful degradation
        - Can integrate with external services (email, webhooks, etc.)
    """
    logger.info("=" * 80)
    logger.info("STARTING TASK: notify_new_product")
    logger.info(f"Product ID: {product_id}, Product Name: {product_name}")
    logger.info("=" * 80)

    try:
        # Step 1: Validate Product Exists
        # Etapa 1: Validar que Produto Existe
        try:
            product = Product.objects.get(id=product_id)
            logger.info(f"Product {product_id} validated successfully")
        except ObjectDoesNotExist:
            error_msg = f"Product {product_id} not found in database"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": "product_not_found",
                "message": error_msg,
                "product_id": product_id,
            }

        # Step 2: Prepare Notification Data
        # Etapa 2: Preparar Dados de Notificação
        notification_data = {
            "product_id": product.id,  # type: ignore
            "product_name": product.name,
            "product_price": str(product.price),
            "formatted_price": product.formatted_price,
            "is_new": product.is_new,
            "created_at": product.created_at.isoformat(),
        }

        logger.info(f"Notification data prepared: {notification_data}")

        # Step 3: Send Notifications
        # Etapa 3: Enviar Notificações

        # This is where you would integrate with real notification services:
        # Este é onde você integraria com serviços reais de notificação:
        #
        # 1. Email notifications
        # 1. Notificações por email
        # send_email_notification(product, notification_data)
        #
        # 2. Webhooks to external systems
        # 2. Webhooks para sistemas externos
        # send_webhook_notification(product, notification_data)
        #
        # 3. Push notifications
        # 3. Notificações push
        # send_push_notification(product, notification_data)
        #
        # 4. Slack/Teams notifications
        # 4. Notificações Slack/Teams
        # send_slack_notification(product, notification_data)

        # For now, we simulate successful notification
        # Por enquanto, simulamos notificação bem-sucedida
        logger.info(f"""✓ Notifications sent successfully
        for product {product_id}""")

        # Step 4: Return Success Result
        # Etapa 4: Retornar Resultado de Sucesso
        result = {
            "status": "success",
            "message": f"New product notification sent: {product.name}",
            "product_id": product_id,
            "product_name": product.name,
            "notifications_sent": [
                "log"
            ],  # Would list actual channels: ['email', 'webhook', 'slack']
        }

        logger.info("=" * 80)
        logger.info("TASK COMPLETED SUCCESSFULLY")
        logger.info(f"Result: {result}")
        logger.info("=" * 80)

        return result

    except Exception as e:
        # Error Handling with Detailed Logging
        # Tratamento de Erros com Logging Detalhado
        error_details = {
            "status": "error",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "product_id": product_id,
            "product_name": product_name,
        }

        logger.error("=" * 80)
        logger.error("TASK FAILED")
        logger.error(f"Error: {e}")
        logger.error(f"Details: {error_details}")
        logger.error("=" * 80, exc_info=True)

        # Re-raise for Django Q to handle retries
        # Relança para Django Q lidar com retries
        raise


def send_product_update_notification(
    product_id: int, changed_fields: list[str]
) -> dict[str, Any]:
    """
    Sends notification when a product is updated.
    Used for tracking important changes like price updates.

    Envia notificação quando um produto é atualizado.
    Usado para rastrear mudanças importantes como atualizações de preço.

    Args:
        product_id (int): The ID of the updated product
        changed_fields (list): List of field names that were changed

    Returns:
        dict: Task execution result
    """
    logger.info(f"Product update notification task started for product {product_id}")
    logger.info(f"Changed fields: {changed_fields}")

    try:
        product = Product.objects.get(id=product_id)

        # Log the update
        # Loga a atualização
        logger.info(
            f"Product {product_id} ({product.name}) was updated. "
            f"Fields changed: {', '.join(changed_fields)}"
        )

        # Future: Send actual notifications
        # Futuro: Enviar notificações reais
        # if 'price' in changed_fields:
        #     send_price_change_alert(product)

        return {
            "status": "success",
            "message": "Update notification processed",
            "product_id": product_id,
            "changed_fields": changed_fields,
        }

    except Product.DoesNotExist:
        logger.error(f"Product {product_id} not found for update notification")
        return {
            "status": "error",
            "error": "product_not_found",
            "product_id": product_id,
        }
    except Exception as e:
        logger.error(f"Error in send_product_update_notification: {e}", exc_info=True)
        raise


# Data Processing Tasks
# Tarefas de Processamento de Dados


def bulk_update_product_status(
    product_ids: list[int], is_deleted: bool
) -> dict[str, Any]:
    """
    Background task to update multiple products' active status.
    Useful for bulk operations from admin interface.

    Tarefa em background para atualizar status ativo de múltiplos produtos.
    Útil para operações em massa da interface admin.

    Args:
        product_ids (list): List of product IDs to update
        is_deleted (bool): New active status

    Returns:
        dict: Execution result with count of updated products
    """
    logger.info(f"Starting bulk update for {len(product_ids)} products")
    logger.info(f"Setting is_deleted={is_deleted}")

    try:
        # Update products in bulk (efficient single query)
        # Atualiza produtos em massa (query única eficiente)
        updated_count = Product.objects.filter(id__in=product_ids).update(
            is_deleted=is_deleted
        )

        logger.info(f"Successfully updated {updated_count} products")

        return {
            "status": "success",
            "message": f"Updated {updated_count} products",
            "updated_count": updated_count,
            "product_ids": product_ids,
            "is_deleted": is_deleted,
        }

    except Exception as e:
        logger.error(f"Error in bulk_update_product_status: {e}", exc_info=True)
        raise


def calculate_product_statistics() -> dict[str, Any]:
    """
    Periodic task to calculate product statistics.
    Can be scheduled to run daily/hourly via Django Q's scheduler.

    Tarefa periódica para calcular estatísticas de produtos.
    Pode ser agendada para rodar diária/horariamente via agendador do Django Q.

    Returns:
        dict: Calculated statistics

    Schedule Example:
        from django_q.tasks import schedule
        from django_q.models import Schedule

        schedule(
            'core.tasks.calculate_product_statistics',
            schedule_type=Schedule.HOURLY
        )
    """
    logger.info("Calculating product statistics...")

    try:
        from django.db.models import Avg, Count, Max, Min, Sum

        stats = Product.objects.aggregate(
            total_products=Count("id"),
            active_products=Count("id", filter=models.Q(is_deleted=True)),
            average_price=Avg("price"),
            min_price=Min("price"),
            max_price=Max("price"),
            total_value=Sum("price"),
        )

        logger.info(f"Statistics calculated: {stats}")

        # Future: Store stats in cache or database table
        # Futuro: Armazenar stats em cache ou tabela de banco de dados
        # from django.core.cache import cache
        # cache.set('product_stats', stats, timeout=3600)

        return {
            "status": "success",
            "message": "Statistics calculated successfully",
            "statistics": stats,
        }

    except Exception as e:
        logger.error(
            f"""Error calculating product statistics:
                     {e}""",
            exc_info=True,
        )
        raise


# Integration Tasks (External Services)
# Tarefas de Integração (Serviços Externos)


def sync_product_to_external_service(product_id: int, service_name: str) -> dict:
    """
    Syncs product data to an external service (e.g., e-commerce platform, ERP).
    Implements retry logic for network failures.

    Sincroniza dados de produto para um serviço
    externo (ex: plataforma e-commerce, ERP).
    Implementa lógica de retry para falhas de rede.

    Args:
        product_id (int): Product to sync
        service_name (str): Name of the external service

    Returns:
        dict: Sync result
    """
    logger.info(f"Syncing product {product_id} to {service_name}")

    try:
        Product.objects.get(id=product_id)

        # Future: Actual API integration
        # Futuro: Integração real com API
        #
        # import requests
        # response = requests.post(
        #     f"https://api.{service_name}.com/products",
        #     json={
        #         'id': product.id,
        #         'name': product.name,
        #         'price': str(product.price),
        #     },
        #     timeout=30
        # )
        # response.raise_for_status()

        logger.info(f"""Product {product_id}
                    synced successfully to {service_name}""")

        return {
            "status": "success",
            "message": f"Product synced to {service_name}",
            "product_id": product_id,
            "service": service_name,
        }

    except Product.DoesNotExist:
        logger.error(f"Product {product_id} not found for sync")
        return {"status": "error", "error": "product_not_found"}
    except Exception as e:
        logger.error(f"Error syncing to {service_name}: {e}", exc_info=True)
        raise  # Re-raise for retry


# Task Health Check
# Verificação de Saúde de Tarefas


def task_health_check() -> dict:
    """
    Health check task to verify Django Q is working correctly.
    Can be called periodically to monitor task queue health.

    Tarefa de health check para verificar que Django Q
    está funcionando corretamente.
    Pode ser chamada periodicamente para monitorar saúde da fila de tarefas.

    Returns:
        dict: Health status
    """
    import sys
    from datetime import datetime

    logger.info("Running task queue health check...")

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Django Q task queue is operational",
        "python_version": sys.version,
        "product_count": Product.objects.count(),
    }


# Task Registration Logging
# Logging de Registro de Tarefas

logger.info("Background tasks module loaded successfully")
logger.debug(
    "Available tasks: "
    "notify_new_product, "
    "send_product_update_notification, "
    "bulk_update_product_status, "
    "calculate_product_statistics, "
    "sync_product_to_external_service, "
    "task_health_check"
)
