import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.core.settings')

application = get_wsgi_application()



from apps.items.tasks import get_items_first_time_run_server

# ###### First-time Execution ####################

"""
Esta seção contém código que é executado quando o aplicativo
corre pela primeira vez.

É usado para obter itens não atribuídos.

Este bloco de código é executado apenas uma vez durante a inicialização inicial
do aplicativo.
"""

try:
    get_items_first_time_run_server()
except Exception as e:
    print(f"Error running get_items_first_time_run_server: {e}")

# ##################################################




