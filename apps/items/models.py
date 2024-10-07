from django.db import models
from apps.tasks.models import Task
from apps.robots.models import Robot
from apps.utils.choices import Status


class Item(models.Model):
    task_id = models.ForeignKey(
        to=Task,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        db_index=True
    )
    robot_id = models.ForeignKey(
        to=Robot,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        db_index=True
    )
    os_number = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        help_text="Número da Ordem de Serviço"
    )
    os_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Nome associado à Ordem de Serviço"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        choices=Status.choices,
        default=Status.CREATED
    )
    shift_result = models.TextField(null=True, blank=True)
    sismama_result = models.TextField(null=True, blank=True)
    stage = models.CharField(max_length=50, default='PENDING')
    def __str__(self) -> str:
        return f"{self.os_number} - {self.os_name or 'Sem nome'}"
