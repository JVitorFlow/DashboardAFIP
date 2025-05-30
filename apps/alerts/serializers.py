from rest_framework import serializers
from .models import RobotAlert

class RobotAlertSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo RobotAlert.

    - Flexível: não restringe os tipos de alerta com choices fixos.
    - Seguro: mantém campos de leitura como 'id' e 'created_at'.
    """

    alert_type = serializers.ChoiceField(
        choices=RobotAlert.ALERT_TYPES,
        help_text="Tipo do alerta. Valores permitidos: Informacao, Erro, Sucesso, Alerta, Debug, Timeout, Validacao, Interrupcao."
    )

    message = serializers.CharField(
        help_text="Mensagem descritiva do alerta."
    )

    details = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Detalhes técnicos do alerta (stack trace, logs, etc.)."
    )

    class Meta:
        model = RobotAlert
        fields = [
            "id",
            "robot",
            "alert_type",
            "message",
            "details",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")
