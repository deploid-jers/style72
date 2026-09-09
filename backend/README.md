## Выбранный стек для бекенда

| Компонент                    | Выбор                                                   |
| ---------------------------- | ------------------------------------------------------- |
| API                          | **FastAPI**                                             |
| Admin                        | **fastapi-admin**                                       |
| ORM                          | **Tortoise ORM**                                        |
| DB                           | **SQLite**                                          |
| Cache/session infrastructure | **Redis**                                               |
| DB migrations                | **Tortoise migrations**                                 |
| Admin UI                     | **Tabler через fastapi-admin**                          |
| Deployment                   | **Docker Compose → затем Docker/K8s при необходимости** |
| Reverse proxy                | **Caddy / Nginx / Traefik**                             |
| HTTPS                        | **обязательно**                                         |


Перед началом разработки необходимо разработать схему нашей базы данных


## План разработки
1. Собираем базовый проект на: FastAPI, Docker ✓
2. Подключаем Tortoise ORM, и создаем одну простую модель ✓
3. Разбираемся с миграциями в БД
4. Добавляем Redis
5. Добавляем сам FastAPI админку
6. Аутентификация админа
7. Разрешения
8. Первый CRUD
9. Основная бизнес логика
10. Проходим по безопасности: Security hardening
11. Добавляем логгирование для админки
12. Тесты
