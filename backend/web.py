from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.core.constants import *
from backend.core.paths import *

def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name='static')

    return app

app = create_app()