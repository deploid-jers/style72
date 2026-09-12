import os
import sys
import subprocess
from backend.settings.constants import *

def run_command(command, description):
    """Вспомогательная функция для запуска команд manage.py"""
    print(f"--> {description}...")
    result = subprocess.run([sys.executable, "manage.py"] + command)
    if result.returncode != 0:
        print(f"[X] Ошибка при выполнении: {description}")
        return False
    return True

def main():
    print("=" * 50)
    print("       Запуск Django проекта (Development)      ")
    print("=" * 50)

    if not os.path.exists("manage.py"):
        print("[X] Ошибка: файл manage.py не найден в текущей директории.")
        print("Убедитесь, что запускаете main.py из корня проекта.")
        sys.exit(1)

    if not run_command(["migrate"], "Применение миграций БД"):
        sys.exit(1)


    print(f"\n[+] Запуск сервера на {APP_URL}")
    print("Нажмите Ctrl+C для остановки.\n")
    
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", f"{APP_HOST}:{APP_PORT}"])
    except KeyboardInterrupt:
        print("\n\n[!] Сервер успешно остановлен.")

if __name__ == "__main__":
    main()