from typing import Any, Dict
from django.shortcuts import redirect, get_object_or_404
from django.db.models.query import QuerySet
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from .utils import read_file
from .serializer import TaskSerializer, TaskWithItemsSerializer
from .models import Task
from apps.robots.models import Robot
from apps.items.models import Item
from apps.processes.models import Process
from apps.api.utils import token_login, check_id, check_if_can_change_status
from apps.utils.choices import Status
from apps.robots.tasks import periodic_task_check


class TaskAPIView(APIView):
    """
    View para obter e editar informações sobre tarefas.
    """
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            Parameter("robot_id", in_=IN_QUERY, type=TYPE_INTEGER, required=True, description="ID do robô."),
            Parameter("task_id", in_=IN_QUERY, type=TYPE_INTEGER, required=False, description="ID da tarefa."),
            Parameter("status", in_=IN_QUERY, type=TYPE_STRING, required=False, description="Novo status da tarefa."),
            Parameter("started_at", in_=IN_QUERY, type=TYPE_STRING, required=False, description="Data e hora de início (formato: YYYY-MM-DD HH:MM:SS)."),
            Parameter("ended_at", in_=IN_QUERY, type=TYPE_STRING, required=False, description="Data e hora de término (formato: YYYY-MM-DD HH:MM:SS)."),
        ],
        responses={200: TaskWithItemsSerializer(many=True)},
        operation_description="Esquema customizado para TaskAPIView",
    )

    def get(self, request) -> Response:
        """
        Obtém todas as tarefas filtradas pelo ID do robô.

        Parâmetros:
        - robot_id (parâmetro da query): ID do robô.

        Resposta:
        - 200 OK: Lista de tarefas com itens associados.
        - 404 NOT FOUND: Se o robô não existir.

        Autenticação:
        - Token Bearer:
            Um token de API válido deve ser fornecido no cabeçalho 'Authorization'.
            Exemplo: Authorization: Token XXXX-XXXX-XXXX-XXXX
        """
        id = request.query_params.get('robot_id')
        check_id(id)
        try:
            robot = Robot.objects.get(id=id)
        except Robot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        tasks_with_items = Task.objects.filter(
            robot_id=robot.id,
            status__in=[Status.CREATED, Status.STARTED]
        ).prefetch_related('item_set').all()
        serializer = TaskWithItemsSerializer(tasks_with_items, many=True)
        return Response(data=serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            Parameter("robot_id", in_=IN_QUERY, type=TYPE_INTEGER, required=True, description="ID do robô."),
            Parameter("task_id", in_=IN_QUERY, type=TYPE_INTEGER, required=True, description="ID da tarefa."),
            Parameter("status", in_=IN_QUERY, type=TYPE_STRING, required=False, description="Novo status da tarefa."),
        ],
        operation_description="Editar informações sobre uma tarefa",
    )

    def patch(self, request):
        """
        Edita uma tarefa.

        Parâmetros necessários na query:
        - robot_id: ID do robô.
        - task_id: ID da tarefa.
        - status: Novo status da tarefa.

        Respostas:
        - 200 OK: A tarefa foi editada com sucesso.
        - 404 NOT FOUND: Se o robô ou a tarefa não existirem.
        """
        robot_id = request.query_params.get('robot_id')
        task_id = request.query_params.get('task_id')
        check_id(robot_id, task_id)

        try:
            Robot.objects.get(id=robot_id)
            task = Task.objects.get(id=task_id)
        except (Robot.DoesNotExist, Task.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        check_if_can_change_status(task)
        serializer = TaskSerializer(instance=task, data=request.query_params, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
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

