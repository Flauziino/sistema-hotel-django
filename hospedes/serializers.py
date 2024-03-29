from rest_framework import serializers

from collections import defaultdict

from .models import Reserva, Hospede


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva


class HospedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospede
