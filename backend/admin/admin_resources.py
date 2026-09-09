from fastapi_admin.resources import Model
from fastapi_admin.resources import Field

from backend.database.models import Category


class CategoryResource(Model):
    label = "Категории"
    model = Category

    fields = [
        Field(name="id", label="ID"),
        Field(name="name", label="Название"),
    ]