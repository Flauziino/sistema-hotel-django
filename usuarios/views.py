from django.db.models import Q
from django.db.models import Min

from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required

from hospedes import models


@method_decorator(
    login_required(login_url='login', redirect_field_name='next'),
    name='dispatch'
)
class Index(TemplateView):
    ordering = ['-id']
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        hoje = timezone.now().date()
        mes = timezone.now().month

        hospedes_mes = (
            models.Hospede.objects
            .filter(
                Q(status='EM_ESTADIA') |
                Q(status='CHECKOUT_REALIZADO')
            )
            .filter(horario_checkin__month=mes)
            .count()
        )

        checkin_hoje = (
            models.Reserva.objects
            .filter(status_reserva='CONFIRMADO')
            .filter(horario_checkin__date=hoje)
            .order_by('horario_checkin')
        )[:5]

        checkout_hoje = (
            models.Reserva.objects
            .filter(status_reserva='CONFIRMADO')
            .filter(horario_checkout__date=hoje)
            .order_by('horario_checkout')
        )[:5]

        quartos_ocupados = (
            models.Hospede.objects
            .filter(status='EM_ESTADIA')
            .values_list('reservas__quartos__numero_quarto', flat=True)
        )

        num_quartos_ocupados = len(quartos_ocupados)

        total_quartos = (
            models.Quarto.objects
            .count()
        )

        reservas = (
            models.Reserva.objects
            .filter(status_reserva='CONFIRMADO')
            .order_by('-pk')
        )

        reservas_proximas = (
            models.Reserva.objects
            .filter(status_reserva='CONFIRMADO')
            .annotate(proxima_checkin=Min('horario_checkin'))
            .order_by('proxima_checkin')
        )[:5]

        hospedes = (
            models.Hospede.objects
            .filter(status='EM_ESTADIA')
            .order_by('-pk')
        )

        total_reservas = (
            models.Reserva.objects
            .filter(status_reserva='CONFIRMADO')
            .count()
        )

        total_checkins = (
            models.Hospede.objects
            .filter(
                Q(status='EM_ESTADIA') |
                Q(status='CHECKOUT_REALIZADO')
            )
            .filter(horario_checkin__date__lte=hoje)
            .count()
        )

        total_checkouts = (
            models.Hospede.objects
            .filter(status='CHECKOUT_REALIZADO')
            .filter(horario_checkout__date__lte=hoje)
            .count()
        )

        taxa_ocupacao = 0
        if total_reservas > 0:
            taxa_ocupacao = (
                num_quartos_ocupados / total_quartos
            ) * 100

        ctx.update({
            'inicio_dashboard': 'Início da dashboard',
            'nome_pagina': 'Informações do hotel',
            'reservas': reservas,
            'hospedes': hospedes,
            'reservas_proximas': reservas_proximas,
            'checkin_hoje': checkin_hoje,
            'checkout_hoje': checkout_hoje,
            'ocupacao_hoje': num_quartos_ocupados,
            'quartos_ocupados': quartos_ocupados,
            'hospedes_mes': hospedes_mes,
            'total_reservas': total_reservas,
            'total_checkins': total_checkins,
            'total_checkouts': total_checkouts,
            'taxa_ocupacao': f'{taxa_ocupacao:.2f} %',
        })

        return ctx
