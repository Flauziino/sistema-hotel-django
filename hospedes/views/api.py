from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.db.models import Min
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404

from hospedes.serializers import ReservaSerializer, HospedeSerializer

from hospedes import models


class IndexAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    http_method_names = ['get',]

    def get(self, request):
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
            .filter()
            .values_list('reservas__quartos__numero_quarto', flat=True)
        )

        num_quartos_ocupados = len(quartos_ocupados)

        total_quartos = (
            models.Quarto.objects
            .count()
        )

        reservas = (
            models.Reserva.objects
            .filter(status_reserva='CONFIRMADO', horario_checkin__gte=hoje)
            .order_by('-pk')
        )[:10]

        reservas_proximas = (
            models.Reserva.objects
            .filter(status_reserva='CONFIRMADO', horario_checkin__gte=hoje)
            .annotate(proxima_checkin=Min('horario_checkin'))
            .order_by('proxima_checkin')
        )[:5]

        hospedes = (
            models.Hospede.objects
            .filter(status='EM_ESTADIA',  horario_checkout__gte=hoje)
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

        reservas_data = ReservaSerializer(reservas, many=True).data
        hospedes_data = HospedeSerializer(hospedes, many=True).data
        prox_reserva = ReservaSerializer(reservas_proximas, many=True).data

        data = {
            'inicio_dashboard': 'Início da dashboard',
            'nome_pagina': 'Informações do hotel',
            'reservas': reservas_data,
            'hospedes': hospedes_data,
            'reservas_proximas': prox_reserva,
            'checkin_hoje': ReservaSerializer(checkin_hoje, many=True).data,
            'checkout_hoje': ReservaSerializer(checkout_hoje, many=True).data,
            'ocupacao_hoje': num_quartos_ocupados,
            'quartos_ocupados': list(quartos_ocupados),
            'hospedes_mes': hospedes_mes,
            'total_reservas': total_reservas,
            'total_checkins': total_checkins,
            'total_checkouts': total_checkouts,
            'taxa_ocupacao': f'{taxa_ocupacao:.2f} %',
        }

        return Response(data)


class CriarHospedeAPIView(CreateAPIView):
    serializer_class = HospedeSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['post',]

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer_hospede = self.serializer_class(data=data)
        if serializer_hospede.is_valid():
            serializer_hospede.save(status='AGUARDANDO_CHECKIN')
            messages.success(
                self.request,
                "Reserva do hóspede registrada com sucesso!"
            )
            return Response(serializer_hospede.data,
                            status=status.HTTP_201_CREATED)

        else:
            messages.error(
                self.request,
                'Erro ao criar hóspede. Por favor, verifique os dados.'
            )
            return Response(
                serializer_hospede.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class RealizarReservaAPIView(CreateAPIView):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['post',]

    def post(self, request, *args, **kwargs):
        data = dict(request.data)

        ultimo_hospede = models.Hospede.objects.latest('id')

        data['nome_hospede'] = ultimo_hospede.nome_completo

        horario_checkin = ultimo_hospede.horario_checkin
        horario_checkout = ultimo_hospede.horario_checkout

        serializer_reserva = self.serializer_class(data=data)
        if horario_checkin.date() < timezone.now().date():
            return Response(
                serializer_reserva.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        # selecionando os quartos pelo forms
        quartos_selecionados = data.get('quartos')
        # fazendo filtros para logica de permiçao ou nao de reserva
        # (checando se quarto esta vago no periodo desejado)
        reservas_intersecao = models.Reserva.objects.filter(
            Q(horario_checkin__lt=horario_checkout,
              horario_checkout__gt=horario_checkin) |
            Q(horario_checkin__lte=horario_checkin,
              horario_checkout__gte=horario_checkout)
        )

        # validando se o quarto esta disponivel no periodo especificado
        if serializer_reserva.is_valid():
            for quarto in quartos_selecionados:
                if reservas_intersecao.filter(quartos=quarto).exists():
                    return Response(
                        serializer_reserva.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )

            reserva = serializer_reserva.save(
                nome_hospede=ultimo_hospede,
                registrado_por=self.request.user.portaria
            )

            if reserva:
                ultimo_hospede.reservas.add(reserva)

        return Response(
            serializer_reserva.data,
            status=status.HTTP_201_CREATED
        )


class CheckInAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    http_method_names = ['post', 'get',]

    def get(self, request, id):
        hospede = get_object_or_404(models.Hospede, id=id)
        data = {
            'hospede': HospedeSerializer(hospede, many=False).data
        }
        return Response(data)

    def post(self, request, id):
        hospede = get_object_or_404(models.Hospede, id=id)
        action = request.data.get('action')
        portaria = models.Portaria.objects.all().first()

        if action == 'check_in' and hospede.status == 'AGUARDANDO_CHECKIN':  # noqa: E501
            hospede.horario_checkin = timezone.now()
            hospede.horario_checkout = '-'
            hospede.status = 'EM_ESTADIA'
            hospede.registrado_por = portaria
            hospede.save()

            reserva = hospede.reservas.get(status_reserva='CONFIRMADO')
            reserva.status_reserva = 'EM_ESTADIA'
            reserva.save()

            return Response({
                'message': 'Check-In do visitante realizado com sucesso'
            }, status=status.HTTP_200_OK)

        elif action == 'cancelar_reserva' \
                and hospede.status == 'AGUARDANDO_CHECKIN':
            reserva = hospede.reservas.get(status_reserva='CONFIRMADO')
            reserva.status_reserva = 'CANCELADA'
            reserva.save()

            return Response({
                'message': 'Reserva do hóspede cancelada com sucesso'
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                'error': 'Algo deu errado!'
            }, status=status.HTTP_400_BAD_REQUEST)


class CheckOutAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    http_method_names = ['post', 'get',]

    def get(self, request, id):
        hospede = get_object_or_404(models.Hospede, iped=id)
        data = {
            'hospede': HospedeSerializer(hospede, many=False).data
        }
        return Response(data)

    def post(self, request, id):
        hospede = get_object_or_404(models.Hospede, id=id)
        action = request.data.get('action')

        if action == 'check_out':
            hospede = get_object_or_404(models.Hospede, id=id)
            hospede.status = 'CHECKOUT_REALIZADO'
            hospede.horario_checkout = timezone.now()
            hospede.save()

            return Response({
                'message': 'Check-Out realizado com sucesso!'
            })
