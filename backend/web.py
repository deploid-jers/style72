import sys
from backend.core.paths import BASE_DIR
sys.path.insert(0, str(BASE_DIR / "vendor"))

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles

from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.depends import get_current_admin
from fastapi_admin.template import templates
from redis.asyncio import Redis

from backend.core.constants import *
from backend.core.paths import *

from backend.routes import home_routes, about_routes, booking_routes, prices_routes, contacts_routes, services_routes, team_routes

from contextlib import asynccontextmanager
from tortoise import Tortoise

from backend.database.db import init_db, close_db
from backend.database.models import Admin

from backend.admin.admin_resources import CategoryResource

login_provider = UsernamePasswordProvider(admin_model=Admin)
redis = Redis.from_url(REDIS_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    await admin_app.configure(redis=redis, admin_path="/admin", providers=[login_provider])
    
    yield

    await close_db()

@admin_app.get("/", dependencies=[Depends(get_current_admin)])
async def admin_home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
    )

def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, lifespan=lifespan)
    admin_app.register_resources(CategoryResource)

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name='static')

    app.mount("/admin", admin_app)
    app.include_router(home_routes.router)
    app.include_router(about_routes.router)
    app.include_router(booking_routes.router)
    app.include_router(prices_routes.router)
    app.include_router(contacts_routes.router)
    app.include_router(services_routes.router)
    app.include_router(team_routes.router)


    return app

app = create_app()