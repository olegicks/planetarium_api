from rest_framework.routers import DefaultRouter
from django.urls import path, include

from planetarium.views import ShowThemeViewSet, AstronomyShowViewSet

router = DefaultRouter()
router.register("show_themes", ShowThemeViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)

urlpatterns = [
    path("", include(router.urls)),
]