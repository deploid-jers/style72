from tortoise import fields
from tortoise.models import Model


class Admin(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.TextField(source_field="password_hash")
    full_name = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "admins"

    def __str__(self) -> str:
        return self.username


class Category(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "categories"

    def __str__(self) -> str:
        return self.name


class Service(Model):
    id = fields.IntField(primary_key=True)

    category = fields.ForeignKeyField(
        "models.Category",
        related_name="services",
        on_delete=fields.CASCADE,
    )

    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    duration_minutes = fields.IntField()
    price = fields.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    is_active = fields.BooleanField(default=True)

    specialists: fields.ManyToManyRelation["Specialist"]

    class Meta:
        table = "services"

    def __str__(self) -> str:
        return self.name


class Specialist(Model):
    id = fields.IntField(primary_key=True)

    full_name = fields.CharField(max_length=255)
    specialization = fields.CharField(max_length=255)
    bio = fields.TextField(null=True)
    photo_url = fields.TextField(null=True)
    is_active = fields.BooleanField(default=True)

    services = fields.ManyToManyField(
        "models.Service",
        related_name="specialists",
        through="specialist_services",
    )

    class Meta:
        table = "specialists"

    def __str__(self) -> str:
        return self.full_name


class SpecialistSchedule(Model):
    id = fields.IntField(primary_key=True)

    specialist = fields.ForeignKeyField(
        "models.Specialist",
        related_name="schedules",
        on_delete=fields.CASCADE,
    )

    work_date = fields.DateField()
    start_time = fields.TimeField()
    end_time = fields.TimeField()

    class Meta:
        table = "specialist_schedules"
        unique_together = (("specialist", "work_date"),)
        indexes = [
            ("work_date",),
        ]

    def __str__(self) -> str:
        return f"{self.specialist.full_name} — {self.work_date}"


class Appointment(Model):
    id = fields.IntField(primary_key=True)

    type = fields.CharField(
        max_length=20,
        choices=[
            ("call_back", "Обратный звонок"),
            ("online_booking", "Онлайн-запись"),
        ],
    )

    client_name = fields.CharField(max_length=255)
    client_phone = fields.CharField(max_length=50)
    client_comment = fields.TextField(null=True)

    specialist = fields.ForeignKeyField(
        "models.Specialist",
        related_name="appointments",
        null=True,
        on_delete=fields.SET_NULL,
    )

    service = fields.ForeignKeyField(
        "models.Service",
        related_name="appointments",
        null=True,
        on_delete=fields.SET_NULL,
    )

    appointment_date = fields.DateField(null=True)
    appointment_time = fields.TimeField(null=True)

    status = fields.CharField(
        max_length=20,
        default="new",
        choices=[
            ("new", "Новая"),
            ("confirmed", "Подтверждена"),
            ("completed", "Завершена"),
            ("cancelled", "Отменена"),
        ],
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "appointments"
        indexes = [
            ("appointment_date", "appointment_time"),
            ("status",),
        ]

    def __str__(self) -> str:
        return f"{self.client_name} — {self.type}"


