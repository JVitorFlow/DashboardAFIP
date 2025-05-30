import uuid
from django.db import models
from apps.robots.models import Robot 

class RobotAlert(models.Model):
    """
    Representa um alerta gerado para um robô.
    """

    ALERT_TYPES = [
        ("Informacao", "Informação"),
        ("Erro", "Erro"),
        ("Sucesso", "Sucesso"),
        ("Alerta", "Alerta"),
        ("Debug", "Debug"),
        ("Timeout", "Timeout"),
        ("Validacao", "Validação"),
        ("Interrupcao", "Interrupção"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE, related_name="alerts")
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.robot} - {self.alert_type}"

    class Meta:
        ordering = ['-created_at']