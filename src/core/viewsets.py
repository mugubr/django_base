from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Endpoint da API que permite que produtos sejam visualizados ou editados.
    Este ViewSet provê automaticamente as ações `list`, `create`, `retrieve`,
    `update` e `destroy`.
    """

    # queryset: Defines the collection of objects that will
    # be available for this view.
    # queryset: Define a coleção de objetos que estará disponível
    # para esta view.
    queryset = Product.objects.all().order_by("-created_at")

    # serializer_class: Indicates the serializer that should be
    # used for validating
    # and deserializing input, and for serializing output.
    # serializer_class: Indica o serializador que deve ser usado para validar
    # e desserializar a entrada, e para serializar a saída.
    serializer_class = ProductSerializer
