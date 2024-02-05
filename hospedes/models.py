from django.db import models


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
        null=True
    )

    horario_checkin = models.DateTimeField(
        verbose_name="Horário da realização do Check-In",
        auto_now=False,
    )

    horario_checkout = models.DateTimeField(
        verbose_name="Horárrio da realização do Check-Out",
        auto_now=True,
        blank=True,
        null=True
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
