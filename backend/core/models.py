from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone



class Category(models.Model):
    name = models.CharField("Название категории", max_length=255)
    description = models.TextField("Описание категории", blank=True, null=True)
    is_active = models.BooleanField("Статус активности", default=True)

    class Meta:
        verbose_name = "Категория"        
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="services",
    )
    name = models.CharField("Название услуги", max_length=255)
    description = models.TextField("Описание услуги", blank=True, null=True)
    duration_minutes = models.PositiveIntegerField("Количество минут")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    is_active = models.BooleanField("Статус активности", default=True)

    class Meta:
        verbose_name = "Услуга"        
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField("Название специальности", max_length=255)
    description = models.TextField("Описание специальности", blank=True, null=True)

    class Meta:
        verbose_name = "Специальность"        
        verbose_name_plural = "Специальности"

    def __str__(self):
            return self.name


class Specialist(models.Model):
    full_name = models.CharField("Фамилия Имя Отчество", max_length=255)
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        related_name="specialists",
        null=True,
        verbose_name="Специальность"
    )
    bio = models.TextField("О себе", blank=True, null=True)
    photo_url = models.URLField("Ссылка на фото", blank=True, null=True)
    is_active = models.BooleanField("Статус активности", default=True)
    services = models.ManyToManyField(
        Service,
        related_name="specialists",
        verbose_name="Предоставляемые услуги",
    )

    class Meta:
        verbose_name = "Специалист"        
        verbose_name_plural = "Специалисты"

    def __str__(self):
        return self.full_name


class SpecialistSchedule(models.Model):
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Специалист"
    )
    work_date = models.DateField("Дата смены")
    start_time = models.TimeField("Время начала работы")
    end_time = models.TimeField("Время окончания работы")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["specialist", "work_date"],
                name="unique_specialist_work_date",
            ),
        ]
        verbose_name = "Расписание специалиста"        
        verbose_name_plural = "Расписание специалистов"

    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(
                    "Время начала должно быть раньше времени окончания."
                )

        if self.work_date and self.work_date < timezone.localdate():
            raise ValidationError(
                "Нельзя создать расписание на прошедшую дату."
            )

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
        verbose_name="Тип записи"
    )

    client_name = models.CharField("ФИО клиента", max_length=255)
    client_phone = models.CharField("Номер телефона клиента", max_length=50)
    client_comment = models.TextField("Комментарий от клиента", blank=True, null=True)

    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name="Специалист"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name="Предоставляемая услуга"
    )

    appointment_date = models.DateField("Дата записи", null=True, blank=True)
    appointment_time = models.TimeField("Время записи", null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус записи"
    )

    created_at = models.DateTimeField("Дата создания записи", default=timezone.localdate)

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

        verbose_name = "Запись"         
        verbose_name_plural = "Записи"

    def __str__(self):
        return f"{self.client_name} — {self.appointment_date}"