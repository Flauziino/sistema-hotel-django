from datetime import timedelta

from django.urls import reverse

from hospedes.forms import ReservaForm
from usuarios.tests.test_usuarios_base import (
    BaseTestMixin, Quarto,
    timezone
)

from parameterized import parameterized


class HospedesFormsTest(BaseTestMixin):
    def setUp(self):
        # data de hoje para checkin
        self.hoje = timezone.now().date()
        # data de amanha para checkin
        self.amanha = self.hoje + timedelta(days=1)

        # criando um quarto
        self.quarto = Quarto.objects.create(
            numero_quarto='101',
            tipo_quarto='PADRAO'
        )

        # simulando a criaçao de uma reserva cadastrando um hospede
        self.form_data = {
            'nome_completo': 'Nome hospede test',
            'cpf': '12345665421',
            'email': 'hospedetest@email.com',
            'telefone': '35991533690',
            'quartos': [self.quarto.id],
            'status_reserva': 'AGUARDANDO',
            'forma_pagamento': 'A_VISTA',
            'horario_checkin': self.hoje,
            'horario_checkout': self.amanha
        }

    # criando metodo para um usuario logado, pois alguns testes nao utilizarao
    # usuario
    def loged_user(self):
        self.user = self.get_user()
        return self.client.force_login(self.user)

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

    @parameterized.expand([
        ('cpf', 'Digite apenas números Ex:15624556712'),
        ('telefone', 'Digite apenas números Ex:35991355676'),
    ])
    def test_form_field_help_text_is_correct(self, field, needed):
        form = ReservaForm()
        helptext = form[field].field.help_text

        self.assertEqual(
            helptext, needed
        )

    #########################################################
    # a partir daqui serao feitos alguns testes de integraçao
    #########################################################
    @parameterized.expand([
        ('nome_completo', 'Este campo é obrigatório.'),
        ('cpf', 'Este campo é obrigatório.'),
        ('email', 'Este campo é obrigatório.'),
        ('telefone', 'Este campo é obrigatório.'),
        ('quartos', ''),
        ('status_reserva', ''),
        ('forma_pagamento', ''),
        ('horario_checkin', ''),
        ('horario_checkout', ''),
    ])
    def test_nome_completo_cpf_email_and_telefone_cannot_be_empty(self, field, msg):  # noqa: E501
        self.loged_user()

        self.form_data[field] = ' '
        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data
        )

        self.assertContains(
            response, msg
        )

    def test_user_cant_acces_urls_realizar_reserva_if_not_logged_in_code_302(self):  # noqa: E501
        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data,
        )

        self.assertEqual(
            response.status_code, 302
        )

    def test_user_redirect_to_login_page_if_not_logged_in(self):
        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data, follow=True
        )

        self.assertEqual(
            response.status_code, 200
        )

        # Checando se a msg do inicio esta presente, provando que esta na
        # tela de login
        self.assertContains(
            response, 'Seja bem-vindo!'
        )

    def test_nome_completo_field_min_length_shoud_be_5_char(self):
        self.loged_user()

        self.form_data['nome_completo'] = 'joa'

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data
        )

        msg = 'O nome completo do hóspede não deve ser tão curto'

        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_nome_completo_field_max_length_shoud_be_less_than_150_char(self):
        self.loged_user()

        self.form_data['nome_completo'] = 'a' * 151

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data
        )

        msg = 'Certifique-se de que o valor tenha no máximo 150 caracteres (ele possui 151)'  # noqa: E501

        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_email_field_max_length_shoud_be_less_than_256_char(self):
        self.loged_user()

        self.form_data['email'] = ('a' * 256) + '@email.com'

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data
        )

        msg = 'Certifique-se de que o valor tenha no máximo 255 caracteres (ele possui 266).'  # noqa: E501

        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_cpf_field_length_shoud_be_11_char(self):
        self.loged_user()

        # testando para mais que 11 chars
        self.form_data['cpf'] = '1' * 12

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data
        )

        msg = 'Certifique-se de que o valor tenha no máximo 11 caracteres (ele possui 12).'  # noqa: E501

        self.assertIn(
            msg, response.content.decode('utf-8')
        )

        # testando para menos que 11 chars
        self.form_data['cpf'] = '1' * 10

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data
        )

        msg = 'O CPF deve ter 11 digitos numéricos'  # noqa: E501

        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_telefone_field_length_shoud_be_11_char(self):
        self.loged_user()

        # testando para mais que 11 chars
        self.form_data['telefone'] = '3' * 12

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data
        )

        msg = 'Certifique-se de que o valor tenha no máximo 11 caracteres (ele possui 12).'  # noqa: E501

        self.assertIn(
            msg, response.content.decode('utf-8')
        )

        # testando para menos que 11 chars
        self.form_data['telefone'] = '4' * 10

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data
        )

        msg = 'O número de telefone deve conter 11 digitos'  # noqa: E501

        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_user_can_create_a_reserva(self):
        user = self.loged_user()

        self.make_porteiro(usuario=user)

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=self.form_data, follow=True
        )

        self.assertIn(
            "Reserva do hóspede registrada com sucesso!",
            response.content.decode('utf-8')
        )
