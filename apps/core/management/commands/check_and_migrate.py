from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.migrations.executor import MigrationExecutor
from django.db import connections, DEFAULT_DB_ALIAS


class Command(BaseCommand):
    help = "Verifica se há migrations pendentes e aplica se necessário."

    def handle(self, *args, **options):
        self.stdout.write("Verificando migrations pendentes...")

        connection = connections[DEFAULT_DB_ALIAS]
        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)

        if plan:
            self.stdout.write(self.style.WARNING("Migrations pendentes encontradas!"))
            self.stdout.write("Executando migrate...\n")
            call_command("migrate")
            self.stdout.write(self.style.SUCCESS("Migrate concluído com sucesso!"))
        else:
            self.stdout.write(self.style.SUCCESS("Nenhuma migration pendente."))
