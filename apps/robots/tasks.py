from django_celery_beat.models import PeriodicTask, IntervalSchedule
from apps.tasks.utils import get_tasks_from_items
from apps.items.utils import get_items
from apps.robots.utils import (check_disconnected_robots, change_status_inactive,
                          assing_robots, get_min_robot, get_active_robots,
                          remove_robots)
from apps.core.celery import app
from apps.core.memory_manager import get_memory

# Remover intervalos duplicados se existirem
IntervalSchedule.objects.filter(every=3, period=IntervalSchedule.MINUTES).exclude(pk=IntervalSchedule.objects.filter(every=3, period=IntervalSchedule.MINUTES).first().pk).delete()

# Obter ou criar um cronograma de intervalo para executar a tarefa a cada 3 minutos
schedule_handle, _ = IntervalSchedule.objects.get_or_create(
    every=3,
    period=IntervalSchedule.MINUTES,
)

# Tente obter uma tarefa periódica existente ou crie uma nova
periodic_task_handle, _ = PeriodicTask.objects.update_or_create(
    name='handle_disconnected_robots',
    defaults={
        'interval': schedule_handle,
        'task': 'robots.tasks.handle_disconnected_robots',
        'enabled': True,
    },
)

@app.task
def handle_disconnected_robots():
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

# Remover intervalos duplicados se existirem
IntervalSchedule.objects.filter(every=1, period=IntervalSchedule.MINUTES).exclude(pk=IntervalSchedule.objects.filter(every=1, period=IntervalSchedule.MINUTES).first().pk).delete()

# Obter ou criar o intervalo de agendamento para a tarefa periódica
schedule_check, _ = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.MINUTES,
)

# Tente obter ou criar a tarefa periódica para verificar robôs
periodic_task_check, _ = PeriodicTask.objects.update_or_create(
    name='check_robots_every_minute',
    defaults={
        'interval': schedule_check,
        'task': 'robots.tasks.check_robots_every_minute',
        'enabled': False,  # A tarefa começa desativada
    },
)

@app.task
def check_robots_every_minute():
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
