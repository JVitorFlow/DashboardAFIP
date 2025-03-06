from rest_framework import serializers
from .models import RobotAlert

class RobotAlertSerializer(serializers.ModelSerializer):
    # Limita os tipos de alerta permitidos (exemplo: start, finish, error)
    ALERT_TYPES = (
        ("start", "Start"),
        ("finish", "Finish"),
        ("error", "Error"),
    )
    alert_type = serializers.ChoiceField(choices=ALERT_TYPES)

    class Meta:
        model = RobotAlert
        # Inclui todos os campos que você deseja expor via API;
        # 'id' e 'created_at' serão somente leitura
        fields = "__all__"
        read_only_fields = ("id", "created_at")
