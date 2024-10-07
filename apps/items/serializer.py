from rest_framework import serializers
from .models import Item
from apps.tasks.models import Task


class TaskSummarySerializer(serializers.ModelSerializer):
    """
    Serializador resumido para a Tarefa.
    """
    class Meta:
        model = Task
        fields = ['id', 'created_at', 'status', 'robot_id']


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializador para os Itens, incluindo os campos de OS e nome.
    """

    class Meta:
        model = Item
        fields = [
            'id', 'os_number', 'os_name', 'created_at',
            'started_at', 'ended_at', 'status'
        ]
