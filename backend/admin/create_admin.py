import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

import asyncio

from tortoise import Tortoise
from fastapi_admin.utils import hash_password

from backend.core.paths import DATABASE_URL
from backend.database.models import Admin


async def main():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["backend.database.models"]},
        _enable_global_fallback=True,
    )

    admin = await Admin.create(
        username="admin",
        password_hash=hash_password("admin"),
        full_name="Administrator",
    )

    print(f"Admin created: {admin.username}")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())