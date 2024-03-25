from django import forms
from hospedes.models import Reserva
from quartos.models import Quarto


class ReservaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome_completo'].widget.attrs['placeholder'] = 'Digite o nome completo do hóspede'  # noqa: E501
        self.fields['email'].widget.attrs['placeholder'] = 'Digite o E-mail do hóspede'  # noqa: E501
        self.fields['cpf'].widget.attrs['placeholder'] = 'Digite o CPF do hóspede'  # noqa: E501
        self.fields['telefone'].widget.attrs['placeholder'] = 'Digite o número de telefone do hóspede'  # noqa: E501

    nome_completo = forms.CharField(
        required=True,
        label='Nome completo:',
    )

    email = forms.CharField(
        required=True,
        max_length=194,
        label='E-mail:',
    )

    cpf = forms.CharField(
        required=True,
        max_length=11,
        label='CPF:',
    )

    telefone = forms.CharField(
        required=True,
        max_length=11,
        label='Telefone:',
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

        error_messages = {
            "nome_completo": {
                "required": "O nome completo do hóspede é obrigatório"
            },
            "cpf": {
                "required": "O CPF do hóspede é obrigatório"
            },
            "email": {
                "required": "O E-mail do hóspede é obrigatório"
            },

            "telefone": {
                "required": "O número do hóspede é obrigatório"
            },

            "quartos": {
                "required": "O número do quarto é obrigatório"
            },

            "horario_checkin": {
                "required": "A previsão de horário de check-in é obrigatório"
            },

            "horario_checkout": {
                "required": "A previsão de horário de check-out é obrigatório"
            }
        }
