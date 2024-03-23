from django.core.exceptions import ValidationError

from usuarios.tests.test_usuarios_base import BaseTestMixin, Hospede


class HospedesModelTest(BaseTestMixin):
    def test_hospedes_model_string_representation(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()
        self.assertEqual(
            str(hospede), hospede.nome_completo
        )

    def test_hospedes_model_status_is_aguardando_checkin_by_default(self):
        hospede = Hospede.objects.create(
            nome_completo='Testiiiiing'
        )
        hospede.save()

        self.assertEqual(
            hospede.status, 'AGUARDANDO_CHECKIN'
        )

    def test_hospedes_status_field_max_length(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()

        self.assertEqual(
            hospede._meta.get_field('status').max_length,
            20
        )

    def test_hospedes_nome_completo_field_raises_error_if_max_length_gt_255_char(self):  # noqa: E501
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()
        hospede.nome_completo = 'a' * 300

        with self.assertRaises(ValidationError):
            hospede.full_clean()

    def test_hospedes_telefone_field_raises_error_if_max_length_gt_11_char(self):  # noqa: E501
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()
        hospede.telefone = '1' * 15

        with self.assertRaises(ValidationError):
            hospede.full_clean()

    def test_hospedes_cpf_field_raises_error_if_max_length_gt_11_char(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()
        hospede.cpf = '1' * 15

        with self.assertRaises(ValidationError):
            hospede.full_clean()

    def test_hospedes_email_field_raises_error_if_max_length_gt_255_char(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()
        hospede.email = '1' * 300

        with self.assertRaises(ValidationError):
            hospede.full_clean()

    def test_hospedes_get_cpf_method_is_working_right(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()

        # O cpf padrao recebido é "12345672341" e deve ser retornado ele
        # editado no formato de cpf, espera-se "123.456.723-41" nesse caso
        self.assertEqual(
            hospede.get_cpf(), "123.456.723-41"
        )

    def test_hospedes_get_cpf_method_dont_get_a_cpf(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()
        hospede.cpf = ''

        # Testando caso o metodo nao receba cpf.
        self.assertIsNone(hospede.get_cpf())
