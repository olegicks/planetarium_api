from django.urls import path, include
from rest_framework.routers import DefaultRouter

from planetarium.views import ShowThemeViewSet

router = DefaultRouter()
router.register("show_themes", ShowThemeViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
