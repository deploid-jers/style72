from tortoise import Tortoise

from backend.core.paths import DATABASE_URL

async def init_db() -> None:
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={
            "models": ["backend.database.models"],
        },
        _enable_global_fallback=True,
    )

async def close_db() -> None:
    await Tortoise.close_connections()