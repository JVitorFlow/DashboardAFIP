from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializer import RobotSerializer
from .models import Robot
from apps.api.utils import token_login, check_id


class RobotAPIView(APIView):
    """
    Visualize para recuperar e editar informações sobre robôs.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: RobotSerializer()},
    )

    def get(self, request, robot_id) -> Response:
        """
        Obtém informações sobre um robô pelo seu ID.
        """
        check_id(robot_id)
        try:
            robot = Robot.objects.get(id=robot_id)
        except Robot.DoesNotExist:
            return Response({'detail': 'Robô não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RobotSerializer(instance=robot)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('robot_id', openapi.IN_QUERY, description="ID do robô.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('status', openapi.IN_QUERY, description="Status do robô.", type=openapi.TYPE_STRING)
        ],
        request_body=RobotSerializer,
        responses={200: 'Sucesso', 404: 'Não Encontrado'},
    )

    def patch(self, request, robot_id) -> Response:
        """
        Edita o estado de um robô pelo seu ID.
        """
        check_id(robot_id)
        try:
            robot = Robot.objects.get(id=robot_id)
        except Robot.DoesNotExist:
            return Response({'detail': 'Robô não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RobotSerializer(instance=robot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)