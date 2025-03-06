from rest_framework import generics
from .models import RobotAlert
from .serializers import RobotAlertSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RobotAlertCreateAPIView(generics.CreateAPIView):
    """
    API endpoint para registrar um alerta de robô.
    Exemplo de uso:
      - alert_type: "start" para notificar que o robô está iniciando;
      - alert_type: "finish" para notificar que o robô terminou a execução;
      - alert_type: "error" para notificar um erro.
    """
    queryset = RobotAlert.objects.all()
    serializer_class = RobotAlertSerializer

    @swagger_auto_schema(
        operation_description="Cria um novo alerta para um robô.",
        request_body=RobotAlertSerializer,
        responses={
            201: openapi.Response('Alerta criado com sucesso', RobotAlertSerializer),
            400: "Requisição inválida",
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RobotAlertListAPIView(generics.ListAPIView):
    """
    API endpoint para listar os alertas registrados.
    Pode ser filtrado por robô, tipo de alerta, data, etc. (se necessário).
    """
    queryset = RobotAlert.objects.all().order_by("-created_at")
    serializer_class = RobotAlertSerializer

    @swagger_auto_schema(
        operation_description="Lista todos os alertas de robô cadastrados.",
        responses={
            200: openapi.Response('Lista de alertas', RobotAlertSerializer(many=True)),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
