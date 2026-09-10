from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="services",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Specialist(models.Model):
    full_name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    services = models.ManyToManyField(
        Service,
        related_name="specialists",
    )

    def __str__(self):
        return self.full_name


class SpecialistSchedule(models.Model):
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    work_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["specialist", "work_date"],
                name="unique_specialist_work_date",
            ),
        ]

    def __str__(self):
        return f"{self.specialist} — {self.work_date}"


class Appointment(models.Model):

    class AppointmentType(models.TextChoices):
        CALLBACK = "call_back", "Обратный звонок"
        ONLINE_BOOKING = "online_booking", "Онлайн-запись"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        CONFIRMED = "confirmed", "Подтверждена"
        COMPLETED = "completed", "Завершена"
        CANCELLED = "cancelled", "Отменена"

    type = models.CharField(
        max_length=20,
        choices=AppointmentType.choices,
    )

    client_name = models.CharField(max_length=255)
    client_phone = models.CharField(max_length=50)
    client_comment = models.TextField(blank=True, null=True)

    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
    )

    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["appointment_date", "appointment_time"],
                name="idx_appointments_date",
            ),
            models.Index(
                fields=["status"],
                name="idx_appointments_status",
            ),
        ]

    def __str__(self):
        return f"{self.client_name} — {self.appointment_date}"