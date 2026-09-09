from tortoise import fields
from tortoise.models import Model

## Тут пропишем все схемы из БД

class Admins(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=255)
    password_hash = fields.TextField()
    full_name = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "admins"

    def __str__(self) -> str:
        return self.username