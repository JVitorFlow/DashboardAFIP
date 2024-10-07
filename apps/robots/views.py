from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializer import RobotSerializer
from .models import Robot
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

class RobotViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, editar e gerenciar robôs.
    """
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: RobotSerializer()}
    )
    def retrieve(self, request, pk=None):
        """
        Obtém informações sobre um robô pelo seu ID.
        """
        try:
            robot = Robot.objects.get(pk=pk)
        except Robot.DoesNotExist:
            raise NotFound(detail="Robô não encontrado.")

        serializer = RobotSerializer(robot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, description="Status do robô.", type=openapi.TYPE_STRING)
        ],
        request_body=RobotSerializer,
        responses={200: 'Sucesso', 404: 'Não Encontrado'},
    )
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Edita o estado de um robô pelo seu ID.
        """
        try:
            robot = Robot.objects.get(pk=pk)
        except Robot.DoesNotExist:
            raise NotFound(detail="Robô não encontrado.")

        serializer = RobotSerializer(robot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
