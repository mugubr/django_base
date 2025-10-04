import logging

# It's a good practice to use loggers for output in tasks.
# É uma boa prática usar loggers para saídas em tarefas.
logger = logging.getLogger(__name__)


def notify_new_product(product_id, product_name):
    """
    A simple async task that simulates a notification for a new product.
    In a real project, this could send an email, a push notification,
    or call an external API.
    Uma tarefa assíncrona simples que simula uma notificação para um novo produto.
    Em um projeto real, isso poderia enviar um email, uma notificação push ou chamar
    uma API externa.
    """
    message = f"Novo produto cadastrado! ID: {product_id}, Nome: {product_name}"

    logger.info("--- STARTING ASYNC TASK ---")
    logger.info(message)
    logger.info("--- TASK COMPLETED ---")

    return message
