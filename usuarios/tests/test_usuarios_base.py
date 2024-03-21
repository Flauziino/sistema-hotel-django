from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


from hospedes.models import Hospede, Reserva
from portaria.models import Portaria
from quartos.models import Quarto


class BaseTestMixin(TestCase):
    def get_user(self, username='test', password='12345'):
        user = get_user_model().objects.create_user(
            username=username,
            password=password
        )
        return user

    def make_porteiro(
        self,
        usuario=None,
        nome_completo="porteiro",
        cpf="12345222341",
        telefone="33333434",
        data_nascimento="1995-05-21"
    ):
        return Portaria.objects.create(
            usuario=usuario or self.get_user(),
            nome_completo=nome_completo,
            cpf=cpf,
            telefone=telefone,
            data_nascimento=data_nascimento
        )

    def make_hospede(
        self,
        status="AGUARDANDO_CHECKIN",
        nome_completo="Nome completo",
        telefone="32323355",
        cpf="12345672341",
        email=None,
        registrado_por=None
    ):
        if not email:
            email = f'{get_random_string(5)}@email.com'

        return Hospede.objects.create(
            status=status,
            nome_completo=nome_completo,
            telefone=telefone,
            cpf=cpf,
            email=email,
            registrado_por=registrado_por or self.make_porteiro()
        )

    def make_quarto(
        self,
        numero_quarto='101',
        tipo_quarto='PADRAO'
    ):
        return Quarto.objects.create(
            numero_quarto=numero_quarto,
            tipo_quarto=tipo_quarto
        )

    def make_reserva(
        self,
        forma_pagamento="A_VISTA",
        nome_hospede=None,
        status_reserva='AGUARDANDO',
        registrado_por=None,
        horario_checkin=None,
        horario_checkout=None,
        **kwargs
    ):
        # Criar um dicionário com os argumentos opcionais
        reserva_args = {
            'forma_pagamento': forma_pagamento,
            'status_reserva': status_reserva,
            'registrado_por': registrado_por or self.make_porteiro(),
            'horario_checkin': horario_checkin or timezone.now(),
            'horario_checkout': horario_checkout or timezone.now(),
            **kwargs  # Desempacotar os argumentos opcionais adicionais
        }

        # Se nome_hospede foi fornecido,
        # tentar encontrar a instância de Hospede correspondente
        if nome_hospede:
            try:
                hospede = Hospede.objects.get(nome_completo=nome_hospede)
                reserva_args['nome_hospede'] = hospede
            except Hospede.DoesNotExist:
                raise ValueError(
                    f"Hospede com o nome '{nome_hospede}' não existe.")

        # Criar a reserva com os argumentos fornecidos
        return Reserva.objects.create(**reserva_args)
