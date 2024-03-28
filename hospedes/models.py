from django.db import models
from portaria.models import Portaria
from quartos.models import Quarto


class Hospede(models.Model):

    STATUS_HOSPEDE = [
        ("AGUARDANDO_CHECKIN", "Aguardando realizar o check-in"),
        ("EM_ESTADIA", "Em estadia"),
        ("CHECKOUT_REALIZADO", "Estadia finalizada")
    ]

    status = models.CharField(
        verbose_name="Status",
        max_length=20,
        choices=STATUS_HOSPEDE,
        default="AGUARDANDO_CHECKIN"
    )

    nome_completo = models.CharField(
        verbose_name="Nome completo",
        max_length=255
    )

    telefone = models.CharField(
        verbose_name="Telefone do hóspede",
        max_length=11,
        blank=True,
        null=True
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11
    )

    email = models.EmailField(
        verbose_name="E-mail do hospede",
        max_length=255,
        blank=True,
        null=True,
    )

    horario_checkin = models.DateTimeField(
        verbose_name="Horário da realização do Check-In",
        auto_now=False,
        blank=True,
        null=True
    )

    horario_checkout = models.DateTimeField(
        verbose_name="Horário da realização do Check-Out",
        auto_now=True,
        blank=True,
        null=True
    )

    reservas = models.ManyToManyField(
        'Reserva',
        verbose_name='Reservas do hóspede'
    )

    registrado_por = models.ForeignKey(
        Portaria,
        verbose_name="Atendente da portaria responsável pelo Check-In",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def get_cpf(self):
        if self.cpf:
            cpf = str(self.cpf)

            cpf_parte_um = cpf[0:3]
            cpf_parte_dois = cpf[3:6]
            cpf_parte_tres = cpf[6:9]
            cpf_final = cpf[9:]

            cpf_formatado = (
                f'{cpf_parte_um}.{cpf_parte_dois}.{cpf_parte_tres}-{cpf_final}'
            )

            return cpf_formatado

    class Meta:
        verbose_name = "Hóspede"
        verbose_name_plural = 'Hóspedes'
        db_table = 'hospede'

    def __str__(self):
        return self.nome_completo


class Reserva(models.Model):

    STATUS_RESERVA = [
        ('AGUARDANDO', 'Aguardando confirmação'),
        ('EM_ESTADIA', 'Em estadia'),
        ('CONFIRMADO', 'Reserva confirmada'),
        ('CANCELADA', 'Reserva cancelada')
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ("CARD_CRED", "Cartão de crédito"),
        ("CARD_DEB", "Cartão de débito"),
        ("BOLETO", "Boleto bancário"),
        ("TED", "Transferência bancária"),
        ("A_VISTA", "Pagamento a vista")
    ]

    forma_pagamento = models.CharField(
        verbose_name="Forma de pagamento",
        max_length=10,
        choices=FORMA_PAGAMENTO_CHOICES,
        default="A_VISTA"
    )

    nome_hospede = models.ForeignKey(
        Hospede,
        on_delete=models.PROTECT
    )

    status_reserva = models.CharField(
        verbose_name="Status da reserva",
        max_length=15,
        default='AGUARDANDO'
    )

    registrado_por = models.ForeignKey(
        Portaria,
        verbose_name="Atendente responsável pela reserva",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    horario_checkin = models.DateTimeField(
        verbose_name="Horário previsto para realização do Check-In",
        auto_now=False,
        blank=True,
        null=True
    )

    horario_checkout = models.DateTimeField(
        verbose_name="Horário previsto realização do Check-Out",
        auto_now=False,
        blank=True,
        null=True
    )

    quartos = models.ManyToManyField(
        Quarto,
        verbose_name='Quarto reservado pelo hóspede',
    )

    def get_status_reserva_display(self):
        return dict(self.STATUS_RESERVA).get(
            self.status_reserva, self.status_reserva
        )

    def get_status_forma_pagamento_display(self):
        return dict(self.FORMA_PAGAMENTO_CHOICES).get(
            self.forma_pagamento, self.forma_pagamento
        )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        db_table = 'reserva'

    def __str__(self):
        return f'Reserva em nome de: {self.nome_hospede}'
