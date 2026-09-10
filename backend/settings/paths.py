from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"

DATABASE_DIR = BASE_DIR / "backend" / "database"
DATABASE_URL = f"sqlite:///{str(DATABASE_DIR / "data" / "app.db")}"

REDIS_URL = "redis://localhost:6379/0"