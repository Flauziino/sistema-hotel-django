from django import forms
from django.core.exceptions import ValidationError

from hospedes.models import Reserva
from quartos.models import Quarto

from collections import defaultdict


class ReservaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        self.fields['nome_completo'].widget.attrs['placeholder'] = 'Digite o nome completo do hóspede'  # noqa: E501
        self.fields['email'].widget.attrs['placeholder'] = 'Digite o E-mail do hóspede'  # noqa: E501
        self.fields['cpf'].widget.attrs['placeholder'] = 'Digite o CPF do hóspede'  # noqa: E501
        self.fields['telefone'].widget.attrs['placeholder'] = 'Digite o número de telefone do hóspede'  # noqa: E501

    nome_completo = forms.CharField(
        required=True,
        label='Nome completo:',
        max_length=150,
    )

    email = forms.CharField(
        required=True,
        max_length=255,
        label='E-mail:',
    )

    cpf = forms.CharField(
        required=True,
        max_length=11,
        label='CPF:',
        help_text='Digite apenas números Ex:15624556712'
    )

    telefone = forms.CharField(
        required=True,
        max_length=11,
        label='Telefone:',
        help_text='Digite apenas números Ex:35991355676'
    )

    status_reserva = forms.ChoiceField(
        choices=Reserva.STATUS_RESERVA,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quartos = forms.ModelMultipleChoiceField(
        label='Quarto (Quartos caso haja mais de um):',
        queryset=Quarto.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    forma_pagamento = forms.ChoiceField(
        choices=Reserva.FORMA_PAGAMENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    horario_checkin = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    horario_checkout = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Reserva

        fields = [
            "nome_completo", "cpf", "email",
            "telefone", "quartos", "status_reserva",
            "forma_pagamento", "horario_checkin", "horario_checkout",
        ]

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        nome_completo = cleaned_data.get('nome_completo')
        cpf = cleaned_data.get('cpf')
        telefone = cleaned_data.get('telefone')

        if nome_completo is not None and len(nome_completo) < 5:
            self._my_errors['nome_completo'].append(
                'O nome completo do hóspede não deve ser tão curto'
            )

        if cpf is not None and len(cpf) < 11:
            self._my_errors['cpf'].append(
                'O CPF deve ter 11 digitos numéricos'
            )

        if telefone is not None and len(telefone) < 11:
            self._my_errors['telefone'].append(
                'O número de telefone deve conter 11 digitos numéricos'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
