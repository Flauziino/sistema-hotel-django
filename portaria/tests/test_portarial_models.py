from usuarios.tests.test_usuarios_base import BaseTestMixin

from django.core.exceptions import ValidationError


class PortariaModelTest(BaseTestMixin):
    def test_portaria_string_representation(self):
        porteiro = self.make_porteiro()
        self.assertEqual(
            str(porteiro), porteiro.nome_completo
        )

    def test_portaria_raise_error_if_nome_completo_gt_255_char(self):
        porteiro = self.make_porteiro()
        porteiro.nome_completo = 'A' * 300

        with self.assertRaises(ValidationError):
            porteiro.full_clean()

    def test_portaria_raise_error_CPF_gt_11_char(self):
        porteiro = self.make_porteiro()
        porteiro.cpf = '1' * 15

        with self.assertRaises(ValidationError):
            porteiro.full_clean()

    def test_portaria_raise_error_telefone_gt_11_char(self):
        porteiro = self.make_porteiro()
        porteiro.telefone = '1' * 15

        with self.assertRaises(ValidationError):
            porteiro.full_clean()
