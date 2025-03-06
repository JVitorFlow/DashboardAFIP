from django.db import models
from apps.tasks.models import Task
from apps.robots.models import Robot
from apps.utils.choices import Status


class Item(models.Model):
    # Etapas do processamento
    STAGE_CHOICES = [
        ('SHIFT', 'Shift Process'),          # Etapa de Shift
        ('IMAGE_PROCESS', 'Image Process'),  # Etapa de processamento de imagem
        ('SISMAMA', 'Sismama Process'),      # Etapa de Sismama
        ('COMPLETED', 'Completed')           # Finalizado
    ]
    # Referência para a task
    task_id = models.ForeignKey(
        to=Task,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        db_index=True
    )

    # Referência para o robô
    robot_id = models.ForeignKey(
        to=Robot,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        db_index=True
    )

    # Informações da Ordem de Serviço
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

    # Status do item
    status = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        choices=Status.choices,
        default=Status.CREATED
    )

    # Datas de criação e execução
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    # Resultados das etapas
    shift_result = models.TextField(null=True, blank=True)
    image_result = models.TextField(null=True, blank=True)
    sismama_result = models.TextField(null=True, blank=True)

    # Etapa atual do processamento
    stage = models.CharField(
        max_length=50,
        choices=STAGE_CHOICES,
        default='SHIFT',  # Começa na etapa de SHIFT
        help_text="Etapa atual do processamento do item"
    )

    # Campo de autorização
    is_authorized = models.BooleanField(default=False, help_text="Indica se o usuário autorizou o avanço para a etapa sistama")
    bot_error_message = models.TextField(null=True, blank=True, help_text="Mensagem de erro do bot, se houver")


    def __str__(self) -> str:
        return f"{self.os_number} - {self.os_name or 'Sem nome'}"