from django.contrib import admin

from planetarium.models import ShowTheme, Ticket, Reservation, PlanetariumDome, ShowSession, AstronomyShow

# Register your models here.
admin.site.register(ShowTheme)
admin.site.register(Ticket)
admin.site.register(Reservation)
admin.site.register(PlanetariumDome)
admin.site.register(ShowSession)
admin.site.register(AstronomyShow)