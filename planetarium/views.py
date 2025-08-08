from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin
)
from rest_framework.viewsets import GenericViewSet

from planetarium.models import ShowTheme
from planetarium.serializers import ShowThemeSerializer


class ShowThemeViewSet(
    CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet
):
    serializer_class = ShowThemeSerializer
    queryset = ShowTheme.objects.all()
