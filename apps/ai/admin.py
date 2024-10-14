from django.contrib import admin
from .models import AIAssessment

@admin.register(AIAssessment)
class AIAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'task', 
        'item', 
        'status', 
        'created_at', 
        'updated_at', 
        'caracteristica_lesao_formatada'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_filter = ('status', 'created_at')

    # Método para melhorar a exibição de caracteristicas da lesão
    def caracteristica_lesao_formatada(self, obj):
        if obj.mama or obj.localizacao_lesao or obj.tamanho_lesao:
            return f"Mama: {obj.mama}, Localização: {obj.localizacao_lesao}, Tamanho: {obj.tamanho_lesao}"
        return "N/A"
    caracteristica_lesao_formatada.short_description = "Características da Lesão"

