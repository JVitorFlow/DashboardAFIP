from django.db.models.query import QuerySet


class Memory:
    """
    Classe Singleton representando a memória do sistema
    para armazenar itens e tarefas pendentes para atribuição.
    """
    def __init__(self):
        """
        Inicializa a memória com conjuntos QuerySet vazios para itens e tarefas.
        """
        self.items = QuerySet().none()
        self.tasks = QuerySet().none()

    def clear(self):
        """
        Limpa a memória esvaziando os conjuntos de itens e tarefas.
        """
        self.items = self.items.none()
        self.tasks = self.tasks.none()


# Singleton pattern
memory_instance = Memory()


def get_memory():
    """
    Obtém a instância exclusiva da memória do sistema.

    Retorna:
    Memória: instância única da classe Memory.
    """
    return memory_instance
