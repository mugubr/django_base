from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello_api(request):
    """
    An example endpoint that returns a welcome message.
    Used to quickly test if the API is up and running.
    Um endpoint de exemplo que retorna uma mensagem de boas-vindas.
    Usado para testar rapidamente se a API está no ar e funcionando.
    """
    data = {"message": "Olá, API do Projeto Base Django!"}
    return Response(data, status=status.HTTP_200_OK)
