from rest_framework import generics
from .models import RobotAlert
from .serializers import RobotAlertSerializer
from django.views.generic import TemplateView
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RobotAlertCreateAPIView(generics.CreateAPIView):
    """
    Cria um novo alerta no sistema.

    Use este endpoint para registrar eventos relevantes do robô,
    como início de execução, término ou falhas durante o processo.
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
    Lista alertas do sistema, podendo filtrar por `created_at` com ?since=timestamp
    """
    serializer_class = RobotAlertSerializer

    def get_queryset(self):
        queryset = RobotAlert.objects.all().order_by("-created_at")
        since = self.request.query_params.get("since")

        if since:
            try:
                from django.utils.dateparse import parse_datetime
                since_dt = parse_datetime(since)
                if since_dt is None:
                    raise ValueError()
                queryset = queryset.filter(created_at__gt=since_dt)
            except ValueError:
                raise ValidationError({"since": "Formato de data inválido. Use formato ISO 8601."})

        return queryset


class AlertListView(TemplateView):
    template_name = "alerts/list.html"