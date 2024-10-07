from typing import Any, Dict
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from apps.robots.models import Robot
from collections import defaultdict
from apps.items.models import Item
from apps.tasks.models import Task
from .serializer import TaskSummarySerializer, ItemSerializer
from apps.api.utils import check_id, check_if_can_change_status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound

class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, editar e gerenciar itens.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Listar todos os itens cadastrados.",
        operation_summary="Listar Itens"
    )
    def list(self, request, *args, **kwargs):
        """
        Listar todos os itens cadastrados no sistema.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Criar um novo item no sistema.",
        operation_summary="Criar Item"
    )
    def create(self, request, *args, **kwargs):
        """
        Criar um novo item no sistema.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obter detalhes de um item específico pelo ID.",
        operation_summary="Detalhar Item"
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Obter detalhes de um item específico pelo ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualizar completamente um item específico pelo ID.",
        operation_summary="Atualizar Item"
    )
    def update(self, request, *args, **kwargs):
        """
        Atualizar completamente um item específico pelo ID.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualizar parcialmente um item específico pelo ID.",
        operation_summary="Atualizar Parcialmente Item"
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Atualizar parcialmente um item específico pelo ID.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Deletar um item específico pelo ID.",
        operation_summary="Deletar Item"
    )
    def destroy(self, request, *args, **kwargs):
        """
        Deletar um item específico pelo ID.
        """
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Listar todos os itens pendentes com status 'CREATED'.",
        operation_summary="Listar Itens Pendentes"
    )
    @action(detail=False, methods=['get'], url_path='pending')
    def list_pending(self, request):
        """
        Lista todos os itens pendentes que precisam ser processados pelo RPA.
        """
        # Filtra apenas os itens com status "CREATED"
        pending_items = Item.objects.filter(status="CREATED")

        # Caso não existam itens pendentes, retorna uma resposta clara
        if not pending_items.exists():
            return Response(
                {"detail": "Nenhum item pendente encontrado."},
                status=status.HTTP_200_OK
            )
                
        # Organiza os itens por tarefa usando um dicionário
        tasks_dict = defaultdict(list)
        for item in pending_items:
            tasks_dict[item.task_id].append(item)

        response_data = []
        for task, items in tasks_dict.items():
            # Serializa os dados da tarefa usando o resumo da tarefa
            task_data = TaskSummarySerializer(task).data
            task_data['items'] = ItemSerializer(items, many=True).data
            response_data.append(task_data)

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Atualizar o status de um item pelo seu ID e pelo `robot_id` associado.",
        operation_summary="Atualizar Status do Item",
        manual_parameters=[
            openapi.Parameter("robot_id", openapi.IN_QUERY, description="ID do robô.", type=openapi.TYPE_INTEGER),
            openapi.Parameter("status", openapi.IN_QUERY, description="Novo status do item.", type=openapi.TYPE_STRING),
            openapi.Parameter("item__started_at", openapi.IN_QUERY, description="Data e hora de início (formato: AAAA-MM-DD HH:MM:SS).", type=openapi.TYPE_STRING),
            openapi.Parameter("item__ended_at", openapi.IN_QUERY, description="Data e hora de término (formato: AAAA-MM-DD HH:MM:SS).", type=openapi.TYPE_STRING),
        ]
    )
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Edita o estado de um item pelo seu ID e o `robot_id` associado.

        Parâmetros:
        - robot_id (int): ID do robô associado ao item.
        - status (str): Novo status do item.

        Retorna:
        - Response: Resposta HTTP com o resultado da operação.
        """
        robot_id = request.data.get('robot_id')
        if not robot_id:
            return Response({'detail': 'robot_id ausente ou inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        check_id(robot_id, pk)

        try:
            robot = Robot.objects.get(id=robot_id)
            item = Item.objects.get(id=pk)
        except (Robot.DoesNotExist, Item.DoesNotExist):
            raise NotFound(detail="Robô ou item não encontrado.")

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
