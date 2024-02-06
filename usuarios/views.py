from django.shortcuts import render
from hospedes import models


def index(request):

    reservas = models.Reserva.objects.filter(status_reserva='CONFIRMADO')

    contexto = {
        'reservas': reservas
    }

    return render(
        request,
        'index.html',
        contexto
    )
