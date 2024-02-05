from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import HospedeForm


# Apos a criaçao do app Quartos
# é preciso voltar e realizar algumas verificaçoes
def registrar_hospede(request):

    form = HospedeForm()

    if request.method == "POST":

        if form.is_valid():
            hospede = form.save(commit=False)

            hospede.registrado_por = request.user.portaria
            hospede.save()

            messages.success(
                request,
                "Check-In do hóspede registrado com sucesso!"
            )

            return redirect(
                "usuarios:index"
            )

    contexto = {
        "nome_pagina": "Registrar hóspede",
        "form": form
    }

    return render(
        request,
        "registrar_hospede.html",
        contexto
    )
