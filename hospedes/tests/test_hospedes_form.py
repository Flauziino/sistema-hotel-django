from hospedes.forms import ReservaForm
from usuarios.tests.test_usuarios_base import BaseTestMixin

from parameterized import parameterized


class HospedesFormsTest(BaseTestMixin):
    @parameterized.expand([
        ('nome_completo', 'Nome completo:'),
        ('cpf', 'CPF:'),
        ('email', 'E-mail:'),
        ('telefone', 'Telefone:'),
        ('quartos', 'Quarto (Quartos caso haja mais de um):'),
    ])
    def test_form_field_label_is_correct(self, field, needed):
        form = ReservaForm()
        label = form[field].field.label

        self.assertEqual(
            label, needed
        )

    @parameterized.expand([
        ('nome_completo', 'Digite o nome completo do hóspede'),
        ('cpf', 'Digite o CPF do hóspede'),
        ('email', 'Digite o E-mail do hóspede'),
        ('telefone', 'Digite o número de telefone do hóspede'),
    ])
    def test_form_field_placeholder_is_correct(self, field, needed):
        form = ReservaForm()
        placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(
            placeholder, needed
        )
