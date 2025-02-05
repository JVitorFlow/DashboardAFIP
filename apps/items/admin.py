from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Item com listagem personalizada,
    e exibição limpa de 'image_result'.
    """

    # Exibir estas colunas na listagem
    list_display = (
        'os_number',
        'os_name',
        'status',
        'stage',
        'created_at',
    )

    # Adicionar filtros laterais para facilitar a busca
    list_filter = ('status', 'stage', 'created_at')

    # Permitir busca por número e nome da OS
    search_fields = ('os_number', 'os_name')

    # Permitir edição direta na tabela para status e stage
    list_editable = ('status', 'stage')

    # Campos somente leitura (não podem ser editados diretamente)
    readonly_fields = ('created_at', 'pretty_image_result')

    # Organizar os campos em seções
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('os_number', 'os_name', 'status', 'stage')
        }),
        ('Resultados', {
            'fields': ('shift_result', 'pretty_image_result')  # Exibe o 'image_result' como texto
        }),
        ('Datas', {
            'fields': ('created_at',)  # Somente leitura
        }),
    )

    def pretty_image_result(self, obj):
        """
        Exibir o campo 'image_result' como texto formatado no Django Admin.
        """
        if obj.image_result:
            # Escapar caracteres especiais e formatar como texto pré-formatado
            return mark_safe(f'<pre style="white-space: pre-wrap;">{obj.image_result}</pre>')
        return "Sem dados"

    # Descrição para o campo formatado
    pretty_image_result.short_description = "Resultado da Imagem (Texto)"

    # Adicionar ações personalizadas no Django Admin
    actions = ['marcar_como_completed', 'marcar_como_pending', 'apagar_resultado_imagem']

    def marcar_como_completed(self, request, queryset):
        """
        Ação para marcar os itens selecionados como COMPLETED.
        """
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f'{updated} itens marcados como COMPLETED com sucesso.')

    marcar_como_completed.short_description = 'Marcar como COMPLETED'

    def marcar_como_pending(self, request, queryset):
        """
        Ação para marcar os itens selecionados como PENDING.
        """
        updated = queryset.update(status='PENDING')
        self.message_user(request, f'{updated} itens marcados como PENDING com sucesso.')

    marcar_como_pending.short_description = 'Marcar como PENDING'

    def apagar_resultado_imagem(self, request, queryset):
        """
        Ação personalizada para apagar o conteúdo de 'image_result'.
        """
        updated = queryset.update(image_result=None)
        self.message_user(request, f'Resultado de imagem apagado para {updated} itens.')

    apagar_resultado_imagem.short_description = 'Apagar Resultado de Imagem'
