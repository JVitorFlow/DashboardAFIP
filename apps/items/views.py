from collections import defaultdict
from datetime import datetime
from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.items.models import Item
from apps.robots.models import Robot
from apps.tasks.models import Task
from apps.values.models import ShiftData
from apps.values.serializer import ShiftDataSerializer

from .forms import ShiftDataForm
from .serializer import (ItemSerializer, ShiftDataUpsertSerializer,
                         TaskSummarySerializer)


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, editar e gerenciar itens.
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Listar todos os itens cadastrados.',
        operation_summary='Listar Itens',
    )
    def list(self, request, *args, **kwargs):
        """
        Listar todos os itens cadastrados no sistema.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Criar um novo item no sistema.',
        operation_summary='Criar Item',
    )
    def create(self, request, *args, **kwargs):
        """
        Criar um novo item no sistema.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Obter detalhes de um item específico pelo ID.',
        operation_summary='Detalhar Item',
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Obter detalhes de um item específico pelo ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Atualizar completamente um item específico pelo ID.',
        operation_summary='Atualizar Item',
    )
    def update(self, request, *args, **kwargs):
        """
        Atualizar completamente um item específico pelo ID.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Atualizar parcialmente um item específico pelo ID.',
        operation_summary='Atualizar Parcialmente Item',
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Atualizar parcialmente um item específico pelo ID.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Deletar um item específico pelo ID.',
        operation_summary='Deletar Item',
    )
    def destroy(self, request, *args, **kwargs):
        """
        Deletar um item específico pelo ID.
        """
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Listar todos os itens em uma etapa específica (SHIFT, IMAGE_PROCESS, SISMAMA).',
        operation_summary='Listar Itens por Etapa',
        manual_parameters=[
            openapi.Parameter(
                'stage',
                openapi.IN_QUERY,
                description='Etapa do processamento (SHIFT, IMAGE_PROCESS, SISMAMA).',
                type=openapi.TYPE_STRING,
            )
        ],
    )
    @action(detail=False, methods=['get'], url_path='by-stage')
    def list_by_stage(self, request):
        """
        Lista todos os itens em uma etapa específica para processamento pelo robô.

        Parâmetros:
        - stage (str): Etapa do processamento.
        """
        stage = request.query_params.get('stage')
        if stage not in ['SHIFT', 'IMAGE_PROCESS', 'SISMAMA']:
            return Response(
                {
                    'detail': 'Etapa inválida. Use SHIFT, IMAGE_PROCESS ou SISMAMA.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        items_in_stage = Item.objects.filter(stage=stage).order_by(
            'created_at'
        )

        if not items_in_stage.exists():
            return Response(
                {'detail': f'Nenhum item encontrado na etapa {stage}.'},
                status=status.HTTP_200_OK,
            )

        # Organiza os itens por tarefa usando um dicionário
        tasks_dict = defaultdict(list)
        for item in items_in_stage:
            tasks_dict[item.task_id].append(item)

        response_data = []
        for task, items in tasks_dict.items():
            # Serializa os dados da tarefa usando o resumo da tarefa
            task_data = TaskSummarySerializer(task).data
            task_data['items'] = ItemSerializer(items, many=True).data
            response_data.append(task_data)

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Atualizar o status e a etapa de um item pelo seu ID e pelo `robot_id` associado.',
        operation_summary='Atualizar Status e Etapa do Item',
        manual_parameters=[
            openapi.Parameter(
                'robot_id',
                openapi.IN_QUERY,
                description='ID do robô.',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description='Novo status do item.',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'stage',
                openapi.IN_QUERY,
                description='Nova etapa do item (SHIFT, IMAGE_PROCESS, SISMAMA, COMPLETED).',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'item__started_at',
                openapi.IN_QUERY,
                description='Data e hora de início (formato: AAAA-MM-DD HH:MM:SS).',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'item__ended_at',
                openapi.IN_QUERY,
                description='Data e hora de término (formato: AAAA-MM-DD HH:MM:SS).',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'bot_error_message',
                openapi.IN_QUERY,
                description='Mensagem de erro do bot, se houver.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Atualiza o status, a etapa e, se fornecido, a mensagem de erro do bot de um item pelo seu ID.
        Parâmetros:
        - robot_id (int): ID do robô associado.
        - status (str): Novo status do item.
        - stage (str): Nova etapa do item.
        - item__started_at (str): Data e hora de início.
        - item__ended_at (str): Data e hora de término.
        - bot_error_message (str): Mensagem de erro do bot, se houver.
        """
        robot_id = request.data.get('robot_id')
        stage = request.data.get('stage')

        if not robot_id or stage not in [
            'SHIFT',
            'IMAGE_PROCESS',
            'SISMAMA',
            'COMPLETED',
        ]:
            return Response(
                {'detail': 'robot_id ausente ou etapa inválida.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            robot = Robot.objects.get(id=robot_id)
            item = Item.objects.get(id=pk)
        except (Robot.DoesNotExist, Item.DoesNotExist):
            raise NotFound(detail='Robô ou item não encontrado.')

        # Atualiza o status e a etapa do item
        serializer = ItemSerializer(
            instance=item, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Autoriza a continuação do processamento do item.',
        operation_summary='Autorizar Item',
        responses={200: ItemSerializer},
    )
    @action(
        detail=True,
        methods=['patch'],
        url_path='authorize',
        permission_classes=[AllowAny],
    )
    def authorize(self, request, pk=None):
        """
        Atualiza o campo is_authorized para True para autorizar a continuação do item.

        Retorna:
        - Response: Confirmação da autorização.
        """
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            raise NotFound(detail='Item não encontrado.')

        # Atualiza o campo is_authorized para True
        item.is_authorized = True
        item.save()

        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='sismama-data')
    def get_sismama_data(self, request):
        authorized = (
            Item.objects.filter(is_authorized=True, stage='SISMAMA')
            .select_related('task')
            .prefetch_related('shift_data')
        )

        result = []
        for item in authorized:
            sd = item.shift_data.first()
            if not sd:
                continue
            item_data = ItemSerializer(item).data
            sd_data = ShiftDataSerializer(sd).data

            result.append({**item_data, 'shift_data': sd_data})

        if not result:
            return Response(
                {'detail': 'Nenhum dado autorizado encontrado.'}, status=200
            )
        return Response(result, status=200)

    @swagger_auto_schema(
        operation_summary='Upsert de ShiftData por item',
        request_body=ShiftDataUpsertSerializer,
        responses={
            200: ShiftDataUpsertSerializer,
            201: ShiftDataUpsertSerializer,
        },
    )
    @action(detail=True, methods=['post'], url_path='shift-data')
    def upsert_shift_data(self, request, pk=None):
        """
        Cria ou atualiza o ShiftData para este item:
        - Se já existir registro com o mesmo os_number (e task, se desejar),
        atualiza com os novos dados.
        - Caso contrário, cria um novo.
        """
        item = self.get_object()
        serializer = ShiftDataUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # vincula o FK task/item
        data.update(task=item.task_id, item=item)

        # faz o upsert: filtra por os_number (e opcionalmente task)
        shift_obj, created = ShiftData.objects.update_or_create(
            os_number=data['os_number'], defaults=data
        )

        out = ShiftDataUpsertSerializer(shift_obj)
        code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(out.data, status=code)


class ItemListView(LoginRequiredMixin, ListView):
    """
    View to display the list of items associated with a task.
    """

    login_url = 'login'
    template_name = 'home/items.html'

    def dispatch(self, request, *args: Any, **kwargs: Any):
        task_id = self.kwargs['task_id']
        self.task = get_object_or_404(Task, id=task_id)
        if request.user != self.task.user_id:
            return redirect(reverse('tasks'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        """
        Obtains the set of items associated with the task.
        Also fetches the associated ShiftData.
        """
        queryset = Item.objects.filter(task_id=self.task).order_by('-id')
        # Pré-carregar os dados de ShiftData para otimizar consultas
        queryset = queryset.prefetch_related('shift_data')
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Provides the context for the template, including task and items data.
        """
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        context['segment'] = 'items'
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = []
    template_name = 'includes/modal_default.html'

    def get_success_url(self):
        """Redireciona para a lista de itens da tarefa após atualização."""
        item = self.get_object()
        return reverse('items', args=[item.task_id])

    def get_context_data(self, **kwargs):
        """Adiciona os dados do ShiftData ao contexto do template."""
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        shift_data = item.shift_data.first()
        context['shift_data_form'] = ShiftDataForm(instance=shift_data)
        return context

    def form_valid(self, form):
        """Processa a atualização do item e do ShiftData relacionado."""
        response = super().form_valid(form)  # Atualiza o item principal
        self.update_item_image_result()
        self.update_shift_data()
        return response

    def update_item_image_result(self):
        """Atualiza apenas o campo `image_result` do Item se um novo valor for enviado."""
        image_result = self.request.POST.get('image_result')
        if image_result:  # Só atualiza se um novo valor for enviado
            item = self.get_object()
            item.image_result = image_result
            item.save()

    def update_shift_data(self):
        """Atualiza os campos do ShiftData associados ao item."""
        shift_data = self.get_object().shift_data.first()
        if not shift_data:
            return  # Se não existir ShiftData, não faz nada

        shift_data_fields = self.get_shift_data_fields()
        for field, value in shift_data_fields.items():
            if (
                value is not None and str(value).strip()
            ):  # Evita sobrescrever com valores vazios
                setattr(shift_data, field, value)

        shift_data.save()

    def get_shift_data_fields(self):
        """Extrai os campos enviados no formulário relacionados ao ShiftData de forma dinâmica."""
        campos = {
            'cnes': self.clean_value,
            'os_number': self.clean_value,
            'cartao_sus': self.clean_value,
            'nome_paciente': self.clean_value,
            'recipiente': self.clean_value,
            'sexo': self.clean_value,
            'raca_etinia': self.clean_value,
            'idade_paciente': self.parse_int,
            'data_nascimento': self.parse_date,
            'data_coleta': self.parse_date,
            'data_liberacao': self.parse_date,
            'tamanho_lesao': self.clean_value,
            'caracteristica_lesao': self.clean_value,
            'localizacao_lesao': self.clean_value,
            'codigo_postal': self.clean_value,
            'logradouro': self.clean_value,
            'numero_residencial': self.clean_value,
            'cidade': self.clean_value,
            'estado': self.clean_value,
        }

        return {
            campo: func(self.request.POST.get(campo))
            for campo, func in campos.items()
        }

    @staticmethod
    def parse_date(date_str):
        """Converte data do formato 'YYYY-MM-DD' para um objeto date ou retorna None."""
        if not date_str:
            return None
        try:
            date_str = date_str.split('T')[0]  # Remove horário se presente
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None

    @staticmethod
    def parse_int(value):
        """Converte string para inteiro ou retorna None."""
        try:
            return int(value) if value and value.isdigit() else None
        except ValueError:
            return None

    @staticmethod
    def clean_value(value):
        """Remove espaços extras e retorna None se o valor for vazio."""
        return value.strip() if value and value.strip() else None
