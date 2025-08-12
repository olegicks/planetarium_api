from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from planetarium.views import ShowThemeViewSet, AstronomyShowViewSet, PlanetariumDomeViewSet, ShowSessionViewSet, \
    ReservationViewSet
from planetarium_project import settings

router = DefaultRouter()
router.register("show_themes", ShowThemeViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)
router.register("show_sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)