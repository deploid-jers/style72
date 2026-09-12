import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Полная первичная инициализация проекта"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("==> Выполнение миграций..."))
        call_command("migrate")

        self.stdout.write(self.style.WARNING("==> Создание суперпользователя..."))
        User = get_user_model()
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@admin.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь '{username}' создан! (Пароль: {password})"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь '{username}' уже существует."))

        self.stdout.write(self.style.WARNING("==> Сбор статики..."))
        call_command("collectstatic", interactive=False)

        self.stdout.write(self.style.SUCCESS("\nИнициализация успешно завершена! Можно запускать runserver."))