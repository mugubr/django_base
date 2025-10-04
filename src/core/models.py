from django.db import models


class Product(models.Model):
    """
    Represents a product in the system.
    Representa um produto no sistema.
    """

    # name: The name of the product, limited to 100 characters.
    # name: O nome do produto, limitado a 100 caracteres.
    name = models.CharField(max_length=100)

    # price: The price of the product, with up to 10 digits
    # and 2 decimal places.
    # price: O preço do produto, com até 10 dígitos e 2 casas decimais.
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # created_at: Timestamp automatically set when the product is created.
    # created_at: Timestamp definido automaticamente quando o produto é criado.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the model, used in the Django admin.
        # Representação em string da model, usada no admin do Django.
        return self.name
