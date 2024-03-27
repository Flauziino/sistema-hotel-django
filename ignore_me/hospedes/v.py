from django.db import transaction
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from hospedes.forms import ReservaForm
from hospedes.models import Hospede, Reserva


@login_required
def realizar_reserva(request):
    form = ReservaForm()

    if request.method == "POST":
        form = ReservaForm(request.POST)

        if form.is_valid():

            # Criar o hospede
            novo_hospede = Hospede.objects.create(
                nome_completo=form.cleaned_data['nome_completo'],
                telefone=form.cleaned_data['telefone'],
                cpf=form.cleaned_data['cpf'],
                email=form.cleaned_data['email'],
                status='AGUARDANDO_CHECKIN'
            )

            # Criar a reserva associada ao novo hospede
            with transaction.atomic():
                reserva = Reserva.objects.create(
                    nome_hospede=novo_hospede,
                    registrado_por=request.user.portaria,
                    status_reserva='CONFIRMADO',
                )

                reserva.quartos.set(form.cleaned_data['quartos'])

                reserva.horario_checkin = (
                    form.cleaned_data['horario_checkin']
                )

                reserva.horario_checkout = (
                    form.cleaned_data['horario_checkout']
                )

                reserva.save()

            novo_hospede.reservas.add(reserva)

            messages.success(
                request,
                "Reserva do hóspede registrada com sucesso!"
            )

            return redirect(
                "index"
            )

    contexto = {
        "form": form,
    }

    return render(
        request,
        "realizar_reserva.html",
        contexto
    )
