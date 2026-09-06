from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.core.constants import *
from backend.core.paths import *

from backend.routes import home_routes, about_routes, booking_routes, prices_routes, contacts_routes, services_routes, team_routes

def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name='static')

    app.include_router(home_routes.router)
    app.include_router(about_routes.router)
    app.include_router(booking_routes.router)
    app.include_router(prices_routes.router)
    app.include_router(contacts_routes.router)
    app.include_router(services_routes.router)
    app.include_router(team_routes.router)


    return app

app = create_app()