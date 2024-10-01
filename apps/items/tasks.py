from apps.items.utils import get_items
from apps.core.memory_manager import get_memory


def get_items_first_time_run_server():
    """
    Recupera itens não atribuídos em caso de inicialização ou reinicialização do servidor.

    Esta função é usada para obter itens que não foram atribuídos
    para qualquer robô quando o servidor for iniciado ou reiniciado.
    Atualiza a lista de itens não atribuídos no objeto de memória.

    Retorna:
        Nenhum
    """
    memory = get_memory()
    memory.items = get_items(robots=None).all()
