from typing import Any, Dict
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from apps.robots.models import Robot
from apps.items.models import Item
from apps.tasks.models import Task
from .serializer import ItemSerializer
from apps.api.utils import token_login, check_id, check_if_can_change_status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication


class ItemAPIView(APIView):
    """
    Visualizar para editar o estado de um item.

    Esta visualização permite editar o estado de um item usando o 'robot_id'
    e parâmetros 'item_id'.

    Atributos:
        authentication_classes (lista): Lista de classes de autenticação
        aplicado à vista.
        permission_classes (lista): Lista de classes de permissão aplicadas
        para a vista.
    """
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("robot_id", openapi.IN_QUERY, description="ID do robô.", type=openapi.TYPE_INTEGER),
            openapi.Parameter("item_id", openapi.IN_QUERY, description="ID do item.", type=openapi.TYPE_INTEGER),
            openapi.Parameter("status", openapi.IN_QUERY, description="novo status da tarefa.", type=openapi.TYPE_STRING),
            openapi.Parameter("item__started_at", openapi.IN_QUERY, description="Data e hora de início (formato: AAAA-MM-DD HH:MM:SS).", type=openapi.TYPE_STRING),
            openapi.Parameter("item__ended_at", openapi.IN_QUERY, description="Data e hora de término (formato: AAAA-MM-DD HH:MM:SS).", type=openapi.TYPE_STRING),
            openapi.Parameter("item__observation", openapi.IN_QUERY, description="Observação do item.", type=openapi.TYPE_STRING),
        ],
        operation_description="Esquema personalizado para ItemAPIView"
    )
    def patch(self, request):
        """
        Edita o estado de um item usando os parâmetros 'robot_id' e 'item_id'.

        Parâmetros:
        - robot_id (int): ID do robô associado ao item.
        - item_id (int): ID do item a ser editado.
        - status (str): Status do item a ser editado.

        Retorna:
        Response: Resposta HTTP com o resultado da operação.

        Autenticação:
        - Token Bearer:
            Um token de API válido deve ser fornecido no cabeçalho 'Authorization'.
            Exemplo: Authorization: Token XXXX-XXXX-XXXX-XXXX
        """
        robot_id = request.data.get('robot_id')
        item_id = request.data.get('item_id')

        # Verifique se os IDs fornecidos são válidos
        if not robot_id or not item_id:
            return Response({'detail': 'IDs inválidos.'}, status=status.HTTP_400_BAD_REQUEST)

        check_id(robot_id, item_id)

        try:
            Robot.objects.get(id=robot_id)
            item = Item.objects.get(id=item_id)
        except (Robot.DoesNotExist, Item.DoesNotExist):
            return Response({'detail': 'Robô ou item não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se pode alterar o status do item
        check_if_can_change_status(item)

        # Serializa e atualiza os dados
        serializer = ItemSerializer(instance=item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemListView(LoginRequiredMixin, ListView):
    """
    View to display the list of items associated with a task.
    """
    login_url = 'login'
    template_name = 'home/items.html'

    def dispatch(self, request, *args: Any, **kwargs: Any):
        """
        Verifies if the user has permissions to access the view.

        Parameters:
        - request (HttpRequest): The incoming HTTP request.
        - args: Positional arguments.
        - kwargs: Keyword arguments.

        Returns:
        HttpResponse: HTTP response that redirects to the tasks page
        or allows access to the view.
        """
        task_id = self.kwargs['task_id']
        self.task = get_object_or_404(Task, id=task_id)
        if request.user != self.task.user_id:
            return redirect(reverse('tasks'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        """
    Obtains the set of items associated with the task.

    Returns:
    QuerySet: Set of items filtered by the task and sorted by ID
    in descending order.
    """
        return Item.objects.filter(task_id=self.task).order_by("-id")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Obtains the context data for the template.

        Returns:
        dict: Dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        context['segment'] = 'items'
        return context
