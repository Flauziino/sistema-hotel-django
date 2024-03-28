from hospedes import views

from datetime import timedelta

from django.urls import reverse, resolve

from usuarios.tests.test_usuarios_base import (
    BaseTestMixin, Quarto,
    timezone
)


class HospedesRealizarReservaViewTest(BaseTestMixin):
    def test_hospedes_realizar_reserva_view_function_is_correct(self):
        view = resolve(
            reverse(
                'hospedes:realizar_reserva'
            )
        )
        self.assertIs(view.func.view_class, views.RealizarReservaView)

    def test_hospedes_realizar_reserva_view_returns_statuscode_200_if_logged(self):  # noqa: E501

        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )

        response = self.client.get(
            reverse(
                'hospedes:realizar_reserva'
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_hospedes_realizar_reserva_view_returns_statuscode_302_if_not_logged(self):  # noqa: E501

        response = self.client.get(
            reverse(
                'hospedes:realizar_reserva'
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_hospedes_realizar_reserva_view_redirect_after_statuscode_302_if_not_logged(self):  # noqa: E501

        response = self.client.get(
            reverse(
                'hospedes:realizar_reserva'
            )
        )

        self.assertEqual(response.status_code, 302)
        # Aqui vem o verdadeiro teste
        self.assertRedirects(
            response, response.url
        )

    def test_hospedes_realizar_reserva_view_loads_correct_template(self):
        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )

        response = self.client.get(
            reverse(
                'hospedes:realizar_reserva'
            )
        )

        self.assertTemplateUsed(
            response, 'realizar_reserva.html'
        )

    def test_hospedes_realizar_reserva_view_loads_form_if_request_method_get(self):  # noqa: E501
        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )

        response = self.client.get(
            reverse(
                'hospedes:realizar_reserva'
            )
        )

        self.assertContains(
            response, 'Formulário para reserva do hóspede'
        )

        self.assertIn(
            'form', response.context
        )

    def test_hospedes_realizar_reserva_create_a_reserva_if_user_logged(self):
        # cria o usuario
        user = self.get_user()
        # realiza o login
        self.client.login(
            username=user.username,
            password='12345'
        )

        # liga usuario a portaria de acordo com metodo pré criado
        self.make_porteiro(usuario=user)
        # cria um quarto
        quarto = Quarto.objects.create(
            numero_quarto='101',
            tipo_quarto='PADRAO'
        )

        # pega as datas para simular data de checkin e checkout
        hoje = timezone.now().date()
        amanha = hoje + timedelta(days=1)

        # preenche o formulario
        data = {
            'nome_completo': 'Nome hospede test',
            'cpf': '12345665421',
            'email': 'hospedetest@email.com',
            'telefone': '35991533690',
            'quartos': [quarto.id],
            'status_reserva': 'AGUARDANDO',
            'forma_pagamento': 'A_VISTA',
            'horario_checkin': hoje,
            'horario_checkout': amanha
        }

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=data, follow=True
        )

        # espera-se ver essa msg na tela de index, apos redirecionar
        self.assertIn(
            "Reserva do hóspede registrada com sucesso!",
            response.content.decode('utf-8')
        )

    def test_hospedes_realizar_reserva_cant_create_a_reserva_if_the_date_is_in_the_past(self):  # noqa: E501
        # cria o usuario
        user = self.get_user()
        # realiza o login
        self.client.login(
            username=user.username,
            password='12345'
        )

        # liga usuario a portaria de acordo com metodo pré criado
        self.make_porteiro(usuario=user)
        # cria um quarto
        quarto = Quarto.objects.create(
            numero_quarto='101',
            tipo_quarto='PADRAO'
        )

        # pega as datas para simular data de checkin e checkout
        hoje = timezone.now().date()
        ontem = hoje - timedelta(days=1)
        amanha = hoje + timedelta(days=1)

        # preenche o formulario
        data = {
            'nome_completo': 'Nome hospede test',
            'cpf': '12345665421',
            'email': 'hospedetest@email.com',
            'telefone': '35991533690',
            'quartos': [quarto.id],
            'status_reserva': 'AGUARDANDO',
            'forma_pagamento': 'A_VISTA',
            'horario_checkin': ontem,
            'horario_checkout': amanha
        }

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=data, follow=True
        )

        # espera-se ver essa msg na tela de index, apos redirecionar
        self.assertRedirects(response, '/')
        self.assertIn(
            'Não é possivel reservar para uma data passada!',
            response.content.decode('utf-8')
        )

    def test_hospedes_realizar_reserva_cant_make_a_reserva_if_quarto_is_busy(self):  # noqa: E501
        # cria o usuario
        user = self.get_user()
        # realiza o login
        self.client.login(
            username=user.username,
            password='12345'
        )

        # liga usuario a portaria de acordo com metodo pré criado
        self.make_porteiro(usuario=user)
        # cria um quarto
        quarto = Quarto.objects.create(
            numero_quarto='101',
            tipo_quarto='PADRAO'
        )

        # pega as datas para simular data de checkin e checkout
        hoje = timezone.now().date()
        amanha = hoje + timedelta(days=1)

        # preenche o formulario
        data = {
            'nome_completo': 'Nome hospede test',
            'cpf': '12345665421',
            'email': 'hospedetest@email.com',
            'telefone': '35991533690',
            'quartos': [quarto.id],
            'status_reserva': 'AGUARDANDO',
            'forma_pagamento': 'A_VISTA',
            'horario_checkin': hoje,
            'horario_checkout': amanha
        }

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=data, follow=True
        )

        # repetindo para simular tentativa de cadastrar reserva com quarto
        # ja ocupado
        hoje_2 = timezone.now().date()
        amanha_2 = hoje_2 + timedelta(days=1)

        # preenche o formulario
        data_2 = {
            'nome_completo': 'Outro Hospede test',
            'cpf': '12345665421',
            'email': 'hospedetest@email.com',
            'telefone': '35991533690',
            'quartos': [quarto.id],
            'status_reserva': 'AGUARDANDO',
            'forma_pagamento': 'A_VISTA',
            'horario_checkin': hoje_2,
            'horario_checkout': amanha_2
        }

        url = reverse('hospedes:realizar_reserva')

        response = self.client.post(
            url, data=data_2, follow=True
        )

        # espera-se ver essa msg na tela de index, apos redirecionar
        self.assertRedirects(response, '/')
        self.assertIn(
            f"O quarto {quarto.numero_quarto} já está ocupado nesse período.",
            response.content.decode('utf-8')
        )
