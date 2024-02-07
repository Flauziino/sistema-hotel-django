from django.shortcuts import render
from django.db.models import Min

from hospedes import models


def index(request):

    reservas = (
        models.Reserva.objects
        .filter(status_reserva='CONFIRMADO')
        .order_by('-pk')[:6]
        )

    reservas_proximas = (
        models.Reserva.objects
        .filter(status_reserva='CONFIRMADO')
        .annotate(proxima_checkin=Min('horario_checkin'))
        .order_by('proxima_checkin')
    )[:5]

    hospedes = (
        models.Hospede.objects
        .filter(status='EM_ESTADIA')
        .order_by('-pk')[:6]
        )

    contexto = {
        'nome_pagina': 'Informações do hotel',
        'reservas': reservas_proximas,
        'hospedes': hospedes,
    }

    return render(
        request,
        'index.html',
        contexto
    )
