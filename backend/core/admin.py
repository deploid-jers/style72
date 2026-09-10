from django.contrib import admin

from .models import (
    Category,
    Service,
    Specialist,
    SpecialistSchedule,
    Appointment,
)


admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Specialist)
admin.site.register(SpecialistSchedule)
admin.site.register(Appointment)