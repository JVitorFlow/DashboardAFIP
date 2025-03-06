import uuid
from django.db import models
from apps.robots.models import Robot 

class RobotAlert(models.Model):
    """
    Representa um alerta gerado para um robô.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE, related_name="alerts")
    alert_type = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.robot.name} - {self.alert_type}"
