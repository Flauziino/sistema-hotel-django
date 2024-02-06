from django.shortcuts import render
from hospedes import models


def index(request):

    reservas = models.Reserva.objects.filter(status_reserva='CONFIRMADO')
    hospedes = models.Hospede.objects.filter(status='EM_ESTADIA')

    contexto = {
        'reservas': reservas,
        'hospedes': hospedes
    }

    return render(
        request,
        'index.html',
        contexto
    )
