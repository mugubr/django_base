from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello_api(request):
    """
    Um endpoint de exemplo que retorna uma mensagem de boas-vindas.
    """
    data = {"message": "Hello!"}
    return Response(data, status=status.HTTP_200_OK)
