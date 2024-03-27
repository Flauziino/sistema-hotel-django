from hospedes import views

from datetime import timedelta

from django.urls import reverse, resolve

from usuarios.tests.test_usuarios_base import (
    BaseTestMixin, Quarto, Reserva,
    timezone
)


class HospedesCheckInViewTest(BaseTestMixin):
    def make_full_hospede_no_login(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()
        return hospede

    def make_full_hospede_with_login(self):
        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()
        return hospede

    def test_hospedes_check_in_view_function_is_correct(self):
        hospede = self.make_full_hospede_no_login()

        view = resolve(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )
        self.assertIs(view.func, views.check_in)

    def test_hospedes_check_in_view_returns_statuscode_200_if_logged(self):
        hospede = self.make_full_hospede_with_login()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_hospedes_check_in_view_returns_statuscode_302_if_not_logged(self):
        hospede = self.make_full_hospede_no_login()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_hospedes_check_in_view_redirect_after_statuscode_302_if_not_logged(self):  # noqa: E501
        hospede = self.make_full_hospede_no_login()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 302)
        # Aqui vem o verdadeiro teste
        self.assertRedirects(
            response, response.url
        )

    def test_hospedes_check_in_view_loads_correct_template(self):
        hospede = self.make_full_hospede_with_login()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertTemplateUsed(
            response, 'checkin.html'
        )

    def test_hospedes_check_in_view_raises_404_if_dont_find_hospede(self):
        hospede = self.make_full_hospede_with_login()

        fake_id = hospede.id + 22222

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': fake_id}
            )
        )

        self.assertEqual(
            response.status_code, 404
        )

    def test_hospedes_check_in_view_loads_context_hospede_if_request_method_get(self):  # noqa: E501
        hospede = self.make_full_hospede_with_login()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertIn(
            'hospede', response.context
        )

        self.assertContains(
            response, 'Informações da reserva'
        )

    def test_hospedes_check_in_view_make_check_in_and_redirect_to_index(self):
        hospede = self.make_full_hospede_with_login()

        url = reverse(
            'hospedes:check_in',
            kwargs={'id': hospede.id}
        )

        response = self.client.post(
            url,
            data={'action': 'check_in'},
            follow=True
        )

        self.assertRedirects(
            response, '/'
        )

        self.assertContains(
            response, 'Check-In do visitante realizado com sucesso'
        )

    def test_hospedes_check_in_view_cancel_if_hospede_has_reserva_confirmada_check_in_and_redirect_to_index(self):  # noqa: E501
        # criar um hospede
        hospede = self.make_full_hospede_with_login()

        # simulando uma data para um checkin para hoje
        hoje = timezone.now().date()
        # simulando checkout para amanha
        amanha = hoje + timedelta(days=1)

        # criando um quarto
        quarto = Quarto.objects.create(
            numero_quarto='101',
            tipo_quarto='PADRAO'
        )

        # criando uma reserva para receber o status de "CONFIRMADO"
        reserva = Reserva.objects.create(
            nome_hospede=hospede,
            status_reserva='CONFIRMADO',
            forma_pagamento='A_VISTA',
            horario_checkin=hoje,
            horario_checkout=amanha,
        )

        # adicionando quarto a reserva e salvando a reserva
        reserva.quartos.add(quarto)
        reserva.save()

        # adicionando a reserva ao hospede e salvando o hospede
        hospede.reservas.add(reserva)
        hospede.save()

        url = reverse(
            'hospedes:check_in',
            kwargs={'id': hospede.id}
        )

        response = self.client.post(
            url,
            data={'action': 'cancelar_reserva'},
            follow=True
        )

        # checando se redirecionou a pg de volta para o index
        self.assertRedirects(
            response, '/'
        )

        # checanco se foi recebido a msg de sucesso
        self.assertContains(
            response,
            'Reserva do hóspede cancelada com sucesso',
        )

    def test_hospedes_check_in_view_got_em_estadia_status(self):
        hospede = self.make_full_hospede_with_login()
        hospede.status = 'EM_ESTADIA'
        hospede.save()

        url = reverse(
            'hospedes:check_in',
            kwargs={'id': hospede.id}
        )

        response = self.client.post(
            url,
            data={'action': 'check_in'},
            follow=True
        )

        self.assertRedirects(
            response, '/'
        )

    def test_hospedes_check_in_view_got_another_action_not_check_in_or_cancelar_reserva(self):  # noqa: E501
        hospede = self.make_full_hospede_with_login()
        hospede.status = 'EM_ESTADIA'
        hospede.save()

        url = reverse(
            'hospedes:check_in',
            kwargs={'id': hospede.id}
        )

        response = self.client.post(
            url,
            data={'action': 'cancelar'},
            follow=True
        )

        self.assertIn(
            'hospede', response.context
        )

    def test_hospedes_check_in_view_got_the_right_action_but_hospede_status_not_aguardando_checkin(self):  # noqa: E501
        hospede = self.make_full_hospede_with_login()
        hospede.status = 'EM_ESTADIA'
        hospede.save()

        url = reverse(
            'hospedes:check_in',
            kwargs={'id': hospede.id}
        )

        response = self.client.post(
            url,
            data={'action': 'cancelar_reserva'},
            follow=True
        )

        self.assertRedirects(
            response, '/'
        )
