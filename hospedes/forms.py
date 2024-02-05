from django import forms
from hospedes.models import Hospede


class HospedeForm(forms.ModelForm):

    class Meta:
        model = Hospede

        fields = [
            "nome_completo", "cpf", "telefone",
            "registrado_por"
        ]

        widgets = {
            'nome_completo': forms.TextInput(
                attrs={'placeholder': 'Digite o nome completo do hóspede'}
            ),
            'cpf': forms.TextInput(
                attrs={'placeholder': 'Digite o CPF'}
            ),
            'telefone': forms.TextInput(
                attrs={'placeholder': 'Digite o número do hóspede'}
            ),
            'registrado_por': forms.TextInput(
                attrs={'placeholder': 'Nome do atendente atual da portaria'}
            )
        }

        labels = {
            'nome_completo': 'Nome completo:',
            'cpf': 'CPF:',
            'telefone': 'Telefone:',
            'registrado_por': 'Nome do atendente:',
        }

        error_messages = {
            "nome_completo": {
                "required": "O nome completo do hóspede é obrigatório"
            },
            "cpf": {
                "required": "O CPF do hóspede é obrigatório"
            },

            "telefone": {
                "required": "O número do hóspede é obrigatório"
            },

            "registrado_por": {
                "required": "Preencha com o atendente atual da portaria"
            }
        }
