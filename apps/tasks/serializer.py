from rest_framework import serializers
from .models import Task
from apps.items.models import Item
from apps.items.serializer import ItemSerializer


class TaskSummarySerializer(serializers.ModelSerializer):
    """
    Serializador resumido para a Tarefa.
    """
    class Meta:
        model = Task
        fields = ['id', 'created_at', 'status', 'robot_id']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializador detalhado para a Tarefa, com os itens aninhados.
    """
    items = ItemSerializer(many=True, read_only=True, source='item_set')

    class Meta:
        model = Task
        fields = ['id', 'created_at', 'status', 'robot_id', 'items']
