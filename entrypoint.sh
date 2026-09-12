#!/bin/bash

# Остановка скрипта при первой же ошибке
set -e

echo "==> Применение миграций БД..."
python manage.py migrate --noinput

echo "==> Сбор статики (для Tailwind / Unfold)..."
python manage.py collectstatic --noinput

echo "==> Создание суперпользователя (если его нет)..."
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Суперпользователь '{username}' успешно создан.")
else:
    print(f"Суперпользователь '{username}' уже существует.")
EOF

# Запуск основного процесса (Gunicorn или Uvicorn)
exec "$@"