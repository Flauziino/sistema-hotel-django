from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import ReservaForm


# Apos a criaçao do app Quartos
# é preciso voltar e realizar algumas verificaçoes
def realizar_reserva(request):

    form = ReservaForm()

    if request.method == "POST":

        form = ReservaForm(request.POST)

        if form.is_valid():
            reserva = form.save(commit=False)

            reserva.registrado_por = request.user.portaria
            reserva.save()

            messages.success(
                request,
                "Check-In do hóspede registrado com sucesso!"
            )

            return redirect(
                "usuarios:index"
            )

    contexto = {
        "nome_pagina": "Realizar reserva",
        "form": form
    }

    return render(
        request,
        "realizar_reserva.html",
        contexto
    )
