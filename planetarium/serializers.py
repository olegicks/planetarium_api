from django.db import transaction
from rest_framework import serializers

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Ticket, Reservation


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "image", "themes")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    themes = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")


class AstronomyShowDetailSerializer(AstronomyShowSerializer):
    themes = ShowThemeSerializer(many=True, read_only=True)


class AstronomyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "image")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(read_only=True)
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionDetailSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowSerializer(read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)

    taken_places = serializers.SerializerMethodField()
    class Meta:
        model = ShowSession
        fields = ("id", "show_time", "astronomy_show", "planetarium_dome", "taken_places")

    def get_taken_places(self, obj):
        return list(obj.tickets.all().values("row", "seat"))


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show_title = serializers.CharField(source="astronomy_show.title", read_only=True)

    astronomy_show_image = serializers.ImageField(source="astronomy_show.image", read_only=True)

    planetarium_dome_name = serializers.CharField(
        source="planetarium_dome.name",
        read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)
    planetarium_dome_capacity = serializers.IntegerField(
        source="planetarium_dome.capacity",
        read_only=True
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show_title",
            "show_time",
            "planetarium_dome_name",
            "planetarium_dome_capacity",
            "tickets_available",
            "astronomy_show_image",
        )


class TicketSerializer(serializers.ModelSerializer):
    show_session = ShowSessionListSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session")


class TicketCreateSerializer(serializers.ModelSerializer):
    show_session = serializers.PrimaryKeyRelatedField(
        queryset=ShowSession.objects.all()
    )
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketCreateSerializer(many=True, write_only=True)
    tickets_info = TicketSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "tickets_info", "created_at")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets", [])
        user = self.context["request"].user

        with transaction.atomic():
            reservation = Reservation.objects.create(user=user)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
        return reservation
