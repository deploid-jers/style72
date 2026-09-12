from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from unfold.contrib.filters.admin import RangeDateFilter
from django import forms
from datetime import datetime, timedelta
from django.forms import widgets
from django.db import models

from .models import (
    Category,
    Service,
    Specialization,
    Specialist,
    SpecialistSchedule,
    Appointment,
)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "duration_minutes",
        "is_active",
    )
    list_filter = ("category", "is_active",)
    search_fields = ("name", "description")


@admin.register(Specialization)
class SpecializationAdmin(ModelAdmin):
    list_display = (
        "name",
    )
    list_filter = (
        "name",
    )
    search_fields = ("name", "")


class SpecialistScheduleInline(TabularInline):
    model = SpecialistSchedule
    compressed_fields = True
    extra = 1

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/npm/flatpickr',
            'core/js/timepicker.js', # Ваш скрипт
        )

@admin.register(Specialist)
class SpecialistAdmin(ModelAdmin):
    list_display = (
        "full_name",
        "specialization",
        "is_active",
    )
    list_filter = ("specialization", "is_active")
    search_fields = ("full_name", "specialization", "bio")
    inlines = [SpecialistScheduleInline]
    filter_horizontal = ('services',)

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/npm/flatpickr',
            'core/js/timepicker.js', # Ваш скрипт
        )


@admin.register(SpecialistSchedule)
class SpecialistScheduleAdmin(ModelAdmin):
    list_display = (
        "specialist",
        "work_date",
        "start_time",
        "end_time",
    )
    list_filter = ( 
        "specialist",
        ("work_date", RangeDateFilter),
        )
    search_fields = ("specialist",)

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/npm/flatpickr',
            'core/js/timepicker.js', # Ваш скрипт
        )


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = "__all__"


    def clean(self):
        cleaned_data = super().clean()

        appointment_type = cleaned_data.get("type") 

        if appointment_type == Appointment.AppointmentType.ONLINE_BOOKING:
            required_fields = {
                "specialist": "Специалист",
                "service": "Услуга",
                "appointment_date": "Дата записи",
                "appointment_time": "Время записи",
            }

            for field, label in required_fields.items():
                if not cleaned_data.get(field):
                    self.add_error(field, f"{label} обязательна для онлайн-записи.")

            specialist = cleaned_data.get("specialist")
            service = cleaned_data.get("service")
            appointment_date = cleaned_data.get("appointment_date")
            appointment_time = cleaned_data.get("appointment_time")

            if specialist and service and appointment_date and appointment_time:
                start = datetime.combine(
                    appointment_date,
                    appointment_time,
                )

                end = start + timedelta(
                    minutes=service.duration_minutes
                )

                schedule = SpecialistSchedule.objects.filter(
                    specialist=specialist,
                    work_date=appointment_date,
                ).first()


                if not schedule:
                    self.add_error(
                        "appointment_date",
                        "У специалиста нет рабочего расписания на эту дату.",
                    )
                elif start.time() < schedule.start_time or end.time() > schedule.end_time:
                    self.add_error(
                        "appointment_time",
                        "Запись не попадает в рабочее время специалиста.",
                    )

                existing_appointments = Appointment.objects.filter(
                    specialist=specialist,
                    appointment_date=appointment_date,
                    status__in=[
                        Appointment.Status.NEW,
                        Appointment.Status.CONFIRMED,
                    ],
                ).exclude(pk=self.instance.pk)

                for appointment in existing_appointments:
                    existing_start = datetime.combine(
                        appointment.appointment_date,
                        appointment.appointment_time,
                    )

                    existing_end = existing_start + timedelta(
                        minutes=appointment.service.duration_minutes
                    )

                    if start < existing_end and end > existing_start:
                        self.add_error(
                            "appointment_time",
                            "Специалист уже занят в это время.",
                        )
                        break


        if appointment_type == Appointment.AppointmentType.CALLBACK:
            cleaned_data["specialist"] = None
            cleaned_data["service"] = None
            cleaned_data["appointment_date"] = None
            cleaned_data["appointment_time"] = None

        return cleaned_data


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    readonly_fields = ("created_at",)

    list_display = (
        "client_name",
        "client_phone",
        "type",
        "service",
        "specialist",
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "type",
        ("appointment_date", RangeDateFilter),
        "specialist",
        "service",
    )
    search_fields = (
        "client_name",
        "client_phone",
    )
    ordering = ("-created_at",)

    autocomplete_fields = (
            "specialist",
        )

    list_editable = ("status",)

    fieldsets = (
        (
            "Клиент",
            {
                "fields": (
                    "client_name",
                    "client_phone",
                    "client_comment",
                )
            },
        ),
        (
            "Заявка",
            {
                "fields": (
                    "type",
                    "status",
                )
            },
        ),
        (
            "Онлайн-запись",
            {
                "fields": (
                    "specialist",
                    "service",
                    "appointment_date",
                    "appointment_time",
                )
            },
        ),
        (
            "Система",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )



    class Media:
        js = ("core/js/appointment_form.js",'https://cdn.jsdelivr.net/npm/flatpickr', 'core/js/timepicker.js', "core/js/status_color.js") 
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',
                "core/css/status_colors.css",
            )
        }


    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = AppointmentForm
        return super().get_form(request, obj, **kwargs)


    # @admin.display(description="Статус")
    # def colored_status(self, obj):
    #     colors = {
    #         "new": "#ffc107",
    #         "confirmed": "#198754",
    #         "completed": "#0d6efd",
    #         "cancelled": "#dc3545",
    #     }

    #     color = colors.get(obj.status, "#6c757d")

    #     return format_html(
    #         '<strong style="color: {};">{}</strong>',
    #         color,
    #         obj.get_status_display(),
    #     )


    # formfield_overrides = {
    #     # Заменяем стандартный виджет времени на нативный HTML5 timepicker
    #     models.TimeField: {
    #         'widget': widgets.TimeInput(
    #             attrs={
    #                 'type': 'time',
    #                 'step': '900',  # Шаг в секундах (900 сек = 15 минут, т.е. 10:00, 10:15, 10:30)
    #                 'class': 'vTimeField',
    #             }
    #         )
    #     },
    # }