from django.utils import timezone
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


@login_required
def check_in(request, id):

    hospede = get_object_or_404(Hospede, id=id)

    if request.method == 'POST':

        action = request.POST.get('action')

        # Para realizar checkin
        if action == 'check_in':

            # Verificando se ainda nao foi feito check-in
            if hospede.status == 'AGUARDANDO_CHECKIN':
                hospede.horario_checkin = timezone.now()
                hospede.horario_checkout = '-'

                hospede.status = 'EM_ESTADIA'

                hospede.registrado_por = request.user.portaria

                hospede.save()

                messages.success(
                    request,
                    'Check-In do visitante realizado com sucesso'
                )

            return redirect(
                'index'
            )

        # para cancelar reserva
        elif action == 'cancelar_reserva':

            # Verificando se ainda nao foi feito check-in
            if hospede.status == 'AGUARDANDO_CHECKIN':

                reserva = hospede.reservas.get(status_reserva='CONFIRMADO')
                reserva.status_reserva = 'CANCELADA'
                reserva.save()

                messages.success(
                    request,
                    'Reserva do hóspede cancelada com sucesso'
                )

            return redirect(
                'index'
            )

    contexto = {
        'hospede': hospede,
    }

    return render(
        request,
        'checkin.html',
        contexto
    )


@login_required
def check_out(request, id):

    hospede = get_object_or_404(Hospede, id=id)

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'check_out':
            hospede = get_object_or_404(
                Hospede,
                id=id
            )

            hospede.status = 'CHECKOUT_REALIZADO'
            hospede.horario_checkout = timezone.now()

            hospede.save()

            messages.success(
                request,
                'Check-Out realizado com sucesso!'
            )

            return redirect(
                'index'
            )

    contexto = {
        "hospede": hospede,
    }

    return render(
        request,
        'checkout.html',
        contexto
    )
