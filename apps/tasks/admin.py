from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Customiza a visualização das tasks no Django Admin.
    """
    # Exibe mais informações na listagem das tasks no admin
    list_display = ('id', 'created_at', 'status', 'robot_id', 'user_id', 'process_id')
    list_display_links = ('id',)  # Permite clicar no ID para editar
    list_filter = ('status', 'created_at', 'robot_id')  # Filtros laterais
    search_fields = ('id', 'user_id__username', 'robot_id__name')  # Campo de busca
    list_per_page = 20  # Número de tasks por página

    # Campos que podem ser editados diretamente da listagem (opcional)
    list_editable = ('status',)

    # Ordenação padrão por data de criação
    ordering = ('-created_at',)

