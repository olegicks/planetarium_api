from rest_framework.routers import DefaultRouter
from django.urls import path, include

from planetarium.views import ShowThemeViewSet, AstronomyShowViewSet, PlanetariumDomeViewSet, ShowSessionViewSet

router = DefaultRouter()
router.register("show_themes", ShowThemeViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)
router.register("show_sessions", ShowSessionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]