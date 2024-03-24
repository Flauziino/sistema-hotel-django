from usuarios.tests.test_usuarios_base import (
    BaseTestMixin, Reserva,
    Portaria, Hospede, Quarto
)


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

    def test_reserva_forma_pagamento_field_is_a_vista_by_default(self):
        user = self.get_user()

        self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Yoo-test',
        )
        reserva = Reserva.objects.create(nome_hospede=hospede)

        self.assertEqual(
            reserva.forma_pagamento, 'A_VISTA'
        )

    def test_reserva_forma_pagamento_field_has_10_max_length(self):
        user = self.get_user()

        self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Test ?',
        )

        reserva = self.make_reserva(nome_hospede=hospede.nome_completo)

        self.assertEqual(
            reserva._meta.get_field('forma_pagamento').max_length,
            10
        )

    def test_reserva_nome_hospede_is_a_instance_of_hospede(self):  # noqa: E501
        user = self.get_user()

        self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Need to be equal this one',
        )

        reserva = self.make_reserva(nome_hospede=hospede.nome_completo)

        self.assertEqual(
            hospede.nome_completo, reserva.nome_hospede.nome_completo
        )
        self.assertIsInstance(reserva.nome_hospede, Hospede)

    def test_reserva_status_reserva_field_is_aguardando_by_default(self):
        user = self.get_user()

        self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Yoo-test',
        )
        reserva = Reserva.objects.create(nome_hospede=hospede)

        self.assertEqual(
            reserva.status_reserva, 'AGUARDANDO'
        )

    def test_reserva_status_reserva_field_has_15_max_length(self):
        user = self.get_user()

        self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Test ?',
        )

        reserva = self.make_reserva(nome_hospede=hospede.nome_completo)

        self.assertEqual(
            reserva._meta.get_field('status_reserva').max_length,
            15
        )

    def test_reserva_registrado_por_is_a_intance_of_portaria(self):
        user = self.get_user()

        porteiro = self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Hospede',
        )

        reserva = self.make_reserva(
            nome_hospede=hospede.nome_completo,
            registrado_por=porteiro
        )

        self.assertEqual(
            porteiro.nome_completo, reserva.registrado_por.nome_completo
        )
        self.assertIsInstance(reserva.registrado_por, Portaria)

    def test_reserva_quartos_is_a_instance_of_quarto(self):
        user = self.get_user()

        porteiro = self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Hospede',
        )
        quarto = self.make_quarto()
        reserva = self.make_reserva(
            nome_hospede=hospede.nome_completo,
            registrado_por=porteiro
        )
        reserva.quartos.add(quarto)

        self.assertEqual(
            reserva.quartos.first().numero_quarto,
            quarto.numero_quarto
        )

        # Como é um campo manytomany foi feito um FOR
        for quarto_reserva in reserva.quartos.all():
            self.assertIsInstance(quarto_reserva, Quarto)

    def test_reserva_get_status_reserva_display_is_ok(self):
        user = self.get_user()

        self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Yoo-test',
        )

        reserva = Reserva.objects.create(
            nome_hospede=hospede,
            status_reserva='AGUARDANDO'
        )

        self.assertEqual(
            reserva.get_status_reserva_display(),
            'Aguardando confirmação'
        )

    def test_reserva_get_status_forma_pagamento_display_is_ok(self):
        user = self.get_user()

        self.make_porteiro(usuario=user)

        hospede = self.make_hospede(
            nome_completo='Yoo-test',
        )

        reserva = Reserva.objects.create(
            nome_hospede=hospede,
            forma_pagamento='TED'
        )

        self.assertEqual(
            reserva.get_status_forma_pagamento_display(),
            'Transferência bancária'
        )
