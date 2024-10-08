from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Item com listagem personalizada e opções de filtragem e busca.
    """
    list_display = (
        'id', 'task_id', 'robot_id', 'os_number', 'os_name', 
        'created_at', 'started_at', 'ended_at', 'status', 'stage'
    )
    list_filter = ('status', 'robot_id', 'task_id', 'created_at', 'stage')
    search_fields = ('os_number', 'os_name', 'shift_result', 'sismama_result')
    readonly_fields = ('created_at', 'started_at', 'ended_at')
    fieldsets = (
        (None, {
            'fields': ('task_id', 'robot_id', 'os_number', 'os_name', 'status', 'stage')
        }),
        ('Resultados', {
            'fields': ('shift_result', 'sismama_result')
        }),
        ('Datas', {
            'fields': ('created_at', 'started_at', 'ended_at')
        }),
    )

    def has_add_permission(self, request):
        """
        Remove a permissão de adicionar itens diretamente no admin.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Remove a permissão de deletar itens diretamente no admin.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Permissão para editar itens no admin.
        """
        return True
