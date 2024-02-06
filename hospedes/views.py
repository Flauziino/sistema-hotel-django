from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import ReservaForm
from .models import Hospede, Reserva


# Apos a criaçao do app Quartos
# é preciso voltar e realizar algumas verificaçoes
def realizar_reserva(request):
    form = ReservaForm()

    if request.method == "POST":
        form = ReservaForm(request.POST)

        if form.is_valid():
            # Inicialmente criar um novo hospede
            novo_hospede = Hospede.objects.create(
                nome_completo=form.cleaned_data['nome_completo'],
                telefone=form.cleaned_data['telefone'],
                cpf=form.cleaned_data['cpf'],
                email=form.cleaned_data['email'],
                horario_checkin=form.cleaned_data['horario_checkin'],
            )

            # Criar reserva associada ao novo hospede
            reserva = form.save(commit=False)
            reserva.nome_hospede = novo_hospede
            reserva.registrado_por = request.user.portaria
            reserva.status_reserva = 'CONFIRMADO'
            reserva.save()

            # atualizar o status do novo hospede
            novo_hospede.status = 'AGUARDANDO_CHECKIN'
            novo_hospede.save()

            messages.success(
                request,
                "Reserva do hóspede registrado com sucesso!"
            )

            return redirect(
                "usuarios:index"
            )

    contexto = {
        "form": form,
    }

    return render(
        request,
        "realizar_reserva.html",
        contexto
    )
