from django.contrib import admin
from .models import ShiftData

@admin.register(ShiftData)
class ShiftDataAdmin(admin.ModelAdmin):
    """
    Admin para o modelo ShiftData, exibindo campos relevantes e customizando
    a listagem e o detalhe da tarefa e seus dados.
    """

    # Campos a serem exibidos na listagem do admin
    list_display = (
        'task', 
        'item', 
        'os_number', 
        'nome_paciente', 
        'data_coleta', 
        'data_liberacao', 
        'status_shift',
        'created_at'
    )
    list_filter = ('status_shift', 'data_coleta', 'data_liberacao', 'created_at')
    search_fields = ('os_number', 'nome_paciente', 'cnes')
    date_hierarchy = 'created_at'
    
    # Campos a serem exibidos no formulário de detalhes
    fieldsets = (
        ("Informações da Tarefa e Item", {
            'fields': ('task', 'item')
        }),
        ("Informações do Paciente", {
            'fields': ('nome_paciente', 'cartao_sus', 'sexo', 'raca_etinia', 'idade_paciente', 'data_nascimento')
        }),
        ("Detalhes do Procedimento", {
            'fields': ('os_number', 'cnes', 'data_coleta', 'data_liberacao', 'tamanho_lesao', 'caracteristica_lesao', 'localizacao_lesao')
        }),
        ("Endereço do Paciente", {
            'fields': ('logradouro', 'numero_residencial', 'codigo_postal', 'cidade', 'estado')
        }),
        ("Resultados e Status", {
            'fields': ('status_shift', 'shift_result', 'sismama_result', 'stage')
        }),
        ("Data de Criação", {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    # Campos somente leitura no formulário de detalhes
    readonly_fields = ('created_at',)

    # Ordem padrão dos itens na listagem do admin
    ordering = ('-created_at',)

    # Personalização da exibição de detalhes de cada registro
    def has_change_permission(self, request, obj=None):
        if obj and obj.status_shift == "COMPLETED":
            return False  # Evita mudanças em tarefas já completas
        return super().has_change_permission(request, obj)
