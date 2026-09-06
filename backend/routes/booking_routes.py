from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.core.paths import TEMPLATES_DIR

router = APIRouter(prefix="/booking", tags=['booking'])
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(
        request,
        "booking.html"
    )