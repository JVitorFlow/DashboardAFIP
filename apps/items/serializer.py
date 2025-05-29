from rest_framework import serializers
from .models import Item
from apps.tasks.models import Task
from apps.values.models import ShiftData


from apps.values.serializer import ShiftDataMiniSerializer

class TaskSummarySerializer(serializers.ModelSerializer):
    """
    Serializador resumido para a Tarefa.
    """

    class Meta:
        model = Task
        fields = ["id", "created_at", "status", "robot_id"]


class ItemSerializer(serializers.ModelSerializer):
    shift_data = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "os_number",
            "os_name",
            "created_at",
            "started_at",
            "ended_at",
            "status",
            "bot_error_message",
            "shift_result",
            "image_result",
            "sismama_result",
            "stage",
            "is_authorized",
            "shift_data",
        ]

    def get_shift_data(self, obj):
        shift_data = obj.shift_data.first()
        if shift_data:
            return ShiftDataMiniSerializer(shift_data).data
        return None
    


class ShiftDataUpsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftData
        fields = '__all__'
        read_only_fields = ('id',)