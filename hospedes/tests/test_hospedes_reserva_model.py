from django.core.exceptions import ValidationError

from usuarios.tests.test_usuarios_base import BaseTestMixin


class ReservaModelTest(BaseTestMixin):
    def test_reserva_model_string_representation(self):
        user = self.get_user()

        self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Test ?',
        )

        reserva = self.make_reserva(nome_hospede=hospede.nome_completo)
        self.assertEqual(
            str(reserva), f'Reserva em nome de: {reserva.nome_hospede}'
        )
