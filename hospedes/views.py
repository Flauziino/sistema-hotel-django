from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ReservaForm
from .models import Hospede

from django.utils import timezone


class MyBaseView(View):
    def get_hospede(self, id):
        hospede = get_object_or_404(Hospede, id=id)
        return hospede


@method_decorator(
    login_required(login_url='login', redirect_field_name='next'),
    name='dispatch'
)
class RealizarReservaView(CreateView):
    # model principal
    model = Hospede
    form_class = ReservaForm
    template_name = 'realizar_reserva.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        novo_hospede = Hospede.objects.create(
            nome_completo=form.cleaned_data['nome_completo'],
            telefone=form.cleaned_data['telefone'],
            cpf=form.cleaned_data['cpf'],
            email=form.cleaned_data['email'],
            status='AGUARDANDO_CHECKIN'
        )

        # Criar a reserva associada ao novo hospede
        # Salvando a reserva, mas sem persistir no banco de dados ainda
        # pois ela vai precisar de um hospede para salvar antes.
        reserva = form.save(commit=False)
        reserva.nome_hospede = novo_hospede  # Associando o hospede à reserva
        reserva.registrado_por = self.request.user.portaria
        reserva.status_reserva = 'CONFIRMADO'
        reserva.save()
        reserva.quartos.set(form.cleaned_data['quartos'])
        reserva.horario_checkin = (form.cleaned_data['horario_checkin'])
        reserva.horario_checkout = (form.cleaned_data['horario_checkout'])

        novo_hospede.reservas.add(reserva)

        messages.success(
            self.request,
            "Reserva do hóspede registrada com sucesso!"
        )
        return super().form_valid(form)


@method_decorator(
    login_required(login_url='login', redirect_field_name='next'),
    name='dispatch'
)
class CheckInView(MyBaseView):
    def get(self, request, id):
        hospede = self.get_hospede(id)
        contexto = {'hospede': hospede}
        return render(
            request,
            'checkin.html',
            contexto
        )

    def post(self, request, id):
        hospede = self.get_hospede(id)
        action = request.POST.get('action')

        # Para realizar checkin
        if action == 'check_in' and hospede.status == 'AGUARDANDO_CHECKIN':
            hospede.horario_checkin = timezone.now()
            hospede.horario_checkout = '-'
            hospede.status = 'EM_ESTADIA'
            hospede.registrado_por = request.user.portaria
            hospede.save()

            reserva = hospede.reservas.get(status_reserva='CONFIRMADO')
            reserva.status_reserva = 'EM_ESTADIA'
            reserva.save()

            messages.success(
                request,
                'Check-In do visitante realizado com sucesso'
            )

        # para cancelar reserva
        elif action == 'cancelar_reserva' \
                and hospede.status == 'AGUARDANDO_CHECKIN':

            reserva = hospede.reservas.get(status_reserva='CONFIRMADO')
            reserva.status_reserva = 'CANCELADA'
            reserva.save()

            messages.success(
                request,
                'Reserva do hóspede cancelada com sucesso'
            )
        else:
            messages.error(
                request,
                'Algo deu errado!'
            )

        return redirect('index')


@method_decorator(
    login_required(login_url='login', redirect_field_name='next'),
    name='dispatch'
)
class CheckOutView(MyBaseView):
    def get(self, request, id):
        hospede = self.get_hospede(id)
        context = {'hospede': hospede}
        return render(
            request,
            'checkout.html',
            context
        )

    def post(self, request, id):
        action = request.POST.get('action')

        if action == 'check_out':
            hospede = self.get_hospede(id)
            hospede.status = 'CHECKOUT_REALIZADO'
            hospede.horario_checkout = timezone.now()
            hospede.save()

            messages.success(
                request,
                'Check-Out realizado com sucesso!'
            )

        return redirect('index')
