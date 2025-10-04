from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import async_task

from .models import Product


# The @receiver decorator connects this function to a signal.
# O decorador @receiver conecta esta função a um sinal.
@receiver(post_save, sender=Product)
def schedule_product_notification(sender, instance, created, **kwargs):
    """
    Schedules an async task to notify about a new product.
    This function is triggered every time a Product instance is saved.
    Agenda uma tarefa assíncrona para notificar sobre um novo produto.
    Esta função é disparada toda vez que uma instância de Product é salva.
    """
    # We only want to run the task if the object was just created.
    # Queremos rodar a tarefa apenas se o objeto acabou de ser criado.
    if created:
        # Calls the 'notify_new_product' function from 'core.tasks' asynchronously.
        # Chama a função 'notify_new_product' de 'core.tasks' de forma assíncrona.
        async_task(
            "core.tasks.notify_new_product",
            product_id=instance.id,
            product_name=instance.name,
        )
