from django.shortcuts import render

from django.db.models import Min
from django.db.models import Q

from django.utils import timezone

from hospedes import models


def index(request):
    hoje = timezone.now().date()
    mes = timezone.now().month

    hospedes_mes = (
        models.Hospede.objects
        .filter(
            Q(status='EM_ESTADIA') |
            Q(status='CHECKOUT_REALIZADO')
            )
        .filter(horario_checkin__month=mes)
        .count()
    )

    checkin_hoje = (
        models.Reserva.objects
        .filter(status_reserva='CONFIRMADO')
        .filter(horario_checkin__date=hoje)
        .order_by('horario_checkin')
    )[:5]

    checkout_hoje = (
        models.Reserva.objects
        .filter(status_reserva='CONFIRMADO')
        .filter(horario_checkout__date=hoje)
        .order_by('horario_checkout')
    )[:5]

    quartos_ocupados = (
        models.Hospede.objects
        .filter(status='EM_ESTADIA')
        .values_list('reservas__quartos__numero_quarto', flat=True)
    )

    num_quartos_ocupados = len(quartos_ocupados)

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
        'inicio_dashboard': 'Início da dashboard',
        'nome_pagina': 'Informações do hotel',
        'reservas': reservas_proximas,
        'hospedes': hospedes,
        'checkin_hoje': checkin_hoje,
        'checkout_hoje': checkout_hoje,
        'ocupacao_hoje': num_quartos_ocupados,
        'quartos_ocupados': quartos_ocupados,
        'hospedes_mes': hospedes_mes,
    }

    return render(
        request,
        'index.html',
        contexto
    )
