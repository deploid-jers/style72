from django.shortcuts import render
from django.http import JsonResponse

from backend.core.models import Specialist

def specialist_services(request, specialist_id):
    specialist = Specialist.objects.get(pk=specialist_id)

    services = specialist.services.values(
        "id", "name"
    )

    return JsonResponse(list(services), safe=False) 


def home_view(request):
    return render(request, "home.html")

def services_view(request):
    return render(request, "services.html")

def team_view(request):
    return render(request, "team.html")

def prices_view(request):
    return render(request, "prices.html")

def about_view(request):
    return render(request, "about.html")

def contacts_view(request):
    return render(request, "contacts.html")

def booking_view(request):
    return render(request, "booking.html")