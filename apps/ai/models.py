from django.db import models
from apps.items.models import Item
from apps.tasks.models import Task

class AIAssessment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="ai_assessments"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="ai_assessments"
    )
    tipo_exame_histopatologico = models.CharField(
        max_length=255, blank=True, null=True
    )
    apresenta_risco_elevado_para_cancer_de_mama = models.CharField(
        max_length=255, blank=True, null=True
    )
    gravida_ou_amamentando = models.CharField(
        max_length=255, blank=True, null=True
    )
    tratamento_anterior_para_cancer = models.CharField(
        max_length=255, blank=True, null=True
    )
    deteccao_da_lesao = models.CharField(
        max_length=255, blank=True, null=True
    )
    mama = models.CharField(max_length=255, blank=True, null=True)
    localizacao_lesao = models.CharField(max_length=255, blank=True, null=True)
    tamanho_lesao = models.CharField(max_length=255, blank=True, null=True)
    caracteristica_lesao = models.TextField(blank=True, null=True)
    material_enviado_procedente_de = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='PENDING')

    # Adicionando campos created_at e updated_at
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AIAssessment for Task {self.task.id}, Item {self.item.id}"

    def caracteristica_lesao_formatada(self):
        return f"Mama: {self.mama}, Localização: {self.localizacao_lesao}, Tamanho: {self.tamanho_lesao}"
    