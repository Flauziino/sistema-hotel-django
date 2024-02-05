from django.db import models
from django.contrib.auth import get_user_model


class Portaria(models.Model):

    usuario = models.OneToOneField(
        get_user_model(),
        verbose_name="Usuário",
        on_delete=models.PROTECT,
    )

    nome_completo = models.CharField(
        verbose_name="Nome completo",
        max_length=255,
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
    )

    telefone = models.CharField(
        verbose_name="Telefone para contato",
        max_length=11
    )

    data_nascimento = models.DateField(
        verbose_name="Data de nascimento",
        auto_now=False,
        auto_now_add=False
    )

    class Meta:
        verbose_name = 'Portaria'
        verbose_name_plural = 'Portarias'
        db_table = 'portaria'

    def __str__(self):
        return self.nome_completo
