from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin
)
from rest_framework.viewsets import GenericViewSet

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome
from planetarium.serializers import ShowThemeSerializer, AstronomyShowSerializer, AstronomyShowListSerializer, \
    AstronomyShowDetailSerializer, PlanetariumDomeSerializer


class ShowThemeViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    serializer_class = ShowThemeSerializer
    queryset = ShowTheme.objects.all()


class AstronomyShowViewSet(
    viewsets.ModelViewSet
):
    queryset = AstronomyShow.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AstronomyShowListSerializer
        elif self.action == 'retrieve':
            return AstronomyShowDetailSerializer
        return AstronomyShowSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            return queryset.prefetch_related("themes")
        else:
            return queryset


class PlanetariumDomeViewSet(
    viewsets.ModelViewSet
):
    serializer_class = PlanetariumDomeSerializer
    queryset = PlanetariumDome.objects.all()
