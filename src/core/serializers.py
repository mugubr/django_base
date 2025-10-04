from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    It converts Product model instances to JSON format and vice-versa.
    Serializador para o modelo Product.
    Ele converte instâncias do modelo Product para o formato JSON e vice-versa.
    """

    class Meta:
        # model: The model that this serializer is based on
        # model: O modelo no qual este serializador é baseado
        model = Product

        # fields: The list of fields from the model to be included
        # in the representation
        # fields: A lista de campos do modelo a serem incluídos
        # na representação
        fields = ["id", "name", "price", "created_at"]
