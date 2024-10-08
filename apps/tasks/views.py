from typing import Any, Dict
from django.shortcuts import redirect, get_object_or_404
from django.db.models.query import QuerySet
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.mixins import LoginRequiredMixin
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import read_file
from .serializer import TaskSerializer
from .models import Task
from apps.robots.models import Robot
from apps.items.models import Item
from apps.processes.models import Process
from apps.robots.tasks import periodic_task_check
from rest_framework.exceptions import  NotFound


class TaskViewSet(viewsets.ViewSet):
    """
    ViewSet para visualizar e gerenciar tarefas.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("task_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False, description="ID da tarefa."),
        ],
        responses={200: TaskSerializer(many=True)},
        operation_description="Obter tarefas de um robô específico ou uma tarefa específica pelo ID.",
        operation_summary="Listar Tarefas por Robô ou Tarefa Específica",
    )
    @action(detail=True, methods=['get'], url_path='tasks')
    def list_tasks(self, request, pk=None):
        """
        Lista as tarefas associadas a um robô específico ou retorna uma tarefa específica.
        """
        # Obtém o robot_id da URL (pk)
        try:
            robot = Robot.objects.get(pk=pk)
        except Robot.DoesNotExist:
            raise NotFound(detail="Robô não encontrado.")

        # Obtém o task_id dos parâmetros de query, se fornecido
        task_id = request.query_params.get('task_id')

        if task_id:
            # Se task_id for fornecido, retorna apenas a tarefa específica
            try:
                task = Task.objects.get(pk=task_id, robot_id=robot.id)
                serializer = TaskSerializer(task)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                raise NotFound(detail="Tarefa não encontrada para o robô fornecido.")
        
        # Se task_id não for fornecido, retorna todas as tarefas do robô
        tasks_with_items = Task.objects.filter(robot_id=robot.id).prefetch_related('item_set')
        serializer = TaskSerializer(tasks_with_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Novo status da tarefa'),
                'started_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Data e hora de início da tarefa'),
                'ended_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Data e hora de finalização da tarefa'),
                'shift_result': openapi.Schema(type=openapi.TYPE_STRING, description='Resultado da etapa Shift'),
                'sismama_result': openapi.Schema(type=openapi.TYPE_STRING, description='Resultado da etapa Sismama'),
                'stage': openapi.Schema(type=openapi.TYPE_STRING, description='Etapa atual da tarefa'),
            },
            required=['status'],  # Defina quais campos são obrigatórios, neste caso apenas 'status'
        ),
        responses={200: TaskSerializer()},
        operation_description="Atualizar uma tarefa específica, incluindo status, horários, resultados e estágio.",
        operation_summary="Atualizar Tarefa",
    )
    @action(detail=True, methods=['patch'], url_path='update-task')
    def update_task_status(self, request, pk=None):
        """
        Atualiza uma tarefa específica.
        """
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound(detail="Tarefa não encontrada.")

        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardListView(LoginRequiredMixin, ListView):
    """
    View da lista de tarefas do usuário.

    Esta view exibe uma lista de tarefas associadas ao usuário, juntamente
    com informações relevantes sobre o estado das tarefas, itens e robôs disponíveis.

    Requer que o usuário esteja autenticado.
    """
    login_url = 'login'
    template_name = 'home/tasks.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        """
        Obtém o conjunto de tarefas associadas ao usuário e as ordena pelo ID de forma decrescente.

        Retorna:
        - QuerySet: Conjunto de tarefas associadas ao usuário.
        """
        user = self.request.user
        paginate_by = int(self.request.GET.get('paginate_by', self.paginate_by))
        self.paginate_by = paginate_by
        return Task.objects.filter(user_id=user).order_by("-id")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Obtém os dados de contexto para o template.

        Retorna:
        - Dict[str, Any]: Dados de contexto para o template.
        """
        total_items = Item.objects.filter(task_id__user_id=self.request.user).count()
        available_robots = Robot.objects.filter(status='ACTIVE').count()
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context["available_robots"] = available_robots
        context['segment'] = 'tasks'
        context['processes'] = Process.objects.all()
        context['total_items'] = total_items
        return context

    def post(self, request, *args, **kwargs):
        """
        Processa uma solicitação POST para criar uma nova tarefa.

        Esta função trata do upload de um arquivo CSV, cria uma nova tarefa associada ao usuário e ao processo selecionado,
        e atribui um robô para a tarefa se possível. Se nenhum robô estiver disponível, habilita a verificação de robôs.

        Retorna:
        - HttpResponse: Redireciona para a página de tarefas após o processamento.
        """
        process_id = request.POST.get('process_id')
        if not process_id:
            # Retorne uma resposta de erro caso process_id não seja fornecido
            return redirect('tasks')

        process = get_object_or_404(Process, id=process_id)

        file = request.FILES.get('formFile')
        if not file:
            # Retorne uma resposta de erro caso o arquivo não seja fornecido
            return redirect('tasks')

        # Processa o arquivo
        assigned_robot = read_file(file, request.user, process)
        
        # Se não houver robô disponível, habilita a tarefa periódica
        if not assigned_robot:
            periodic_task_check.enabled = True
            periodic_task_check.save()

        # Redireciona para a página de tarefas após o processamento
        return redirect('tasks')

