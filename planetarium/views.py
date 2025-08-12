from django.template.defaulttags import querystring
from django.db.models import Count, F
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Reservation
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import ShowThemeSerializer, AstronomyShowSerializer, AstronomyShowListSerializer, \
    AstronomyShowDetailSerializer, PlanetariumDomeSerializer, ShowSessionDetailSerializer, ShowSessionSerializer, \
    ShowSessionListSerializer, ReservationSerializer, ReservationListSerializer, AstronomyImageSerializer


class ShowThemeViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet
):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    serializer_class = ShowThemeSerializer
    queryset = ShowTheme.objects.all()


class AstronomyShowViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    queryset = AstronomyShow.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AstronomyShowListSerializer
        elif self.action == 'retrieve':
            return AstronomyShowDetailSerializer
        elif self.action == "upload_image":
            return AstronomyImageSerializer
        return AstronomyShowSerializer

    @action(
        methods=["post"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        astronomy_show = self.get_object()
        serializer = self.get_serializer(astronomy_show, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()

        themes = self.request.query_params.get("themes")
        title = self.request.query_params.get("title")

        if themes:
            themes_ids = [int(str_id) for str_id in themes.split(",") if str_id.isdigit()]
            queryset = queryset.filter(themes__id__in=themes_ids)

        if title:
            queryset = queryset.filter(title__icontains=title)


        if self.action in ['list', 'retrieve']:
            return queryset.prefetch_related("themes")
        return queryset.distinct()


class PlanetariumDomeViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,

):
    serializer_class = PlanetariumDomeSerializer
    queryset = PlanetariumDome.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ShowSessionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    serializer_class = ShowSessionSerializer
    queryset = ShowSession.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShowSessionListSerializer
        elif self.action == 'retrieve':
            return ShowSessionDetailSerializer
        return ShowSessionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        astronomy_show = self.request.query_params.get("astronomy_show")
        date = self.request.query_params.get("date")

        if astronomy_show:
            queryset = queryset.filter(astronomy_show_id=astronomy_show)
        if date:
            queryset = queryset.filter(show_time__date=date)

        if self.action == "list":
            queryset = queryset.annotate(
                tickets_available=F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row") - Count("tickets")
            )

        if self.action in ['list', 'retrieve']:
            return queryset.select_related("astronomy_show", "planetarium_dome")
        return queryset


class ReservationPagination(
    PageNumberPagination
):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ReservationViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
):
    queryset = Reservation.objects.all()
    pagination_class = ReservationPagination
    serializer_class = ReservationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'list'):
            return ReservationListSerializer
        return ReservationSerializer
