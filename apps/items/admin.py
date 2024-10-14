from django.contrib import admin
from .models import Item
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import json

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Item com listagem personalizada,
    exibição formatada de JSON para o campo 'image_result',
    e a possibilidade de editar status e stage diretamente na listagem.
    """

    list_display = (
        'os_number', 'os_name', 'status', 'stage', 'created_at'
    )
    list_filter = ('status', 'stage', 'created_at')
    search_fields = ('os_number', 'os_name')

    # Permitir edição direta dos campos 'status' e 'stage'
    list_editable = ('status', 'stage')

    readonly_fields = ('created_at', 'pretty_image_result')

    fieldsets = (
        (None, {
            'fields': ('os_number', 'os_name', 'status', 'stage')
        }),
        ('Resultados', {
            'fields': ('shift_result', 'pretty_image_result')  # Exibe o 'image_result' formatado
        }),
        ('Datas', {
            'fields': ('created_at',)  # Campos somente leitura
        }),
    )

    def pretty_image_result(self, obj):
        """
        Exibe o campo image_result formatado em uma estrutura legível no Django Admin.
        """
        if obj.image_result:
            try:
                # Garantir que image_result é um dicionário válido, caso seja string JSON
                result = json.loads(obj.image_result) if isinstance(obj.image_result, str) else obj.image_result
                
                html_output = '<table class="table table-bordered">'

                for key, value in result.items():
                    if isinstance(value, dict):  # Se for um dicionário aninhado
                        html_output += f'<tr><td><strong>{key}</strong></td><td>'
                        html_output += '<table class="table table-sm">'
                        for subkey, subvalue in value.items():
                            html_output += f'<tr><td><strong>{subkey}:</strong></td><td>{subvalue}</td></tr>'
                        html_output += '</table></td></tr>'
                    elif isinstance(value, list):  # Se for uma lista
                        html_output += f'<tr><td><strong>{key}</strong></td><td><ul>'
                        for item in value:
                            html_output += f'<li>{item}</li>'
                        html_output += '</ul></td></tr>'
                    else:
                        html_output += f'<tr><td><strong>{key}</strong></td><td>{value}</td></tr>'

                html_output += '</table>'
                return mark_safe(html_output)
            except json.JSONDecodeError:
                return "Erro ao processar JSON"
        return "Sem dados"

    pretty_image_result.short_description = "Image Result (Tabela)"

    # Adicionar ações personalizadas
    actions = ['marcar_como_completed', 'marcar_como_pending', 'apagar_resultado_imagem']

    # Ação para marcar itens selecionados como COMPLETED
    def marcar_como_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f'{updated} itens marcados como COMPLETED com sucesso.')
    marcar_como_completed.short_description = 'Marcar itens selecionados como COMPLETED'

    # Ação para marcar itens selecionados como PENDING
    def marcar_como_pending(self, request, queryset):
        updated = queryset.update(status='PENDING')
        self.message_user(request, f'{updated} itens marcados como PENDING com sucesso.')
    marcar_como_pending.short_description = 'Marcar itens selecionados como PENDING'

    # Ação para apagar o resultado da imagem
    def apagar_resultado_imagem(self, request, queryset):
        """
        Ação personalizada para apagar o conteúdo de image_result.
        """
        updated = queryset.update(image_result=None)
        self.message_user(request, f'O conteúdo de image_result foi apagado para {updated} itens com sucesso.')
    apagar_resultado_imagem.short_description = 'Apagar Resultado de Imagem'
