import os
from django.contrib.auth import get_user_model
from django.core.management import base


class Command(base.BaseCommand):
    help = "Cria um superusuário automaticamente caso ele não exista"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not User.objects.filter(username=username).exists():
            print(f"👤 Criando superusuário: {username}")
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
        else:
            print("✅ Superusuário já existe. Pulando criação...")
