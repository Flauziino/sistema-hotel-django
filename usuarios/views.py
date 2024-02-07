from django.shortcuts import render
from hospedes import models


def index(request):

    reservas = (
        models.Reserva.objects
        .filter(status_reserva='CONFIRMADO')
        .order_by('-pk')
        )

    hospedes = (
        models.Hospede.objects
        .filter(status='EM_ESTADIA')
        .order_by('-pk')
        )

    contexto = {
        'reservas': reservas,
        'hospedes': hospedes,
    }

    return render(
        request,
        'index.html',
        contexto
    )
