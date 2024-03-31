from rest_framework import serializers

from collections import defaultdict

from .models import Reserva, Hospede

from quartos.models import Quarto
from portaria.models import Portaria


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = [
            'id', 'forma_pagamento', 'nome_hospede', 'status_reserva',
            'registrado_por', 'horario_checkin', 'horario_checkout',
            'quartos'
        ]

    nome_hospede = serializers.CharField(read_only=True)
    registrado_por = serializers.StringRelatedField()
    forma_pagamento = serializers.StringRelatedField()


class HospedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospede
        fields = [
            'id', 'nome_completo', 'telefone',
            'cpf', 'email', 'horario_checkin', 'registrado_por'
        ]

        registrado_por = serializers.StringRelatedField(
            source='portaria'
        )

        horario_checkin = serializers.DateTimeField()


class QuartoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarto
        fields = [
            'id', 'numero_quarto', 'tipo_quarto'
        ]


class PortariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portaria
        fields = [
            'id', 'usuario'
        ]
