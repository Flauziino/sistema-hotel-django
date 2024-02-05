from django import forms
from hospedes.models import Hospede


class HospedeForm(forms.ModelForm):

    class Meta:
        model = Hospede
        fields = [
            "nome_completo", "cpf", "telefone"
        ]

        error_messages = {
            "nome_completo": {
                "required": "O nome completo do hóspede é obrigatório"
            },
            "cpf": {
                "required": "O CPF do hóspede é obrigatório"
            },

            "telefone": {
                "required": "O número do hóspede é obrigatório"
            }
        }
