from backend.core.paths import DATABASE_URL

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["backend.database.models"],
            "default_connection": "default",
            "migrations": "backend.database.migrations"
        },
    },
}

