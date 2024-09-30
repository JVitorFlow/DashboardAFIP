from django_celery_beat.models import PeriodicTask, IntervalSchedule
from tasks.utils import get_tasks_from_items
from items.utils import get_items
from robots.utils import (check_disconnected_robots, change_status_inactive,
                          assing_robots, get_min_robot, get_active_robots,
                          remove_robots)
from orchestrator.celery import app
from orchestrator.memory_manager import get_memory


# CREATING THE TASK: handle_disconnected_robots
# Crie ou obtenha um cronograma de intervalo para executar a tarefa a cada 1 minuto
schedule_handle, created_handle = IntervalSchedule.objects.get_or_create(
    every=3,
    period=IntervalSchedule.MINUTES,
)

# Tente obter uma tarefa periódica existente ou crie uma nova
try:
    periodic_task_handle = PeriodicTask.objects.get(
        name='handle_disconnected_robots')
except PeriodicTask.DoesNotExist:
    # If the task doesn't exist, create it
    periodic_task_handle = PeriodicTask.objects.create(
        interval=schedule_handle,
        name='handle_disconnected_robots',
        task='robots.tasks.handle_disconnected_robots',
        enabled=True,
    )


@app.task
def handle_disconnected_robots():
    """
    Tarefa do Celery para lidar com robôs desconectados.

    Esta tarefa está programada para ser executada periodicamente e executa
    as seguintes ações:
    1. Procura robôs desconectados.
    2. Altera o estado dos robôs desconectados para inativos.
    3. Recupera itens associados a robôs desconectados e seus
       tarefas correspondentes.
    4. Remove atribuições de robôs de itens e tarefas.
    5. Verifica se existem robôs ativos. Se não houver robôs ativos,
       habilita a tarefa periódica para verificação do robô.

    Returns:
    None
    """
    robots_disconnecteds = check_disconnected_robots()

    if robots_disconnecteds:
        change_status_inactive(robots_disconnecteds)
        items = get_items(robots_disconnecteds).all()
        if items:
            tasks = get_tasks_from_items(items)
            remove_robots([items, tasks])
            items = items.none()
            tasks = tasks.none()
    robots_active = get_active_robots()
    if not robots_active:
        periodic_task_check.enabled = True
        periodic_task_check.save()


# CREATING THE TASK: check_robots_every_minute

# Define the interval schedule for the periodic task
schedule_check, created_check = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.MINUTES,
)

# Try to retrieve the existing periodic task or create a new one
try:
    periodic_task_check = PeriodicTask.objects.get(
        name='check_robots_every_minute')
except PeriodicTask.DoesNotExist:
    # Create a new periodic task with the defined interval and settings
    periodic_task_check = PeriodicTask.objects.create(
        interval=schedule_check,
        name='check_robots_every_minute',
        task='robots.tasks.check_robots_every_minute',
        enabled=False,  # Disable the task initially
    )


@app.task
def check_robots_every_minute():
    """
    Tarefa de aipo para verificar robôs a cada minuto.

    Esta tarefa está programada para ser executada periodicamente e executa o seguinte
    ações:
    1. Se a tarefa para lidar com robôs desconectados estiver habilitada, ela desabilita
       e registra uma mensagem.
    2. Procura robôs ativos.
    3. Se houver robôs ativos, verifica se a memória não está atribuída
       Unid.
    4. Se a memória tiver itens não atribuídos, ela atribui os itens e tarefas
       para um robô e limpa a memória.
    5. Desativa a tarefa de verificar robôs ativos e permite que a tarefa lide
       robôs desconectados.
    6. Se não houver robôs ativos, habilita a tarefa para verificar robôs desconectados
       robôs.

    Retorna:
    Nenhum
    """
    if periodic_task_handle.enabled:
        periodic_task_handle.enabled = False
        periodic_task_handle.save()
    memory = get_memory()
    robots = get_active_robots()
    if robots:
        if not memory.items.exists():
            memory.items = get_items(robots=None).all()
            if memory.items.exists():
                robot = get_min_robot()
                memory.task = get_tasks_from_items(memory.items).all()
                assing_robots(memory.items, robot)
                assing_robots(memory.task, robot)
                memory.clear()
            periodic_task_check.enabled = False
            periodic_task_handle.enabled = True
            periodic_task_handle.save()
            periodic_task_check.enabled = False
            periodic_task_check.save()
