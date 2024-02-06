from django import forms
from hospedes.models import Hospede, Reserva
from quartos.models import Quarto
from portaria.models import Portaria


class ReservaForm(forms.ModelForm):

    nome_completo = forms.CharField(
        required=True
    )

    email = forms.CharField(
        required=True,
        max_length=194
    )

    cpf = forms.CharField(
        required=True,
        max_length=11
    )

    telefone = forms.CharField(
        required=True,
        max_length=11
    )

    status_reserva = forms.ChoiceField(
        choices=Reserva.STATUS_RESERVA,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quartos = forms.ChoiceField(
        choices=Quarto.objects.values_list('numero_quarto', 'numero_quarto'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    forma_pagamento = forms.ChoiceField(
        choices=Reserva.FORMA_PAGAMENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    horario_checkin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    horario_checkout = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Reserva

        fields = [
            "nome_completo", "cpf", "email",
            "telefone", "quartos", "status_reserva",
            "forma_pagamento", "horario_checkin", "horario_checkout",
        ]

        widgets = {
            'nome_completo': forms.TextInput(
                attrs={'placeholder': 'Digite o nome completo do hóspede'}
            ),
            'cpf': forms.TextInput(
                attrs={'placeholder': 'Digite o CPF'}
            ),
            'email': forms.TextInput(
                attrs={'placeholder': 'Digite o E-mail'}
            ),
            'telefone': forms.TextInput(
                attrs={'placeholder': 'Digite o número do hóspede'}
            ),
            'quartos': forms.TextInput(
                attrs={'placeholder': 'Digite o número do quarto que o hóspede deseja reservar'}
            ),
            'status_reserva': forms.TextInput(
                attrs={'placeholder': 'Selecione o status da reserva'}
            ),
            'horario_checkin': forms.TextInput(
                attrs={'placeholder': 'Qual horário previsto para check-in?'}
            ),
            'horario_checkout': forms.TextInput(
                attrs={'placeholder': 'Qual horário previsto para check-out?'}
            )
        }

        labels = {
            'nome_completo': 'Nome completo:',
            'cpf': 'CPF:',
            'email': 'E-mail:',
            'telefone': 'Telefone:',
            'quartos': 'Quarto (Quartos caso haja mais de um):',
        }

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
