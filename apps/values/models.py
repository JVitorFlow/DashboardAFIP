from django.db import models
from apps.items.models import Item
from apps.tasks.models import Task

class ShiftData(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="shift_data",
        null=False,
        blank=False
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="shift_data",
        null=False,
        blank=False
    )
    cnes = models.CharField(max_length=100, blank=True, null=True)
    os_number = models.CharField(max_length=50)
    cartao_sus = models.CharField(max_length=100, blank=True, null=True)
    nome_paciente = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=255, blank=True, null=True)
    raca_etinia = models.CharField(max_length=255, blank=True, null=True)
    idade_paciente = models.IntegerField(blank=True, null=True)
    

    data_nascimento = models.DateField(blank=True, null=True)
    data_coleta = models.DateTimeField(blank=True, null=True)
    data_liberacao = models.DateTimeField(blank=True, null=True)

    recipiente = models.CharField(max_length=100, blank=True, null=True)
    
    tamanho_lesao = models.CharField(max_length=255, blank=True, null=True)
    caracteristica_lesao = models.CharField(max_length=255, blank=True, null=True)
    localizacao_lesao = models.CharField(max_length=255, blank=True, null=True)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    numero_residencial = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)

    # Novos campos sugeridos para resultados e status
    status_shift = models.CharField(max_length=50, blank=True, null=True)
    shift_result = models.CharField(max_length=255, blank=True, null=True)
    sismama_result = models.CharField(max_length=255, blank=True, null=True)
    stage = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ShiftData para Task {self.task.id}, Item {self.item.id}"

    class Meta:
        unique_together = ('item',)