import csv
from .models import Task
from apps.items.models import Item
from apps.values.models import ShiftData
from apps.robots.utils import get_min_robot


def get_tasks_from_items(items):
    """
    Obtém tarefas exclusivas de uma lista de itens.

    Parâmetros:
    - itens (QuerySet): Conjunto de itens.

    Retorna:
    QuerySet: Conjunto de tarefas exclusivas relacionadas aos itens fornecidos.
    """
    unique_task_ids = items.values_list('task_id', flat=True).distinct()
    unique_tasks = Task.objects.filter(id__in=unique_task_ids)
    return unique_tasks


def read_file(file, user, process):
    """
    Lê um arquivo CSV e cria objetos Item no banco de dados.

    Parâmetros:
    - file (Arquivo): O arquivo CSV a ser lido.
    - user (User): O usuário associado à tarefa.
    - process (Process): O processo associado à tarefa.

    Retorna:
    bool: Verdadeiro se a operação foi bem-sucedida,
          Falso se um robô não puder ser atribuído.
    """
    # Obtém o robô com menor carga
    robot = get_min_robot()
    task = Task.objects.create(user_id=user, process_id=process, robot_id=robot)

    # Ler o arquivo CSV utilizando DictReader
    csv_reader = csv.DictReader(file.read().decode('utf-8').splitlines())

    # Lista para armazenar os objetos Item a serem criados
    items_to_create = []

    # Iterar sobre as linhas do arquivo CSV e adicionar à lista
    for row in csv_reader:
        try:
            # Extrair o valor da coluna "O.S."
            os_field = row.get('O.S.')
            if not os_field:
                continue

            # Dividir a string em número da OS e nome, removendo ponto e vírgula
            os_field = os_field.rstrip(';')
            os_number, os_name = os_field.split(' - ', 1)
            os_number = os_number.strip()
            os_name = os_name.strip()

            # Criar um objeto Item e associar à tarefa
            item = Item(
                task_id=task,
                robot_id=robot,
                os_number=os_number,
                os_name=os_name
            )
            items_to_create.append(item)

        except Exception as e:
            print(f"Erro ao processar linha: {row}. Erro: {e}")
            continue

    # Inserir os objetos Item no banco de dados usando bulk_create
    Item.objects.bulk_create(items_to_create)

    if not robot:
        return False
    return True


