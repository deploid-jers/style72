FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости и исходный код
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Делаем скрипт исполняемым и задаем его как точку входа
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Стандартная команда запуска приложения
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]