from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .models import ShiftData
from .serializer import ShiftDataSerializer
from drf_yasg import openapi

class ShiftDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet para criar, listar, editar e deletar ShiftData.
    """
    queryset = ShiftData.objects.all()
    serializer_class = ShiftDataSerializer

    @swagger_auto_schema(
        operation_description="Listar todos os registros de ShiftData.",
        operation_summary="Lista todos os ShiftData",
        responses={200: ShiftDataSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """
        Lista todos os registros de ShiftData.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Criar um novo registro de ShiftData.",
        operation_summary="Cria um novo ShiftData",
        request_body=ShiftDataSerializer,
        responses={201: ShiftDataSerializer},
    )
    def create(self, request, *args, **kwargs):
        """
        Cria um novo ShiftData.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Recuperar um ShiftData específico pelo ID.",
        operation_summary="Recuperar ShiftData por ID",
        responses={200: ShiftDataSerializer, 404: 'Not Found'},
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retorna um ShiftData específico pelo ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualizar completamente um ShiftData específico pelo ID.",
        operation_summary="Atualizar ShiftData",
        request_body=ShiftDataSerializer,
        responses={200: ShiftDataSerializer, 404: 'Not Found'},
    )
    def update(self, request, *args, **kwargs):
        """
        Atualiza um ShiftData específico pelo ID.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualizar parcialmente um ShiftData específico pelo ID.",
        operation_summary="Atualização parcial de ShiftData",
        request_body=ShiftDataSerializer,
        responses={200: ShiftDataSerializer, 404: 'Not Found'},
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente um ShiftData específico pelo ID.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Deletar um ShiftData específico pelo ID.",
        operation_summary="Deletar ShiftData",
        responses={204: 'No Content', 404: 'Not Found'},
    )
    def destroy(self, request, *args, **kwargs):
        """
        Deleta um ShiftData específico pelo ID.
        """
        return super().destroy(request, *args, **kwargs)
