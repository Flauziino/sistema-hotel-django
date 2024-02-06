from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from .forms import ReservaForm
from .models import Hospede, Reserva

from django.utils import timezone


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


def hospede_info(request, id):

    hospede = get_object_or_404(
        Hospede,
        id=id
    )

    reserva = Reserva.objects.filter(nome_hospede=hospede).first()

    form = ReservaForm()

    if request.method == 'POST':
        form = ReservaForm(
            request.POST,
            instance=hospede
        )

        if form.is_valid():
            hospede = form.save(commit=False)

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
            # Em caso de estadia no hotel, salvar checkout
            elif hospede.status == 'EM_ESTADIA':
                hospede.horario_checkout = timezone.now()

                hospede.status = 'CHECKOUT_REALIZADO'

                hospede.registrado_por = request.user.portaria

                hospede.save()

                messages.success(
                    request,
                    'Check-Out do visitante realizado com sucesso'
                )

            return redirect(
                'usuarios:index'
            )

    contexto = {
        'hospede': hospede,
        'form': form,
        'reserva': reserva,
    }

    return render(
        request,
        'informacoes_hospede.html',
        contexto
    )
