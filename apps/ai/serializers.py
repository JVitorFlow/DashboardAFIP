from rest_framework import serializers
from .models import AIAssessment


class AIAssessmentInputSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    image = serializers.ImageField(required=True)


class AIAssessmentOutputSerializer(serializers.ModelSerializer):
    os_number = serializers.CharField(source="item.os_number", read_only=True)

    class Meta:
        model = AIAssessment
        fields = [
            "id",
            "task",
            "item",
            "os_number",
            "tipo_exame_histopatologico",
            "apresenta_risco_elevado_para_cancer_de_mama",
            "gravida_ou_amamentando",
            "tratamento_anterior_para_cancer",
            "deteccao_da_lesao",
            "mama",
            "localizacao_lesao",
            "tamanho_lesao",
            "caracteristica_lesao",
            "material_enviado_procedente_de",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "task", "item", "os_number", "status", "created_at"]
